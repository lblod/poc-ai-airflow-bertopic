import fire

from bertopic_helper import BERTopicHelper as bth
from gcs import read_json

# Instantiate the topic model helper class.
topic_model = bth(from_scratch=True, min_topic_size=10)


def main():
    """
    This function loads the input data and retrains the topic model
    :return:
    """
    records = read_json(file_name="sparql_input.json")
    if not records:
        raise Exception("ERROR IF RECORDS IS EMPTY")
    topic_model.train_and_save([r["text"][:10_000] for r in records])


if __name__ == "__main__":
    fire.Fire(main)
