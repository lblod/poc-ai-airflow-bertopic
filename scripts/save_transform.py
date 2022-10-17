import uuid

import fire
from tqdm import tqdm

from gcs import read_json
from util import make_request


def save(endpoint: str):
    """
    Function that takes transformed output from bertopic and writes it to sparql

    :param endpoint: the url to the sparql endpoint
    :return:
    """
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

            # request for delete statement
            make_request(endpoint=endpoint, query=q)

            q = f"""
            PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
            INSERT {{
            GRAPH <http://mu.semte.ch/application> {{
            <{record['thing']}> ext:HasTopic <{new_uri}> ; ext:ingestedByMl2GrowSmartRegulationsTopics "1" .
    
            <{new_uri}> a ext:TopicScore;
            ext:TopicURI <http://data.lblod.info/ML2GrowTopicModeling/topic/{record['topic']}>; 
            ext:score {record['probability']} .
                    }}
            }}
            """
            # request for insert statement
            make_request(endpoint=endpoint, query=q)

        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    fire.Fire(save)
