import argparse
import os
from pathlib import Path

from transformers import items
from transformers import weapon_categories

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", help="Directory of item data to transform", required=True
    )
    parser.add_argument(
        "--output",
        help="Output directory to dump transformed data",
        default="./runeql-data/",
    )
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    Path.mkdir(Path(output_path), exist_ok=True)

    weapon_categories.transform(
        os.path.join(input_path, "items-json/"),
        os.path.join(output_path, "weaponCategories/"),
    )
    items.transform(
        os.path.join(input_path, "items-json/"),
        os.path.join(output_path, "items/"),
    )

    print("Completed.")
