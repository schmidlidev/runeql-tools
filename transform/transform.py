import argparse
import os
from pathlib import Path

from transformers import items
from transformers import monsters
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
    parser.add_argument(
        "--collection", help="Name of a single collection to transform", default="all"
    )
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    collection = args.collection

    Path.mkdir(Path(output_path), exist_ok=True)

    if collection == "items" or collection == "all":
        items.transform(
            os.path.join(input_path, "items-json/"),
            os.path.join(output_path, "items/"),
        )
    if collection == "weaponCategories" or collection == "all":
        weapon_categories.transform(
            os.path.join(input_path, "items-json/"),
            os.path.join(output_path, "weaponCategories/"),
        )
    if collection == "monsters" or collection == "all":
        monsters.transform(
            os.path.join(input_path, "monsters-json/"),
            os.path.join(output_path, "monsters/"),
        )

    print("Completed.")
