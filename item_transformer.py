import glob
import json
import os

from progress.bar import ChargingBar

EXCLUDE_IDS = [617, 8890]  # Coins(Shilo Village)  # Coins(Mage Training Arena)


def requirements_to_list(requirements):
    if not requirements:
        return None

    new_requirements = []
    for key, value in requirements.items():
        new_requirements.append({"skill": key, "level": value})

    return new_requirements


files = glob.glob("../osrsbox-db/docs/items-json/*.json")
progress_bar = ChargingBar(max=len(files), suffix="[%(index)d/%(max)d] %(percent).1f%%")
for filepath in files:
    progress_bar.next()

    with open(filepath, "r") as f:
        item = json.load(f)

    if item["id"] in EXCLUDE_IDS:
        continue
    if item["duplicate"] or item["noted"] or item["stacked"] or item["placeholder"]:
        continue

    # Translate
    item["value"] = item["cost"]
    item["quest"] = item["quest_item"]

    # Transform
    if item["highalch"] or item["lowalch"]:
        item["alchemy"] = {"high": item["highalch"], "low": item["lowalch"]}

    item["exchange"] = {
        "tradeable": item["tradeable_on_ge"],
    }
    if item["buy_limit"]:
        item["exchange"]["buy_limit"] = item["buy_limit"]
    if item["equipment"]:
        item["equipment"] = {
            "slot": item["equipment"]["slot"],
            "requirements": requirements_to_list(item["equipment"]["requirements"]),
            "bonuses": {
                "attack": {
                    "stab": item["equipment"]["attack_stab"],
                    "slash": item["equipment"]["attack_slash"],
                    "crush": item["equipment"]["attack_crush"],
                    "magic": item["equipment"]["attack_magic"],
                    "ranged": item["equipment"]["attack_ranged"],
                },
                "defence": {
                    "stab": item["equipment"]["defence_stab"],
                    "slash": item["equipment"]["defence_slash"],
                    "crush": item["equipment"]["defence_crush"],
                    "magic": item["equipment"]["defence_magic"],
                    "ranged": item["equipment"]["defence_ranged"],
                },
                "strength": {
                    "melee": item["equipment"]["melee_strength"],
                    "ranged": item["equipment"]["ranged_strength"],
                    "magic": item["equipment"]["magic_damage"],
                },
                "prayer": item["equipment"]["prayer"],
            },
        }

    if item["weapon"]:
        item["equipment"]["weapon"] = {
            "speed": item["weapon"]["attack_speed"],
            "category": {"name": item["weapon"]["weapon_type"]},
        }

    # Filter
    KEYS = [
        "id",
        "name",
        "members",
        "tradeable",
        "stackable",
        "noteable",
        "equipable",
        "value",
        "alchemy",
        "exchange",
        "weight",
        "quest",
        "release_date",
        "examine",
        "icon",
        "wiki_name",
        "wiki_url",
        "equipment",
    ]
    # Keep only specified keys
    # Drop keys with None value
    item = {key: item[key] for key in KEYS if item.get(key) is not None}

    write_path = f"transformed_items/{os.path.basename(filepath)}"
    # print(f"Writing {write_path}")
    with open(write_path, "w") as f:
        f.write(json.dumps(item))

print("Completed.")
