import json
from pathlib import Path

# Reference to the data path where the airflow-data volume is mounted.
storage_dir = Path("/data")


def read_json(file_name: str) -> dict:
    """
    Loads the content from a json file.

    :param file_name: filename to open and load json content from.
    :return: a dict, containing the content of the given file
    """
    with open(storage_dir / file_name, "r") as f:
        return json.load(f)


def write_json(file_name: str, content) -> None:
    """
    Calls the write_string function

    :param file_name: the name to create a file
    :param content: the content to write to the file
    :return:
    """
    write_string(file_name, json.dumps(content))


def write_string(file_name: str, content: str) -> None:
    """
    Funciton that writes a json string to local storage

    :param file_name: name to create such file
    :param content: the content to write to the file
    :return:  None
    """
    with open(storage_dir / file_name, "w") as f:
        f.write(content)
