# Backwards-Compatibility Policy

`linkml-redcap` is an **import dependency**: other LinkML schemas (e.g.,
RareLink-CDM) `import` its schemas and reference their classes, slots, enums,
types and permissible values *by name*, and reference each schema by its
`id` URI. Downstream Python also imports `schema_path`, `schema_view`, and the
grouping helpers. All of that is public surface.

We treat this surface like a stable API.

## The rules

1. **Never change a schema `id`.**
   `https://w3id.org/linkml/redcap-data-dictionary` and
   `https://w3id.org/linkml/redcap-record` are permanent. Downstream `imports:`
   resolve against them.

2. **Never rename or remove a public element.**
   Classes, slots, enums, types and permissible-value *codes* are referenced by
   name. To retire one, keep it and mark it `deprecated: "<reason; use X>"`,
   then remove only in a major release.

3. **Additive minor releases only.**
   In a minor/patch you may add optional slots, new enums, new permissible
   values, new types, and new classes. You may **not**:
   - make an optional slot required,
   - remove or rename a permissible value,
   - tighten a `pattern` or narrow a `range`,
   - change a slot's `multivalued`/`inlined` shape.

4. **Breaking changes ⇒ major version bump**, and update the frozen sets in
   `tests/test_public_surface.py` in the same commit.

5. **The YAML travels with the install.** Schemas are shipped in the wheel and
   loaded via `importlib.resources`, so a pinned `linkml-redcap==X.Y.Z` always
   sees exactly the schema it was built against — downstream projects can pin a
   version and upgrade deliberately.

6. **Python API parity.** Every submodule exposes the same minimal loader API:
   `SCHEMA_FILENAME`, `schema_path() -> Path`, `schema_view() -> SchemaView`.

## What enforces this

`tests/test_public_surface.py` performs a **subset check**: every frozen name
must still be present. Adding elements passes; removing or renaming one fails CI.
That makes a breaking change impossible to do *by accident* — it can only happen
as a conscious edit to the frozen sets, which is the signal to bump major.

## Versioning

[SemVer](https://semver.org/). The schema `version:` field and the package
version move together. Pre-`1.0.0` we still follow the rules above; the only
difference is that the `0.x` line communicates "early, but disciplined".
