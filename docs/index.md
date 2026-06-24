# linkml-redcap

LinkML schemas modelling **REDCap** structures — vendor-neutral, fully typed, and
backwards-compatible — for use as the canonical substrate in schema-driven
conversion pipelines.

The package ships two schemas plus small loaders:

- **Data dictionary** (`linkml_redcap.data_dictionary`) — a meta-schema for the
  REDCap data dictionary (the 18-column CSV that *describes* a project).
- **Record** (`linkml_redcap.record`) — the REDCap record data itself, in both
  serializations REDCap's data uses: `FlatRecord` (the flat export row) and the
  generic, lossless `StructuredRecord` / `RepeatedElement` (the record-grouped
  form), plus a dependency-free `grouping` helper for the flat ⇄ structured step.

It models **REDCap itself** — nothing project- or RareLink-specific. The RareLink
ontology conventions and the Phenopacket/FHIR engine live in
[rarelink](https://github.com/BIH-CEI/rarelink), layered on top.

## Where to go next

- **Schema reference** — auto-generated, browsable pages for every class, slot,
  enum and type in each schema (regenerated from the schema on every release, so
  it never goes stale).
- **[Design decisions](design-decisions.md)** — what the package is, the scope
  boundary, and why each choice was made.
- **[Mapping workflow](mapping-workflow.md)** — how consumer repos use this:
  tabular → REDCap-flat (linkml-map + SSSOM), and REDCap-flat → Phenopackets.
- **[Compatibility](compatibility.md)** — the backwards-compatibility policy for
  downstream schemas that import this one.

## Install

```bash
pip install linkml-redcap
```

```python
from linkml_redcap.record import schema_view, group_flat_records
from linkml_redcap.data_dictionary import schema_view as dd_view

sv = schema_view()          # SchemaView over the record schema
print(sorted(sv.all_classes()))
```
