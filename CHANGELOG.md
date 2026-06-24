# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Because downstream schemas import this package, see
[`instructions/COMPATIBILITY.md`](instructions/COMPATIBILITY.md) for what counts
as a breaking change.

## [Unreleased]

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
