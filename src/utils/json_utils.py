import json
import pathlib
from collections import defaultdict


class JsonSetEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)

def load_json_as_dict(filepath: pathlib.Path) -> dict:
    data = dict()

    try:
        with open(file=filepath, mode="r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found. Please ensure the file exists.")
    except Exception as e:
        print(f"Error: {e}")
    
    return data

def save_dict_to_json(data: defaultdict | dict, output_filepath: pathlib.Path):
    try:
        with open(file=output_filepath, mode="w", encoding="utf-8") as json_file:
            json.dump(dict(data), json_file, indent=2, cls=JsonSetEncoder)
    except FileNotFoundError:
        print(f"Error: The filepath {output_filepath} is incorrect. Please ensure the directory exists.")
    except Exception as e:
        print(f"Error: {e}")