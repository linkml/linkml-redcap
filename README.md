# linkml-redcap

[![CI](https://github.com/linkml/linkml-redcap/actions/workflows/ci.yaml/badge.svg)](https://github.com/linkml/linkml-redcap/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/linkml-redcap.svg)](https://badge.fury.io/py/linkml-redcap)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://linkml.github.io/linkml-redcap)

LinkML schemas modelling **REDCap structures**. This package is the canonical,
vendor-neutral source of the REDCap primitives that downstream projects build
on — what a valid data dictionary looks like, and what record data looks like in
both its flat and structured shapes. You can find more information in the [documentation](https://linkml.github.io/linkml-redcap).

It is an umbrella with two submodules:

- **`data_dictionary`** — the meta-schema that formalises a REDCap *data
  dictionary*: the 18-column CSV structure, field-naming rules, field/validation
  types, and matrix groups.
- **`record`** — a reusable envelope for REDCap *record data*: the structural
  fields REDCap adds to every export (`record_id`, `redcap_event_name`,
  `redcap_repeat_instrument`, `redcap_repeat_instance`, ...), the universal
  `*_complete` / yes-no / true-false / checkbox value spaces, the REDCap
  date/time string types, and the `RepeatedElement` wrapper — plus the generic
  flat ⇄ structured grouping step.

It contains **no project-specific or RareLink-specific rules**. Those conventions
(variable naming, instrument naming, annotation profile) live in
[RareLink](https://github.com/BIH-CEI/rarelink) and are layered on top of these
primitives. Contributions and collaboration are welcome.

## Install

```bash
pip install linkml-redcap
```

## Usage

```python
# --- the data dictionary meta-schema ---
from linkml_redcap.data_dictionary import schema_view as dd_view
sv = dd_view()
assert "Field" in sv.all_classes()
assert "FieldType" in sv.all_enums()

# --- the record-data envelope ---
from linkml_redcap.record import schema_view as record_view, group_flat_records
rv = record_view()
assert "FlatRecord" in rv.all_classes()
assert "StructuredRecord" in rv.all_classes()
assert "FormCompleteStatus" in rv.all_enums()

# group a flat REDCap export into per-record objects (generic structural step)
grouped = group_flat_records(flat_rows, drop_empty=True)
```

Each submodule exposes the same loader API — `schema_path() -> Path` (for LinkML
CLI tools) and `schema_view() -> SchemaView` (for introspection). Schemas load
via `importlib.resources`, so they work from any install location — regular
installs, zipped wheels, or air-gapped environments.

## What's in it

### `linkml_redcap.data_dictionary`

A LinkML meta-schema for the REDCap data dictionary CSV:

- **`DataDictionary`** — tree root, a complete DD
- **`Field`** — one CSV row, all 18 REDCap columns as typed/constrained slots
- **`Choice`** — structured representation of one permissible value
- **`Instrument`** — logical grouping of contiguous fields sharing a `form_name`

Enums cover REDCap's native value spaces (`FieldType`, `TextValidationType`
incl. the European comma-decimal variants, `CustomAlignment`, `IdentifierStatus`,
`MatrixRanking`).

> This schema is **vendor-neutral REDCap only**. RareLink ontology conventions —
> variable-name prefixes (`snomedct_…`), the structured `field_annotation`
> grammar, and BioPortal/ontology curation — are **not** defined here; they live
> in [rarelink](https://github.com/BIH-CEI/rarelink).

### `linkml_redcap.record`

The single source of truth for the **REDCap record representation** — the actual
shape of REDCap record data, in the two serializations the data uses:

- **`FlatRecord`** (abstract) — one flat-export row; a project specialises it via
  `is_a: FlatRecord` and adds one typed slot per field variable.
- **`StructuredRecord`** (abstract) — the lossless record-grouped serialization:
  one object per `record_id` with its repeating-instrument instances nested. A
  project specialises it (`is_a`), marks itself `tree_root`, and adds its typed
  non-repeating instrument slots.
- **`RepeatedElement`** — the `(redcap_repeat_instrument, redcap_repeat_instance)`
  wrapper for one repeating-instrument instance. The canonical version of the
  class rarelink and cieinr currently redeclare per repo — import this one.
- Structural slots: `record_id`, `redcap_event_name`, `redcap_repeat_instrument`,
  `redcap_repeat_instance`, `redcap_data_access_group`,
  `redcap_survey_identifier`, `repeated_elements`.
- Enums **`FormCompleteStatus`** (0/1/2), **`YesNo`**, **`TrueFalse`**,
  **`CheckboxState`** — REDCap's universal value spaces.
- Types **`redcap_date`** / **`redcap_datetime`** / **`redcap_time`** /
  **`redcap_integer`** / **`redcap_number`** / **`redcap_email`** — one typed
  primitive per REDCap value space, so a project can give every field a defined
  range (never a bare `string` where REDCap constrains the value, never `Any`).
- `grouping.group_flat_records` / `ungroup_records` — the lossless flat ⇄
  structured conversion (the cardinality change `linkml-map` can't express),
  depending only on REDCap-native fields.

> The structured envelope here is deliberately **generic, abstract and
> convention-free** — REDCap's own record-and-repeats model, serialized
> hierarchically. It defines **no** typed instrument classes, variable-naming
> rules, or ontology/Phenopacket mappings: that *semantic* layer is the
> consuming project's (the instrument classes that specialise these) and
> [rarelink](https://github.com/BIH-CEI/rarelink)'s (the conventions and the
> Phenopacket/FHIR engine). Nothing RareLink-specific is defined here.

See [`instructions/MAPPING_WORKFLOW.md`](instructions/MAPPING_WORKFLOW.md) for the
full flat → grouped → structured pipeline and how it feeds Phenopacket/FHIR export.

## Why this exists

REDCap data dictionaries are unstructured CSVs governed by implicit rules, and
REDCap record exports are flat and wide. Making both machine-readable lets
downstream tools **validate** any DD or export, **generate** DDs from higher-level
specs, and **transform** flat exports into structured models with `linkml-map`
instead of hand-written, per-instrument Python — the same envelope serving
RareLink-CDM, the MII KDS-SE editions, CIEINR, and any other RareLink-based model.

## Backwards compatibility

This package is an import dependency, so its schema `id`s and public
class/slot/enum/type names are treated as a stable API: additive minor releases
only, deprecate-don't-remove, breaking changes ⇒ major bump. The policy is in
[`instructions/COMPATIBILITY.md`](instructions/COMPATIBILITY.md) and enforced by
`tests/test_public_surface.py`, which fails CI if any public name disappears.

## Ecosystem

- [**RareLink**](https://github.com/BIH-CEI/rarelink) — the REDCap-based rare
  disease interoperability framework that defines the rules built on these
  primitives
- [**rd-cdm**](https://pypi.org/project/rd-cdm/) — ontology code systems & versions

## Development

```bash
git clone https://github.com/linkml/linkml-redcap
cd linkml-redcap
poetry install --with dev

# Validate the schemas
poetry run linkml-lint src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml
poetry run linkml-lint src/linkml_redcap/record/schema/redcap_record.yaml

# Run tests
poetry run pytest
```

Releases are tag-triggered: push a `vX.Y.Z` tag matching the version in
`pyproject.toml` and GitHub Actions builds and publishes to PyPI via OIDC
trusted publishing.

## License

MIT
