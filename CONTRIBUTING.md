# Contributing to linkml-redcap

Thanks for your interest in contributing! `linkml-redcap` provides the
vendor-neutral LinkML schemas that model REDCap data dictionaries and REDCap
record data (flat + structured). Because downstream projects (RareLink, cieinr,
and others) import these schemas, contributions are reviewed with an emphasis on
**stability** and **staying true to REDCap** (nothing project-specific belongs
here — see `instructions/DESIGN_DECISIONS.md`).

## Ways to contribute

- Report a bug or request a change by opening an issue.
- Improve documentation in `README.md` or `instructions/`.
- Propose schema changes (new REDCap value spaces, validation types, etc.),
  keeping the backwards-compatibility policy below in mind.

## Development setup

This project uses [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/linkml/linkml-redcap
cd linkml-redcap
poetry install --with dev
```

### Pre-commit hooks

We use [pre-commit](https://pre-commit.com/) (ruff, yamllint, codespell, typos,
and basic file hygiene). Install the hooks once:

```bash
poetry run pre-commit install
```

They then run automatically on every commit. To run them across the whole repo:

```bash
poetry run pre-commit run --all-files
```

### Validate the schemas

Both schemas must lint and generate cleanly:

```bash
poetry run linkml-lint --ignore-warnings \
  src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml
poetry run linkml-lint --ignore-warnings \
  src/linkml_redcap/record/schema/redcap_record.yaml
```

`--ignore-warnings` is intentional: REDCap's numeric/uppercase permissible-value
names (e.g. `0`/`1`/`2`) trip the `standard_naming` style rule but must equal
REDCap's stored values, so the warnings are expected. Lint **errors** still fail.

### Run the tests

```bash
poetry run pytest
```

`tests/test_public_surface.py` is a backwards-compatibility guard — see below.

## Backwards-compatibility policy

This package is an import dependency, so its schema `id`s and public
class/slot/enum/type/permissible-value **names** are treated as a stable API:

- **Additive minor releases only** — add new optional slots / enums / values.
- **Deprecate, don't remove** — mark old elements `deprecated:` instead of
  deleting or renaming them.
- **Breaking changes require a major version bump.**

`tests/test_public_surface.py` fails CI if a frozen public name disappears, so a
break can only happen as a conscious edit. Full policy in
`instructions/COMPATIBILITY.md`.

## Pull requests

1. Create a branch off `main`.
2. Make focused, minimal changes; update docs and tests alongside code.
3. Ensure `pre-commit`, both `linkml-lint` runs, and `pytest` pass locally.
4. Open a PR against `main`. CI must be green, and `main` is protected (a review
   approval is required before merge).
5. For schema changes, note in the PR whether the change is additive (minor) or
   breaking (major), and update `CHANGELOG.md`.

## Releases

Releases are tag-triggered: pushing a `vX.Y.Z` tag that matches the version in
`pyproject.toml` builds and publishes to PyPI via OIDC trusted publishing.

## Code of conduct

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
