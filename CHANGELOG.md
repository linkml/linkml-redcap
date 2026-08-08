# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Because downstream schemas import this package, see
[`instructions/COMPATIBILITY.md`](instructions/COMPATIBILITY.md) for what counts
as a breaking change.

## [Unreleased]

## [0.1.2] - 2026-08-08

### Added

- **`record.checkbox`** — lossless, vendor-neutral bridge between REDCap's flat
  checkbox export columns (`<field>___<code>` holding `"1"`/`"0"`) and the
  semantic multivalued-slot shape (`field: ["1", "2"]`) a LinkML project schema
  declares:
  - `collapse_checkboxes(record, checkbox_map)` — flat columns → list of
    checked option codes; descends into `repeated_elements` and arbitrary
    nesting, so it composes directly with `group_flat_records`;
  - `expand_checkboxes(record, checkbox_map)` — the full-width inverse (every
    option column emitted), producing exactly the shape `ungroup_records`
    accepts for a REDCap import file; raises on undeclared codes instead of
    dropping them;
  - `infer_checkbox_map(columns)` — recover `{field: [codes]}` from the export
    columns themselves;
  - `checkbox_map_from_data_dictionary(rows)` — build the authoritative map
    from data dictionary rows (both the 18 CSV headers and the snake_case
    schema aliases are accepted);
  - `checkbox_column(field, code)` — reproduces REDCap's column-name
    sanitisation (lower-case; non-`[a-z0-9_]` → `_`, so option code `-2`
    becomes `field____2`), keeping signed/alphanumeric codes round-trippable.
  All exported from `linkml_redcap.record`.

### Notes

- Purely additive; no schema element changed. The `CheckboxState` enum already
  documented the per-column value space — this release adds the structural
  conversion that was previously left to each consuming project (rarelink,
  tir-charite).

## [0.1.1] - 2026-08-01

### Added

- `importmap()` / `write_importmap()` and the `linkml-redcap-importmap` console
  script, so a downstream schema can resolve its `imports:` from the installed
  package instead of copying the schema YAML into its own tree. Use
  `SchemaView(path, importmap=importmap())` in Python, or
  `linkml-redcap-importmap importmap.json` followed by
  `gen-project --importmap importmap.json ...` for the LinkML CLI generators.

### Changed

- Documentation now shows the **canonical URI** import form
  (`https://w3id.org/linkml/redcap-record`) rather than the bare name
  `redcap_record`. A bare import cannot resolve from a schema in a subdirectory:
  linkml-runtime's `imports_closure()` rewrites it relative to the importing file
  (`if "/" in sn and ":" not in i`), so it never reaches the importmap. Imports
  containing `:` are exempt. Bare names remain mapped for schemas that sit next to
  the import root.

### Notes

- No schema element changed, so the compatibility surface in
  `instructions/COMPATIBILITY.md` is untouched.

## [0.1.0] - 2026-06-24

Initial release.

### Added

- **`data_dictionary` submodule** — a LinkML meta-schema for the REDCap data
  dictionary (18-column CSV): classes `DataDictionary`, `Field`, `Choice`,
  `Instrument`; enums `FieldType`, `TextValidationType` (incl. the comma-decimal
  and seconds variants), `CustomAlignment`, `IdentifierStatus`, `MatrixRanking`.
- **`record` submodule** — a LinkML schema for REDCap record data in both
  serializations:
  - `FlatRecord` (abstract) — the flat export row;
  - `StructuredRecord` / `RepeatedElement` (abstract, generic, lossless) — the
    record-grouped form of REDCap's own record-and-repeats model;
  - structural slots (`record_id`, `redcap_event_name`,
    `redcap_repeat_instrument`, `redcap_repeat_instance`,
    `redcap_data_access_group`, `redcap_survey_identifier`, `repeated_elements`);
  - universal value-space enums (`FormCompleteStatus`, `YesNo`, `TrueFalse`,
    `CheckboxState`);
  - typed REDCap primitives (`redcap_date`, `redcap_datetime`, `redcap_time`,
    `redcap_integer`, `redcap_number`, `redcap_email`).
- **`record.grouping`** — generic, dependency-free flat ⇄ structured grouping
  helper (`group_flat_records` / `ungroup_records`).
- Loader API (`schema_path`, `schema_view`) for both submodules, resolving
  schemas via `importlib.resources`.
- Backwards-compatibility guard (`tests/test_public_surface.py`) that fails CI if
  a frozen public schema name disappears.
- Project hygiene: pre-commit (ruff, yamllint, codespell, typos), Dependabot
  (GitHub Actions + Python), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and the
  design/compatibility/mapping docs under `instructions/`.

[Unreleased]: https://github.com/linkml/linkml-redcap/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/linkml/linkml-redcap/releases/tag/v0.1.0
