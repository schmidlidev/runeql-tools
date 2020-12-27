import json
import os

from transformers import util


def translate_slayer_categories(categories):
    # The reason for this is that in our schema slayer category is an enum,
    # and object names in GraphQL cannot contain spaces
    return [category.replace(" ", "_") for category in categories]


def buildQuantity(quantity, monster):
    # monster param used purely for debug output

    if quantity is None:
        return None

    # * A very few number of monsters drop an item with a quantity type of both list and range,
    # * like "1-4,20". There's simply not a good way to parse this. It's also expected that
    # * over time, the wiki maintainers will flatten them out to multiple drop entries.
    # ! So for now we simply return None in these cases (Oh well :/)
    try:
        if "," in quantity:  # List
            quantities = [int(q) for q in quantity.split(",")]
            return {"__typename": "ItemDropQuantityList", "quantities": quantities}

        if "-" in quantity:  # Range
            _range = quantity.split("-")
            return {
                "__typename": "ItemDropQuantityRange",
                "min": int(_range[0]),
                "max": int(_range[1]),
            }

        return {"__typename": "ItemDropQuantityScalar", "quantity": int(quantity)}

    except:
        print(
            f" Drop quantity parsing error: [{monster['id']}] {monster['qualified_name']}"
        )
        return None


def transform(input_path, output_path):
    util.prepare_workspace(output_path)
    print("Transforming monsters")

    files = util.getFiles(input_path)
    bar = util.createProgressBar(len(util.getFilenames(input_path)))

    for (monster, filename) in files:
        bar.next()

        # Filter monsters
        if monster["duplicate"]:
            continue
        if not monster["wiki_name"]:
            continue

        # Translate
        monster["qualified_name"] = monster["wiki_name"]
        monster["attack_types"] = monster["attack_type"]

        # Transform
        if monster["slayer_monster"]:
            monster["slayer"] = {
                "masters": monster["slayer_masters"],
                "level": monster["slayer_level"],
                "xp": monster["slayer_xp"],
                "categories": translate_slayer_categories(monster["category"]),
            }

        monster["levels"] = {
            "combat": monster["combat_level"],
            "hitpoints": monster["hitpoints"],
            "attack": monster["attack_level"],
            "strength": monster["strength_level"],
            "defence": monster["defence_level"],
            "magic": monster["magic_level"],
            "ranged": monster["ranged_level"],
        }

        monster["bonuses"] = {
            "attack": {
                "melee": monster["attack_bonus"],
                "ranged": monster["attack_ranged"],
                "magic": monster["attack_magic"],
            },
            "defence": {
                "stab": monster["defence_stab"],
                "slash": monster["defence_slash"],
                "crush": monster["defence_crush"],
                "magic": monster["defence_magic"],
                "ranged": monster["defence_ranged"],
            },
            "strength": {
                "melee": monster["strength_bonus"],
                "ranged": monster["ranged_bonus"],
                "magic": monster["magic_bonus"],
            },
        }

        for drop in monster["drops"]:
            drop["quantity"] = buildQuantity(drop["quantity"], monster)
            del drop["name"]
            del drop["drop_requirements"]

        # Filter keys
        KEYS = [
            "id",
            "name",
            "qualified_name",
            "examine",
            "members",
            "release_date",
            "attributes",
            "size",
            "aggressive",
            "poisonous",
            "venomous",
            "immune_poison",
            "immune_venom",
            "max_hit",
            "attack_types",
            "attack_speed",
            "wiki_url",
            "slayer",
            "levels",
            "bonuses",
            "drops",
        ]
        # Keep only specified keys
        # Drop keys with None value
        monster = {key: monster[key] for key in KEYS if monster.get(key) is not None}

        util.writeFile(monster, os.path.join(output_path, filename))

    print(f"\nGenerated {len(util.getFilenames(output_path))} monsters")