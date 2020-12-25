#!/bin/sh
set -e  # if a command fails it stops the execution
set -u  # script fails if trying to access to an undefined variable

python /load_data/load_data.py --input $INPUT --mongo_uri $MONGO_URI