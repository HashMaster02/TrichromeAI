import pathlib
from pathlib import Path
from collections import defaultdict, Counter
from functools import reduce
import re
import json
import matplotlib.pyplot as plt
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color


class JsonSetEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)

def extract_colors_to_defaultdict(raw_data_filepath: pathlib.Path) -> defaultdict[str, set]:
    color_palette = defaultdict(set)

    try:
        with open(file=raw_data_filepath, mode="r", encoding="utf-8") as raw_data:
            for line in raw_data:
                line = line.strip()
                color_label, color = line.split(" ")

                company_name_split_pattern = r"^([a-z0-9\-]+?)(?=-\d+:|:)\s*"
                company_key = re.split(company_name_split_pattern, color_label)[1]
                color_palette[company_key].add(color)
    except FileNotFoundError:
        print(f"Error: The filepath {raw_data_filepath} was not found. Please ensure the file exists.")
    except Exception as e:
        print(f"Error: {e}")
    
    return color_palette

def save_dict_to_json(data: defaultdict | dict, output_filepath: pathlib.Path):
    try:
        with open(file=output_filepath, mode="w", encoding="utf-8") as json_file:
            json.dump(dict(data), json_file, indent=2, cls=JsonSetEncoder)
    except FileNotFoundError:
        print(f"Error: The filepath {output_filepath} is incorrect. Please ensure the directory exists.")
    except Exception as e:
        print(f"Error: {e}")

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

def convert_dict_itemlist_to_itemlist_frequencies(dictionary: dict[str, list]) -> dict[str, int]:
    itemlist_frequencies = map(lambda item: len(item), dictionary.values())
    item_to_freq_dict = dict(zip(dictionary.keys(), itemlist_frequencies))
    return item_to_freq_dict 

def plot_bar_chart(x_axis, y_axis):
    # Plot as bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(x_axis, y_axis, color='skyblue', edgecolor='black')

    # Add x_axis and title
    plt.xlabel('Label')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution')
    plt.xticks(x_axis, rotation=45)

    # Show plot
    plt.tight_layout()
    plt.show()

def filter_palettes(palette: dict, paeltte_freq: int = 3) -> dict:
    _filtered = dict(filter(lambda item: item if len(item[1]) >= paeltte_freq else None , palette.items()))
    return _filtered

def truncate_color_palettes(color_palettes: dict, required_palette_size: int) -> dict[str, list[str]]:
    truncated_color_palettes = map(lambda item: item[1][:required_palette_size], color_palettes.items())
    res = dict(zip(color_palettes.keys(), truncated_color_palettes))
    return res

def hex_to_lab(hex_color_string: str) -> LabColor:
    rgb_color = sRGBColor.new_from_rgb_hex(hex_color_string)
    lab_color = convert_color(rgb_color, LabColor)  # this function should return a LabColor object
    return lab_color

def convert_hexlist_to_lablist(color_palette: list[str]) -> list[dict[str, float]]:
    new_color_palette = []
    for hex_color in color_palette:
        lab_col = hex_to_lab(hex_color)
        new_color_palette.append(
            {'lab_l': lab_col.lab_l,
             'lab_a': lab_col.lab_a,
             'lab_b': lab_col.lab_b}
        )
    return new_color_palette

def main():

    truncated_colors_filepath = Path().cwd() / "dataset" / "HEX" / "truncated-selected-colors.json"
    # Run this if you want to create the final palettes used in the dataset
    if False:
        raw_data_path = Path().cwd() / "dataset" / "raw" / "all-colors.txt"
        json_data_path = Path().cwd() / "dataset" / "raw" / "all-colors.json"

        all_colors_hex = extract_colors_to_defaultdict(raw_data_path)
        save_dict_to_json(all_colors_hex, json_data_path)
        filtered_color_palettes_hex = filter_palettes(load_json_as_dict(json_data_path))
        truncated_color_palettes_hex = truncate_color_palettes(filtered_color_palettes_hex, required_palette_size=3)
        save_dict_to_json(truncated_color_palettes_hex, truncated_colors_filepath)

    lab_truncated_colors_filepath = Path().cwd() / "dataset" / "LAB" / "truncated-selected-colors.json"
    final_color_palettes = load_json_as_dict(truncated_colors_filepath)
    lab_color_palettes = dict(zip(final_color_palettes.keys() ,map(convert_hexlist_to_lablist, final_color_palettes.values())))
    save_dict_to_json(lab_color_palettes, lab_truncated_colors_filepath)

if __name__ == "__main__":
    main()