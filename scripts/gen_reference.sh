#!/usr/bin/env bash
# Regenerate the browsable LinkML schema reference consumed by mkdocs.
# Output (docs/reference/) is git-ignored and rebuilt from the schemas every time,
# so it never goes stale. Run this before `mkdocs serve` / `mkdocs build`.
set -euo pipefail

cd "$(dirname "$0")/.."

REC="src/linkml_redcap/record/schema/redcap_record.yaml"
DD="src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml"

rm -rf docs/reference
mkdir -p docs/reference/record docs/reference/data_dictionary

echo "Generating record schema reference..."
poetry run gen-doc --directory docs/reference/record "$REC"

echo "Generating data dictionary schema reference..."
poetry run gen-doc --directory docs/reference/data_dictionary "$DD"

echo "Schema reference written to docs/reference/"
