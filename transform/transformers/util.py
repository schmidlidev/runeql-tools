import glob
import json
import os
from pathlib import Path
import shutil

from progress.bar import ChargingBar


def prepare_workspace(path):
    # Creates an empty directory
    # If a directory already exists, clear its contents

    print(f"Preparing workspace {path}")
    Path.mkdir(
        Path(path), exist_ok=True
    )  # Prevents shutil.rmtree from failing if the directory doesn't exist
    shutil.rmtree(path)
    Path.mkdir(Path(path))


def getFilenames(path):
    return glob.glob(os.path.join(path, "*.json"))


def createProgressBar(length):
    return ChargingBar(max=length, suffix="[%(index)d/%(max)d] %(percent).1f%%")


def writeFile(dict, path):
    with open(path, "w") as f:
        f.write(json.dumps(dict))


def getFiles(path):
    for filepath in getFilenames(path):
        with open(filepath, "r") as f:
            yield (json.load(f), os.path.basename(filepath))