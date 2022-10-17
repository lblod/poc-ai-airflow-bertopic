import fire
from bertopic import BERTopic
from tqdm import tqdm

from util import make_request


def get_clear_queries(topic_model):
    """
    Function that creates the required queries to clear out the space needed to save new topics
    :param topic_model: the actual topic model itself
    :return: a list with clear queries
    """
    topic_dict = {}
    for topic, count, name in topic_model.get_topic_info().itertuples(name=None, index=False):
        topic_dict = {
            **topic_dict,
            **{
                topic: {
                    "count": count,
                    "relevant_words": [{"word": item[0], "score": item[1]} for item in topic_model.get_topics()[topic]],
                    "topic_label": "_".join(name.split("_")[1:])
                }
            }
        }

    uris, sparql_obj = [], []
    for k, v in topic_dict.items():
        topic_base_uri = f"http://data.lblod.info/ML2GrowTopicModeling/topic/{k}"
        uris.append(topic_base_uri)

        relevant_word_uri, relevant_obj = [], []
        for i, word in enumerate(v["relevant_words"]):
            word_uri = f"{topic_base_uri + '/relevant_words/' + str(i)}"
            relevant_word_uri.append(f"<{word_uri}>")
            relevant_obj.append(
                f"<{word_uri}> a ext:relevant_word; ext:word \"{word['word']}\" ; ext:score {word['score']} .")

        joined = ' \n '.join(relevant_obj)
        sparql_query = f"""
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
        
        DELETE {{
            GRAPH <http://mu.semte.ch/application> {{
            <{topic_base_uri}> ext:relevant_words ?words;  ext:count ?count; ext:topic_label ?label .
            
            {joined}
            }}
        }}
        WHERE {{
            GRAPH <http://mu.semte.ch/application> {{
            <{topic_base_uri}> ext:relevant_words ?words;  ext:count ?count; ext:topic_label ?label .
            
            {joined}
            }}
        }}
        """
        sparql_obj.append(sparql_query)
    return sparql_obj


def get_insert_queries(topic_model):
    """
    This function generates a list of insert queries to define the new topic model in the sparql environment.

    :param topic_model: the actual topic model
    :return:
    """

    topic_dict = {}
    for topic, count, name in topic_model.get_topic_info().itertuples(name=None, index=False):
        topic_dict = {
            **topic_dict,
            **{
                topic: {
                    "count": count,
                    "relevant_words": [{"word": item[0], "score": item[1]} for item in topic_model.get_topics()[topic]],
                    "topic_label": "_".join(name.split("_")[1:])
                }
            }
        }

    uris, sparql_obj = [], []
    for k, v in topic_dict.items():
        topic_base_uri = f"http://data.lblod.info/ML2GrowTopicModeling/topic/{k}"
        uris.append(topic_base_uri)

        relevant_word_uri, relevant_obj = [], []
        for i, word in enumerate(v["relevant_words"]):
            word_uri = f"{topic_base_uri + '/relevant_words/' + str(i)}"
            relevant_word_uri.append(f"<{word_uri}>")
            relevant_obj.append(
                f"<{word_uri}> a ext:relevant_word; ext:word \"{word['word']}\" ; ext:score {word['score']} .")

        joined = ' \n '.join(relevant_obj)
        sparql_query = f"""
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

        INSERT {{
            GRAPH <http://mu.semte.ch/application> {{

                <{topic_base_uri}> a ext:isTopic; ext:relevant_words {", ".join(relevant_word_uri)} ; ext:count {v['count']} ; ext:topic_label \"{v['topic_label']}\" . 

                {joined}
            }}
        }}
        """
        sparql_obj.append(sparql_query)
    return sparql_obj


def save(endpoint: str):
    """
    Function that prepares and saves the topics to sparql.

    :param endpoint: sparql endpoint url
    :return:
    """

    # Load the topic model to extract the topic information from
    topic_model = BERTopic.load("/models/topic.model")

    # Loop for deleteing --> can prob be optimized in one query
    for q in tqdm(get_clear_queries(topic_model)):
        try:
            make_request(endpoint=endpoint, query=q)

        except Exception as ex:
            print(ex)

    # Loop for inserting --> can prob be optimized in one query
    for q in tqdm(get_insert_queries(topic_model)):
        try:
            make_request(endpoint=endpoint, query=q)

        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    fire.Fire(save)
