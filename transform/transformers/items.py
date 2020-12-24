import os

from transformers import util

EXCLUDE_IDS = [617, 8890]  # Coins(Shilo Village)  # Coins(Mage Training Arena)


def build_requirements(requirements):
    if not requirements:
        return []

    new_requirements = []
    for key, value in requirements.items():
        new_requirements.append({"skill": key, "level": value})

    return new_requirements


def translate_slot(slot):
    if slot == "2h":
        return "twohanded"

    if slot == "shield":
        return "offhand"

    if slot == "ammo":
        return "ammunition"

    return slot


def transform(input_path, output_path):
    util.prepare_workspace(output_path)
    print("Transforming items")

    files = util.getFiles(input_path)
    bar = util.createProgressBar(len(util.getFilenames(input_path)))

    for (item, filename) in files:
        bar.next()

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
                "slot": translate_slot(item["equipment"]["slot"]),
                "requirements": build_requirements(item["equipment"]["requirements"]),
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
            "examine",
            "members",
            "release_date",
            "quest",
            "weight",
            "value",
            "alchemy",
            "tradeable",
            "stackable",
            "noteable",
            "equipable",
            "tradeable_ge",
            "buy_limit",
            "icon",
            "wiki_url",
            "equipment",
        ]
        # Keep only specified keys
        # Drop keys with None value
        item = {key: item[key] for key in KEYS if item.get(key) is not None}

        util.writeFile(item, os.path.join(output_path, filename))

    print(f"\nGenerated {len(util.getFilenames(output_path))} items")