import glob
import json
import os
import shutil
import sys

from progress.bar import ChargingBar

from transformers import util

EXCLUDE_IDS = [617, 8890]  # Coins(Shilo Village)  # Coins(Mage Training Arena)


def requirements_to_list(requirements):
    if not requirements:
        return []

    new_requirements = []
    for key, value in requirements.items():
        new_requirements.append({"skill": key, "level": value})

    return new_requirements


def getCategory(item):
    weapon = item.get("weapon", {})
    # type = weapon["weapon_type"]
    stances = weapon.get("stances", [])

    for stance in stances:
        del stance["experience"]
        del stance["boosts"]

    return {"name": weapon["weapon_type"], "stances": stances}


def transform(input_path, output_path):
    util.prepare_workspace(output_path)
    print("Transforming items")

    files = glob.glob(os.path.join(input_path, "*.json"))
    progress_bar = ChargingBar(
        max=len(files), suffix="[%(index)d/%(max)d] %(percent).1f%%"
    )

    for filepath in files:
        progress_bar.next()

        with open(filepath, "r") as f:
            item = json.load(f)

        # Filter out 'fake' items
        if item["id"] in EXCLUDE_IDS:
            continue
        if item["duplicate"] or item["noted"] or item["stacked"] or item["placeholder"]:
            continue
        if not item["wiki_name"]:
            continue

        # Translate
        item["value"] = item["cost"]
        item["quest"] = item["quest_item"]
        item["tradeable_ge"] = item["tradeable_on_ge"]
        item["qualified_name"] = item["wiki_name"]

        # Transform
        if item["highalch"] or item["lowalch"]:
            item["alchemy"] = {"high": item["highalch"], "low": item["lowalch"]}

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
            "qualified_name",
            "members",
            "tradeable",
            "stackable",
            "noteable",
            "equipable",
            "value",
            "alchemy",
            "tradeable_ge",
            "buy_limit",
            "weight",
            "quest",
            "release_date",
            "examine",
            "icon",
            "wiki_url",
            "equipment",
        ]
        # Keep only specified keys
        # Drop keys with None value
        item = {key: item[key] for key in KEYS if item.get(key) is not None}

        write_path = os.path.join(output_path, os.path.basename(filepath))
        with open(write_path, "w") as f:
            f.write(json.dumps(item))

    print(f"\nGenerated {len(glob.glob(os.path.join(output_path, '*.json')))} items")