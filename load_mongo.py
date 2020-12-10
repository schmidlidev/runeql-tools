import glob
import json

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


print("Connecting to mongodb")
client = MongoClient("mongodb://localhost:27017/")
db = client.osrs

upsert_many(glob.glob("transformed_items/*.json"), "items", "id")

print("\nCompleted.")