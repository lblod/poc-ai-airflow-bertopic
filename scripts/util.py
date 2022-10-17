import requests


def make_request(endpoint: str, query: str, headers: dict = {"Accept": "application/sparql-results+json,*/*;q=0.9"}):
    """
    Very basic function that just checks if it was succesfull, fails if not.
    :param endpoint: the sparql endpoint
    :param query: the sparql query
    :param headers: http headers to add
    :return:
    """
    r = requests.post(endpoint, data={"query": query}, headers=headers)

    if r.status_code != 200:
        print(f"[FAILURE] {50 * '-'} /n {query} /n {50 * '-'}")

    raise Exception(f"Failed to upload data for query : {query} with error {r.text}")
