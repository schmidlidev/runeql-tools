#!/bin/sh
set -e  # if a command fails it stops the execution
set -u  # script fails if trying to access to an undefined variable

timestamp=`date +%Y-%m-%d_%H:%M:%S`

cd /transform

git config --global user.email "schmidlidev@gmail.com"
git config --global user.name "schmidlidev"

git clone --single-branch --branch update --depth 1 https://github.com/schmidlidev/runeql-data.git
git clone --single-branch --branch master --depth 1 https://github.com/schmidlidev/osrsbox-db.git 

echo "Executing data transformer"
python /transform/item_transformer.py

echo "Committing data to runeql-data"
cd /transform/runeql-data/
git remote set-url origin https://schmidlidev:${RUNEQL_DATA_LOAD}@github.com/schmidlidev/runeql-data.git
git add .
git status
git commit -m "Data Update ${timestamp}"
git push --set-upstream origin testbranch