import torch
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

seed = 1
import random
import numpy as np

random.seed(seed)
np.random.seed(seed)

torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)


class BERTopicHelper:
    """
    Helper class containing some basic functionality to easily adapt and update the bertopic model/ documents.
    """

    def __init__(
            self,
            content_file: str = "/data/something.json",
            embedding_model_path: str = "/models/RobertaModel_PDF_V1",
            topic_model_path: str = "/models/topic.model",
            min_topic_size=20,
            from_scratch=False,
    ):
        """
        The init function takes in arguments, and sets up the required configuration for the bertopic model

        :param content_file:
        :param embedding_model_path:
        :param topic_model_path:
        :param min_topic_size:
        :param from_scratch:
        """
        embed_model = SentenceTransformer(embedding_model_path)
        self.model_path = topic_model_path

        if from_scratch:
            self.topic_model = BERTopic(self.model_path, embedding_model=embed_model, min_topic_size=min_topic_size,
                                        verbose=True)
        else:
            self.topic_model = BERTopic.load(self.model_path, embedding_model=embed_model)

    def train_and_save(self, input_texts):
        """
        This function triggers a retrain of the bertopic model and save it
        :param input_texts: a list of all the content from the loaded files
        :return:
        """
        input_texts = [t for t in input_texts]
        self.topic_model.fit(input_texts)
        self.topic_model.save(self.model_path, save_embedding_model=False)

    def transform(self, input_texts):
        """
        This function executes the transform for

        :param input_texts: a list of all the content from the loaded files
        :return: the topics and probabilities
        """
        topics, probs = self.topic_model.transform(input_texts)
        return topics, probs
