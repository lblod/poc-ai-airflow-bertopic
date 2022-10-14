import uuid

import fire
import requests
from tqdm import tqdm

from gcs import read_json


def save(endpoint):
    records = read_json(file_name="BERTopic_output.json")
    for record in tqdm(records):
        try:
            new_uri = f"http://data.lblod.info/ML2GrowTopicModeling/{str(uuid.uuid4())}"

            q = f"""
            PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
    
                 DELETE{{
             GRAPH <http://mu.semte.ch/application> {{
            <{record['thing']}> ext:HasTopic ?topic_link ; ext:ingestedByMl2GrowSmartRegulationsTopics ?srt . 
            ?topic_link ext:TopicURI ?topic_uri ; ext:score ?topic_score .
             }}
             }}
                         WHERE {{
               GRAPH <http://mu.semte.ch/application> {{
                <{record['thing']}> ext:HasTopic ?topic_link ; ext:ingestedByMl2GrowSmartRegulationsTopics ?srt . 
                ?topic_link ext:TopicURI ?topic_uri ; ext:score ?topic_score .
              }}
             }}
            """
            r = requests.post(endpoint, data={"query": q},
                              headers={"Accept": "application/sparql-results+json,*/*;q=0.9"})

            q = f"""
            PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
            INSERT {{
            GRAPH <http://mu.semte.ch/application> {{
            <{record['thing']}> ext:HasTopic <{new_uri}> ; ext:ingestedByMl2GrowSmartRegulationsEmbedding "1" .
    
            <{new_uri}> a ext:TopicScore;
            ext:TopicURI <http://data.lblod.info/ML2GrowTopicModeling/topic/{record['topic']}>; 
            ext:score {record['probability']} .
                    }}
            }}
            """

            r = requests.post(endpoint, data={"query": q},
                              headers={"Accept": "application/sparql-results+json,*/*;q=0.9"})
        except Exception as ex:
            print(ex)
            print(r.text)


if __name__ == "__main__":
    fire.Fire(save)
