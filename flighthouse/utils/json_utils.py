# file to store useful json utilities
import json, os
from pathlib import Path
from typing import Optional

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
    

def create_json(vehicles:list, obstacles:list|None=None, file_path:Optional[str|None]=None)->dict:
    output = {'name': 'flighthouse_output'}
    building_info = [
        {
        "ID": f"B{idx}",
        "vertices": vertices
        }
        for idx, vertices in enumerate(obstacles)  
    ]
    vehicle_info = [
        {
        "ID": f"B{idx}",
        "radius": 0.1,
        "path": path
        }
        for idx, path in enumerate(vehicles)  
    ]
    output["buildings"] = building_info
    output["vehicles"] = vehicle_info
    if file_path:
        dump_to_json(file_path, output)
    return output







