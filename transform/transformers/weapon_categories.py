import glob
import json
import os

from progress.bar import ChargingBar

from transformers import util


def getStances(weapon):
    stances = weapon.get("stances", [])

    for stance in stances:
        del stance["boosts"]

    return stances


def transform(input_path, output_path):
    util.prepare_workspace(output_path)
    print("Generating Weapon Categories")

    categories = {}

    files = glob.glob(os.path.join(input_path, "*.json"))
    bar = ChargingBar(max=len(files), suffix="[%(index)d/%(max)d] %(percent).1f%%")

    for filepath in files:
        bar.next()

        with open(filepath, "r") as f:
            item = json.load(f)

        weapon = item.get("weapon", None)
        if weapon is None:
            continue

        category = weapon["weapon_type"]
        if category not in categories:
            categories[category] = []

        categories[category].extend(getStances(weapon))

    for category in categories:
        stances = categories[category]
        categories[category] = [
            dict(t) for t in {tuple(sorted(stance.items())) for stance in stances}
        ]

        for stance in categories[category]:
            stance["name"] = stance.pop("combat_style")
            stance["type"] = stance.pop("attack_type")
            stance["style"] = stance.pop("attack_style")

            # Items missing Style, use Combat Style
            if stance["style"] is None:
                stance["style"] = stance["name"]

            # Items missing Attack Type, infer based on Experience
            if stance["type"] is None:
                if stance["experience"] and "ranged" in stance["experience"].lower():
                    stance["type"] = "ranged"
                if stance["experience"] and "magic" in stance["experience"].lower():
                    stance["type"] = "magic"

            del stance["experience"]

        weaponCategory = {"name": category, "stances": categories[category]}

        # Write files
        write_path = os.path.join(output_path, f"{weaponCategory['name']}.json")
        with open(write_path, "w") as f:
            f.write(json.dumps(weaponCategory))

    print(
        f"\nGenerated {len(glob.glob(os.path.join(output_path, '*.json')))} weapon categories"
    )
