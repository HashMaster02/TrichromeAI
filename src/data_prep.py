import pathlib
from pathlib import Path
from collections import defaultdict, Counter
from functools import reduce
import re
import json
import matplotlib.pyplot as plt


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

def save_defaultdict_to_json(data: defaultdict, output_filepath: pathlib.Path):
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

def map_dict_itemlist_to_itemlist_frequencies(dictionary: dict[str, list]) -> dict[str, int]:
    itemlist_frequencies = map(lambda item: len(item), dictionary.values())
    item_to_freq_dict = dict(zip(dictionary.keys(), itemlist_frequencies))
    return item_to_freq_dict 

def print_total_samples(labels, frequencies, palette_threshold: int = 3) -> int:
    _filtered = list(filter(lambda item: item if item[0] >= 3 else None, zip(labels, frequencies)))
    return sum(value for _, value in _filtered)

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


def main():
    raw_data_path = Path().cwd() / "dataset" / "raw" / "all-colors.txt"
    color_palette_filepath = Path().cwd() / "dataset" / "all-colors.json"
    
    color_palette = extract_colors_to_defaultdict(raw_data_path)
    save_defaultdict_to_json(color_palette, color_palette_filepath)

    color_palette_filepath = Path().cwd() / "dataset" / "all-colors.json"
    color_palette = load_json_as_dict(color_palette_filepath)
    company_plette_size = map_dict_itemlist_to_itemlist_frequencies(color_palette)

    # Create barchart data
    barchart_data = defaultdict(int)
    for _, palette_size in company_plette_size.items():
        barchart_data[palette_size] += 1
    
    labels = list(barchart_data.keys())
    frequencies = list(barchart_data.values())
    labels, frequencies = zip(*sorted(zip(labels, frequencies)))
    plot_bar_chart(labels, frequencies)


if __name__ == "__main__":
    main()