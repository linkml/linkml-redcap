# How consumer repos use linkml-redcap

This package defines **two REDCap serializations** of a record — `FlatRecord`
(the flat export row) and the generic `StructuredRecord` / `RepeatedElement` (the
lossless record-grouped form) — plus the lossless grouping between them. Consumer
repos build two kinds of conversion on top, both *anchored* on these classes.

> Scope boundary: `linkml-redcap` defines both serializations (`FlatRecord` and
> the generic, abstract `StructuredRecord` / `RepeatedElement`) plus the lossless
> grouping. The **typed instrument classes** that specialise them, the
> **transformation specs**, and the RareLink conventions (naming, annotation
> profile, Phenopacket/FHIR engine) live in the project / **rarelink**, layered
> on top. Nothing RareLink-specific is defined here.

## A project's flat schema

Every RareLink-based project specialises `FlatRecord`, giving each field a
*defined* range drawn from the typed primitives here (never bare `string` where
REDCap constrains the value, never `Any`):

```yaml
# myproject_flat.yaml
imports:
  - linkml:types
  - redcap_record                      # from linkml-redcap (record submodule)
classes:
  MyProjectFlatRecord:
    is_a: FlatRecord                    # inherits record_id + redcap_* structural slots
    slots: [snomedct_184099003, loinc_76689_9, disease_coding,
            rarelink_2_personal_information_complete, ...]
slots:
  snomedct_184099003: {range: redcap_date}
  loinc_76689_9:      {range: SexAtBirth}                 # project enum
  disease_coding:     {range: string}
  rarelink_2_personal_information_complete: {range: FormCompleteStatus}
```

That schema is the canonical, fully-typed description of the project's REDCap
flat export.

## A project's structured schema

The project's CDM root specialises `StructuredRecord`, and its repeat wrapper
specialises `RepeatedElement` — both imported from `linkml-redcap`, so the
structural envelope is defined once and only the *typed instrument classes* are
project-specific:

```yaml
# myproject_cdm.yaml
imports:
  - linkml:types
  - redcap_record                      # from linkml-redcap (record submodule)
classes:
  MyProjectRecord:
    is_a: StructuredRecord             # inherits record_id + repeated_elements
    tree_root: true
    slots: [personal_information]      # + the project's non-repeating instruments
    slot_usage:
      repeated_elements: {range: MyProjectRepeatedElement}
  MyProjectRepeatedElement:
    is_a: RepeatedElement              # inherits redcap_repeat_instrument/instance
    slots: [disease]                   # one slot per repeating instrument block
  PersonalInformation:                 # project-specific typed instrument class
    slots: [snomedct_184099003, loinc_76689_9]
  Disease:
    slots: [disease_coding]
```

## Use 1 — any tabular data → REDCap-flat format (linkml-map + SSSOM)

To bring external tabular data into the RareLink world, a project writes a
`linkml-map` `TransformationSpecification` from the source schema to
`MyProjectFlatRecord`, using **SSSOM** for the value-level term mappings (source
codes → the ontology codes REDCap expects). The target is well-typed because of
the schema above, so the mapping is checkable. The output is valid REDCap-flat
data ready to import or to feed Use 2.

## Use 2 — REDCap-flat → structured → Phenopackets / FHIR

```
flat REDCap export (list[dict])
   │  group_flat_records(..., drop_empty=True)   ← linkml_redcap.record.grouping (generic)
   ▼
grouped records (list[dict])      # record_id + flat fields + per-instrument repeats (untyped)
   │  linkml-map TransformationSpecification      ← rarelink / project (declarative)
   ▼
typed structured records          # StructuredRecord (linkml-redcap) + project instrument classes
   │  rarelink phenopackets engine (+ SSSOM for value→ontology mappings)
   ▼
GA4GH Phenopackets / HL7 FHIR
```

### Why grouping is a separate, generic step

`linkml-map` transforms **object → object**. Flat → structured is a **cardinality
change** (many flat rows fold into one record, repeats fanning out into a list),
which `linkml-map` cannot express. `group_flat_records` does exactly and only
that, depending solely on REDCap-native fields (`record_id`,
`redcap_repeat_instrument`, `redcap_repeat_instance`) — so it is identical for
every project and lives here as a generic helper. Its output is a
`StructuredRecord`-shaped dict (untyped at the field level); the *typed instrument
classes* that give those fields meaning are the project's.

It is also the **scale answer**: the flat export is *wide* (every row carries all
columns, mostly empty), so for 1000+ records it is the heavy artifact.
`group_flat_records(..., drop_empty=True)` collapses it to compact per-record
objects, and because each grouped record is independent you can map
record-by-record with bounded memory. Group first, then map.

```python
import json
from linkml_redcap.record import group_flat_records

flat = json.load(open("export.json"))
grouped = group_flat_records(flat, drop_empty=True)   # generic structural step
json.dump(grouped, open("grouped.json", "w"))
# then (in rarelink/project): linkml-map run --source-schema myproject_flat.yaml \
#                                            --target-schema myproject_cdm.yaml \
#                                            --transformer-specification flat_to_cdm.transform.yaml \
#                                            grouped.json
```

## Annotation profile (lives in rarelink, noted here for orientation)

rarelink's schema-driven generators read slot/class annotations. The
`linkml-redcap` enums/types are reused as their value spaces where applicable:

| annotation | meaning | value space |
|------------|---------|-------------|
| `redcap_form` | instrument machine name | string |
| `redcap_field_type` | REDCap field type | `redcap_dd:FieldType` |
| `redcap_validation` | text validation | `redcap_dd:TextValidationType` |
| `fhir_expression` | HL7 FHIR R4 path | string |
| `phenopacket_element` | GA4GH Phenopacket v2 element | string |

Standardising these annotation tags is rarelink's responsibility; they are listed
here only so the flat and structured schemas above make sense.
