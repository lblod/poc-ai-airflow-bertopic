import json
from pathlib import Path

storage_dir = Path("/data")


def read_json(file_name: str) -> dict:
    with open(storage_dir / file_name, "r") as f:
        return json.load(f)


def write_json(file_name: str, content):
    write_string(file_name, json.dumps(content))


def write_string(file_name: str, content: str):
    with open(storage_dir / file_name, "w") as f:
        f.write(content)