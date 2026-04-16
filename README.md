# linkml-redcap

LinkML schemas modelling REDCap structures. This package is the canonical
source of the meta-schema that formalises what a valid REDCap data dictionary looks like — field naming rules, the 18-column CSV structure, ontology-based annotation conventions, and the relationships between instruments, fields, and choices.

It's designed as an umbrella: `data_dictionary` is the first submodule, with room for additional submodules (`project`, `api`, etc.) as we formalise other REDCap structures.

## Install

```bash
pip install linkml-redcap
```

## Usage

```python
from linkml_redcap.data_dictionary import schema_path, schema_view

# Path to the bundled YAML (for LinkML CLI tools)
path = schema_path()

# Ready-to-use SchemaView (for programmatic introspection)
sv = schema_view()

assert "DataDictionary" in sv.all_classes()
assert "Field" in sv.all_classes()
assert "FieldType" in sv.all_enums()
```

The schema loads via `importlib.resources`, so it works from any install
location — regular filesystem installs, zipped wheels, or air-gapped
environments.

## What's in it

### `linkml_redcap.data_dictionary`

A LinkML schema formalising the structure of REDCap data dictionaries:

- **`DataDictionary`** — tree root, a complete DD
- **`Field`** — one CSV row, with all 18 REDCap columns as typed/constrained slots
- **`Choice`** — structured representation of a single permissible value
- **`OntologyAnnotation`** — the structured annotation block used by
  RareLink-style ontology-based instruments
- **`Instrument`** — logical grouping of contiguous fields sharing a `form_name`

Enums cover REDCap's native value spaces (`FieldType`, `TextValidationType`,
`CustomAlignment`, `IdentifierStatus`, `MatrixRanking`) plus ontology-related
extensions (`OntologyPrefix`, `BioPortalOntology`) for RareLink's variable
naming and annotation conventions.

Validated against the production RareLink-CDM v2.0.6 data dictionary
(108 fields, 11 instruments).

## Why this exists

REDCap data dictionaries are unstructured CSVs governed by implicit rules
documented in PDFs. Validating, generating, or transforming them
programmatically has historically meant hand-written parsers. This package
makes those rules machine-readable so downstream tools can:

- **Validate** any REDCap DD CSV against the meta-schema
- **Generate** REDCap DDs from higher-level specs (e.g., Excel + ontology codes)
- **Drive** runtime engines that route flat REDCap records into nested
  structures, without hard-coding per-instrument routing logic

## Ecosystem

- [**RareLink**](https://github.com/BIH-CEI/rarelink) — the REDCap-based
  framework for rare disease interoperability that motivated this schema
- [**rarelink-redcap-data-dictionary skill**](https://github.com/aslgraefe/rarelink-redcap-data-dictionary) —
  a Claude skill that uses this meta-schema to generate new
  RareLink-compatible instruments from domain-expert input
- [**rd-cdm**](https://pypi.org/project/rd-cdm/) — the rare disease common
  data model providing ontology code systems and versions

## Development

```bash
git clone https://github.com/aslgraefe/linkml-redcap
cd linkml-redcap
poetry install --with dev

# Validate the schema
poetry run linkml-lint src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml
poetry run gen-json-schema src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml > /dev/null

# Run tests
poetry run pytest
```

Releases are tag-triggered: push a `vX.Y.Z` tag matching the version in
`pyproject.toml` and GitHub Actions builds and publishes to PyPI via OIDC
trusted publishing.

## License

MIT