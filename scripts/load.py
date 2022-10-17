import fire
import requests

from gcs import write_json


def load(endpoint, query):
    """
    This executes a sparql query and laods it straight into pandas.

    :param endpoint: The url where to sparql endpoint can be found
    :param query: The query to execute on the given sparql endpoint.
    :return: Nothing
    """
    headers = {
        "Accept": "application/sparql-results+json,*/*;q=0.9"
    }

    # Created request
    r = requests.post(endpoint, data={"query": query}, headers=headers)
    assert r.status_code == 200, "Incorrect status code returned"

    # processing data from the response to the pandas data frame and saving it
    data = r.json()["results"]["bindings"]
    records = [{k: v['value'] for k, v in i.items()} for i in data]
    write_json(file_name="export.json", content=records)


if __name__ == '__main__':
    fire.Fire(load)
