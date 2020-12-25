# runeql-tools

Tools to support [RuneQL](https://github.com/schmidlidev/runeql)

## Tools

### Transform

Python tool and GitHub Action that transforms the shape of [OSRSBox](https://github.com/osrsbox/osrsbox-db) data to the shape of the [RuneQL schemas](https://www.runeql.com/schema/).

### Auto PR

Javascript GitHub Action used for automatically opening a pull request in [runeql-data](https://github.com/schmidlidev/runeql-data) when new data has been updated.

### Load Data

Python tool that upserts the output data of Transform to the RuneQL database.
