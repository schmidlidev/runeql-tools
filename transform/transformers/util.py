from pathlib import Path
import shutil


def prepare_workspace(path):
    # Creates an empty directory
    # If a directory already exists, clear its contents

    print(f"Preparing workspace {path}")
    Path.mkdir(
        Path(path), exist_ok=True
    )  # Prevents shutil.rmtree from failing if the directory doesn't exist
    shutil.rmtree(path)
    Path.mkdir(Path(path))
