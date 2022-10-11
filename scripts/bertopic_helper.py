from bertopic import BERTopic
from transformers import AutoTokenizer, AutoModel
import os


# os.environ['TRANSFORMERS_OFFLINE']='1'

class BERTopicHelper:

    def __init__(
            self,
            content_file: str = "/data/something.json",
            embedding_model_path: str = "/models/RobertaModel_PDF_V1",
            topic_model_path: str = "/models/topic.model",
            min_topic_size=20,
            from_scratch=False,
    ):
        embed_model = AutoModel.from_pretrained(embedding_model_path)
        self.model_path = topic_model_path

        if from_scratch:
            self.topic_model = BERTopic(self.model_path, embedding_model=embed_model, min_topic_size=min_topic_size,
                                        verbose=True)
        else:
            self.topic_model = BERTopic.load(self.model_path, embedding_model=embed_model)

    def train_and_save(self, input_texts):
        input_texts = [t for t in input_texts]
        self.topic_model.fit(input_texts)
        self.topic_model.save(self.model_path, save_embedding_model=False)

        # TODO: add writing files to the folder with tags to get the correct information

    def transform(self, input_texts):
        topics, probs = self.topic_model.transform(input_texts)
        return topics, probs
