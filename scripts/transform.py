import fire
import pandas as pd

from bertopic_helper import BERTopicHelper as bth
from gcs import read_json, write_json

# Instantiate the topic model helper class.
topic_model = bth()


def main():
    """
    This function loads the sparql document corpus and starts the transformation of linking correct topics.
    :return:
    """
    records = read_json(file_name="sparql_input.json")
    topics, probs = topic_model.transform([r["text"][:10_000] for r in records])

    df = pd.DataFrame(records)
    df["topic"] = topics
    df["probability"] = probs

    write_json("BERTopic_output.json", content=df.to_dict(orient="records"))


if __name__ == "__main__":
    fire.Fire(main)
