from bertopic_helper import BERTopicHelper as bth
from gcs import read_json, write_json
import pandas as pd
import fire

topic_model = bth()


def main():
    records = read_json(file_name="sparql_input.json")
    # print("text", [r["text"] for r in records])
    topics, probs = topic_model.transform([r["text"][:10_000] for r in records])

    df = pd.DataFrame(records)
    df["topic"] = topics
    df["probability"] = probs

    # new_records = [{"topics": x[0], "probabilities": x[1], **x[2]} for x in zip(topics, probs, records)]

    # print(new_records)
    write_json("BERTopic_output.json", content=df.to_dict(orient="records"))


if __name__ == "__main__":
    fire.Fire(main)
