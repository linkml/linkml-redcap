# Example: Generating a Disease-Specific REDCap Instrument

## Input: Domain Expert Specification

A clinician working on an immunodeficiency registry provides this table:

| Ontology Code     | Label                        | Field Type | Choices Ontology | Notes                           |
|-------------------|------------------------------|------------|------------------|---------------------------------|
| HP:0002719        | Recurrent infections         | dropdown   | SNOMEDCT         | onset date, severity needed     |
| HP:0004313        | Decreased IgG                | text       | BIOPORTAL:LOINC  | numeric value + unit            |
| HP:0002960        | Autoimmunity                 | dropdown   | SNOMEDCT         | link to specific autoimmune dx  |
| MONDO:0018038     | Primary immunodeficiency     | text       | BIOPORTAL:MONDO  | main disease code               |
| LOINC:26464-8     | Leukocytes [#/volume]        | text       | -                | numeric, unit = 10*3/uL         |

## Generated Output 1: REDCap Data Dictionary CSV

```csv
Variable / Field Name,Form Name,Section Header,Field Type,Field Label,Choices Calculations OR Slider Labels,Field Note,Text Validation Type OR Show Slider Number,Text Validation Min,Text Validation Max,Identifier?,Branching Logic,Required Field?,Custom Alignment,Question Number,Matrix Group Name,Matrix Ranking?,Field Annotation
hp_0002719,cieinr_immunophenotype,,dropdown,1.1 Recurrent infections,"snomedct_373066001, Yes - present | snomedct_373067005, No - absent | snomedct_261665006, Unknown",Select whether this phenotypic feature is observed,,,,,,y,,,,,"Variable:
HP:0002719 | Recurrent infections |
Choices:
- SNOMED:373066001 | Yes
- SNOMED:373067005 | No
- SNOMED:261665006 | Unknown
Version(s):
- HP 2026-02-16
- SNOMED CT 2025AB
Mapping:
- GA4GH Phenopacket Schema v2.0 Element: PhenotypicFeature.type
- HL7 FHIR Expression v4.0.1: Observation.code"
hp_0002719_onset,cieinr_immunophenotype,,text,1.1.1 Onset date,,Date of first observation of recurrent infections,date_ymd,,,,[hp_0002719] = 'snomedct_373066001',,,,,,"Variable:
HP:0002719 | Recurrent infections - Onset |
Choices: n/a
Version(s):
- HP 2026-02-16
Mapping:
- GA4GH Phenopacket Schema v2.0 Element: PhenotypicFeature.onset
- HL7 FHIR Expression v4.0.1: Observation.effectiveDateTime"
hp_0004313,cieinr_immunophenotype,,text,1.2 Decreased IgG in blood,BIOPORTAL:LOINC,Search for the specific LOINC code,,,,,,,,,,,
mondo_0018038,cieinr_disease,,text,2.1 Primary immunodeficiency disorder,BIOPORTAL:MONDO,Search and select the specific MONDO disease code,,,,,,,,,,,
loinc_26464_8,cieinr_measurements,,text,3.1 Leukocytes [#/volume],,White blood cell count,number,0,,,,y,,,,,"Variable:
LOINC:26464-8 | Leukocytes [#/volume] in Blood |
Choices: n/a
Version(s):
- LOINC 281
Mapping:
- GA4GH Phenopacket Schema v2.0 Element: Measurement.value
- HL7 FHIR Expression v4.0.1: Observation.valueQuantity"
```

## Generated Output 2: LinkML Instrument Schema

```yaml
id: https://example.org/cieinr_immunophenotype
name: cieinr_immunophenotype
prefixes:
  linkml: https://w3id.org/linkml/
  cieinr: https://example.org/cieinr/
  HP: http://purl.obolibrary.org/obo/HP_
  SNOMEDCT: http://snomed.info/sct/
imports:
  - linkml:types
  - rarelink_code_systems
default_range: string
default_prefix: cieinr

classes:
  Immunophenotype:
    description: >-
      CIEINR immunophenotype instrument for capturing immunodeficiency-
      related phenotypic features.
    slots:
      - hp_0002719
      - hp_0002719_onset
      - hp_0004313

slots:
  hp_0002719:
    title: "1.1 Recurrent infections"
    description: Whether recurrent infections are observed
    range: PresentAbsentUnknown
    required: true
  hp_0002719_onset:
    title: "1.1.1 Onset date"
    description: Date of first observation of recurrent infections
    range: date
    required: false
  hp_0004313:
    title: "1.2 Decreased IgG in blood"
    description: Decreased circulating IgG level
    range: string
    required: false

enums:
  PresentAbsentUnknown:
    permissible_values:
      snomedct_373066001:
        description: "Yes - present"
        meaning: SNOMEDCT:373066001
      snomedct_373067005:
        description: "No - absent"
        meaning: SNOMEDCT:373067005
      snomedct_261665006:
        description: Unknown
        meaning: SNOMEDCT:261665006
```

## Generated Output 3: Phenopacket Mapping Config

```yaml
# mapping_config for cieinr_immunophenotype
instrument: cieinr_immunophenotype
phenopacket_block: phenotypic_features
mappings:
  hp_0002719:
    target: PhenotypicFeature.type
    ontology: HP
    code_field: hp_0002719
    onset_field: hp_0002719_onset
    status_mapping:
      snomedct_373066001: true    # present → excluded=false
      snomedct_373067005: false   # absent  → excluded=true
```

## What the Meta-Schema Validates

Before any of these artifacts are produced, the meta-schema ensures:

1. **Variable names** conform to `^[a-z][a-z0-9_]*$`
2. **Form names** are lowercase with underscores only
3. **Field types** are valid REDCap types (dropdown, text, radio, etc.)
4. **Choice encoding** follows `raw_value, Label` pipe-delimited format
5. **Date fields** use a valid REDCap text-validation type (e.g. `date_ymd`)
6. **Branching logic** references existing variable names
7. **Required fields** carry a valid `y` flag

> Note: the *ontology* conventions an immunodeficiency example like this relies on
> — the `snomedct_…` / `hp_…` variable-prefix convention, the structured
> `field_annotation` grammar (Variable / Choices / Versions / Mapping), and
> BioPortal ontology references — are **RareLink rules, not REDCap facts**, and
> are therefore **not** validated by `linkml-redcap` (see DESIGN_DECISIONS §10).
> They are validated by the RareLink layer that owns those conventions. This file
> shows them only to illustrate the end-to-end RareLink workflow the REDCap base
> feeds into.
