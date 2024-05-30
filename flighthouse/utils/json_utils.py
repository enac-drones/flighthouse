# file to store useful json utilities
import json, os
from pathlib import Path


def load_from_json(file_path: str) -> dict:
    """load case data from json"""
    file_path = Path(file_path).resolve()
    with open(file_path, "r") as f:
        file_contents = json.load(f)
        return file_contents


def dump_to_json(file_path: str, data: dict) -> dict:
    # ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        return None


