from pathlib import Path
from collections import defaultdict
from json_utils import load_json_as_dict, save_dict_to_json

if __name__ == "__main__":
    COLORS_FILEPATH = Path().cwd() / "dataset" / "colors" / "LAB" / "truncated-selected-colors.json"
    DESCRIPTIONS_FILEPATH = Path().cwd() / "dataset" / "descriptions" / "descriptions.json"
    OUTPUT_FILEPATH = Path().cwd() / "dataset" / "data.json"

    colors = load_json_as_dict(COLORS_FILEPATH)
    descriptions = load_json_as_dict(DESCRIPTIONS_FILEPATH)

    dataset = defaultdict(str)
    for brand in descriptions.keys():
        desc = descriptions[brand]
        col = colors[brand]
        dataset[desc] = col

    save_dict_to_json(data=dataset, output_filepath=OUTPUT_FILEPATH)
