import glob
import json
import os
from pathlib import Path

import argparse
from progress.bar import ChargingBar
from pymongo import MongoClient


def upsert_many(files, collection, identity_key):
    print(f"Upserting data for collection {collection}")
    bar = ChargingBar(max=len(files), suffix="[%(index)d/%(max)d] %(percent).1f%%")

    for filepath in files:
        bar.next()
        with open(filepath, "r") as f:
            document = json.load(f)

        db[collection].replace_one(
            {identity_key: document[identity_key]}, document, upsert=True
        )
    bar.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mongo_uri",
        help="MongoDB URI",
        default="mongodb://localhost:27017/",
    )
    parser.add_argument(
        "--input", help="Directory of data to upload", default="./runeql-data"
    )
    parser.add_argument(
        "--collection", help="Name of a single collection to load", default="all"
    )
    args = parser.parse_args()

    print("Connecting to mongodb")
    client = MongoClient(args.mongo_uri)
    db = client["osrs"]

    # Monsters
    if args.collection == "monsters" or args.collection == "all":
        files = glob.glob(os.path.join(Path(args.input), "monsters/*.json"))
        upsert_many(files, "monsters", "id")

    # Weapon Categories
    if args.collection == "weaponCategories" or args.collection == "all":
        files = glob.glob(os.path.join(Path(args.input), "weaponCategories/*.json"))
        upsert_many(files, "weaponCategories", "name")

    # Items
    if args.collection == "items" or args.collection == "all":
        files = glob.glob(os.path.join(Path(args.input), "items/*.json"))
        upsert_many(files, "items", "id")

    client.close()
    print("Completed.")
