from  bertopic_helper import BERTopicHelper as bth
from gcs import read_json, write_json
import fire

topic_model = bth(from_scratch=True, min_topic_size=10)

def main():
    records = read_json(file_name="sparql_input.json")
    topic_model.train_and_save([r["text"][:10_000] for r in records])

if __name__ == "__main__":
    fire.Fire(main)