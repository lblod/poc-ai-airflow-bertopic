import requests
from gcs import write_json
import fire


def load(endpoint, query):
    headers = {
        "Accept": "application/sparql-results+json,*/*;q=0.9"
    }

    r = requests.post(endpoint, data={"query": query}, headers=headers)
    assert r.status_code == 200, "Incorrect status code returned"
    data = r.json()["results"]["bindings"]
    records = [{k: v['value'] for k,v in i.items()} for i in data]
    write_json(file_name="sparql_input.json", content=records)


if __name__ == '__main__':
    fire.Fire(load)
