# Project Structure & Relationship to RareLink

## Repository: `redcap-data-dictionary`

Based on `linkml-project-copier`, the project would be structured as:

```
redcap-data-dictionary/
├── project/
│   └── redcap_data_dictionary.yaml          # Core meta-schema (REDCap rules)
│
├── src/
│   └── redcap_data_dictionary/
│       ├── datamodel/                        # Generated Python classes
│       │   ├── redcap_data_dictionary.py     # Dataclasses (gen-python)
│       │   └── redcap_data_dictionary_pydantic.py  # Pydantic models
│       ├── generators/
│       │   ├── csv_generator.py              # LinkML instance → REDCap DD CSV
│       │   └── linkml_generator.py           # Ontology spec → LinkML schema
│       └── validators/
│           ├── dd_validator.py               # Validate CSV against meta-schema
│           ├── ontology_validator.py          # Validate codes via BioPortal
│           └── annotation_parser.py          # Parse/generate structured annotations
│
├── tests/
│   ├── test_data/
│   │   ├── rarelink_cdm_v2.0.6.csv          # Reference DD for validation
│   │   └── cieinr_extension.csv             # Extension DD for testing
│   ├── test_csv_generator.py
│   ├── test_validator.py
│   └── test_roundtrip.py                    # CSV → instance → CSV roundtrip
│
├── examples/
│   ├── rarelink_cdm/                        # Full RareLink CDM as schema instance
│   ├── cieinr/                              # CIEINR extension example
│   └── minimal_instrument/                  # Minimal working example
│
└── docs/
    ├── index.md
    ├── schema_reference.md                  # Auto-generated from schema
    └── integration_guide.md                 # How to use with RareLink
```

## Relationship Between Schemas

There are three distinct schema layers that work together:

### Layer 1: `redcap-data-dictionary.yaml` (this project)
**What it models:** The structure of REDCap data dictionaries themselves.
**Instances:** A complete REDCap DD CSV (108 fields of the RareLink-CDM, for example).
**Purpose:** Validate and generate REDCap DD CSVs.

### Layer 2: `rarelink_cdm.yaml` + instrument schemas (RareLink project)
**What it models:** The clinical data model — what data is captured.
**Instances:** Patient records (JSON/YAML conforming to the CDM).
**Purpose:** Validate clinical data, generate Python classes for processing.

### Layer 3: `rd-cdm` code systems (rd-cdm package)
**What it models:** Ontology code systems, versions, and value sets.
**Instances:** `CodeSystemsContainer` with current ontology versions.
**Purpose:** Provide version-controlled ontology references.

### How they connect:

```
rd-cdm CodeSystemsContainer
  │
  │ provides ontology versions + valid codes
  │
  ▼
redcap-data-dictionary meta-schema
  │
  │ validates structure ──────────────────────┐
  │                                           │
  ▼                                           ▼
REDCap DD CSV ◄──────────────────── rarelink_cdm.yaml
  (108 fields,                      (data model: Record,
   18 columns each)                  FormalCriteria, Disease, ...)
  │                                           │
  │ uploaded to REDCap                        │ validates clinical data
  │                                           │
  ▼                                           ▼
REDCap Project ──── CLI export ──── LinkML JSON instances
                                              │
                                              ▼
                                    Phenopackets / FHIR
```

## Key Design Decisions

### 1. Two-schema approach (recommended)

The meta-schema (`redcap-data-dictionary.yaml`) should NOT import or depend on
the clinical schema (`rarelink_cdm.yaml`). They model different things:

- Meta-schema: "Is this a valid REDCap DD CSV?"
- Clinical schema: "Is this valid patient data?"

The connection is in the **tooling**, not the schema. A generator uses the
meta-schema to produce a valid CSV and the clinical schema to ensure the
fields match the data model.

### 2. Ontology conventions as optional profile

The base meta-schema defines REDCap's own rules (useful for anyone).
RareLink-specific conventions (variable naming with ontology prefixes,
structured annotations, BioPortal patterns) are included as enums and
documentation but don't constrain the base Field class. This means:

- Any REDCap DD can be validated against the base schema
- Ontology-based DDs additionally validated against the conventions
- Non-RareLink projects can use just the base validation

### 3. Roundtrip fidelity

A critical test: parse a real REDCap DD CSV into schema instances,
then serialize back to CSV. The output must be byte-identical (modulo
whitespace normalization). This ensures no information is lost.

## Integration Points with RareLink Issues

| Issue | How this project addresses it |
|-------|------------------------------|
| #223 (YAML-based mappings) | Mapping configs generated alongside DD CSVs |
| #204 (LLM automation) | Meta-schema = contract for Claude skill |
| #209 (simplified setup) | CLI tool generates all artifacts from ontology input |
| #185 (extensional models) | New instruments = configuration, not development |

## Next Steps (Proposed)

### Phase 1: Schema stabilisation (weeks 1-2)
- Validate meta-schema against RareLink-CDM v2.0.6 DD (all 108 fields)
- Validate against CIEINR extension DD
- Write roundtrip tests (CSV → instance → CSV)
- Community feedback from LinkML call

### Phase 2: Generator tooling (weeks 3-4)
- CSV parser: REDCap DD CSV → schema instances
- CSV generator: schema instances → REDCap DD CSV
- Annotation parser: structured text ↔ OntologyAnnotation instances

### Phase 3: Claude skill prototype (weeks 5-6)
- Skill definition: input format, validation steps, output artifacts
- Integration with rd-cdm for ontology version lookup
- End-to-end test: Excel input → validated DD + LinkML + mapping config

### Phase 4: Integration with RareLink (weeks 7-8)
- CLI command: `rarelink instruments generate <spec.xlsx>`
- Documentation update: new instrument development workflow
- CIEINR as validation case study
