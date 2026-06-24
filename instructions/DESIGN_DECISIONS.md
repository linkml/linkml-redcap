# Design Decisions

A record of *what* `linkml-redcap` is, the decisions made building it, and *why*.
Read alongside `COMPATIBILITY.md` (the stability policy) and `MAPPING_WORKFLOW.md`
(how consumers use it).

## 1. Scope: REDCap primitives only — one source of truth

`linkml-redcap` is the single, authoritative, vendor-neutral model of **REDCap
itself**. Two submodules, both modelling real REDCap constructs:

- **`data_dictionary`** — the REDCap data dictionary (the 18-column CSV that
  *describes* a project): fields, choices, field/validation types, etc.
- **`record`** — the REDCap **record** (the data a project *exports*), in the two
  serializations the data uses: `FlatRecord` (the flat export row) and
  `StructuredRecord` / `RepeatedElement` (the lossless record-grouped form),
  plus the structural columns and universal value spaces.

**Decision:** everything here corresponds 1:1 to a real REDCap construct. Nothing
project-specific is defined or duplicated. For example, the [RareLink](https://rarelink.readthedocs.io/en/latest/index.html)
*rules* (variable-naming conventions, instrument-naming conventions, the
annotation profile, and the **named-instrument-block specialization** of the
structured form — the typed `Disease` / `PhenotypicFeature` / … classes) live in
the **rarelink** repository and are layered on top of these primitives. The
*abstract, generic structured envelope* they specialise (`StructuredRecord` /
`RepeatedElement`) is defined here — see §2.

**Why:** a shared dependency must have exactly one owner per concept. If the
REDCap representation lived partly here and partly in each consumer repository
(e.g., RareLink), they would drift.

## 2. Including the structured serialization (the key scope decision)

The structured/nested form (`StructuredRecord` + `RepeatedElement` +
`repeated_elements`) is **included here, generically**. This was debated — REDCap
never literally *emits* this shape — and the decision rests on a specific reading:

**Why include it.** REDCap's data model genuinely contains a record and its
repeating-instrument instances, identified by `(redcap_repeat_instrument,
redcap_repeat_instance)`. The flat export is one serialization of that model;
grouping the rows back into "one record with its repeats nested" is a **lossless
re-serialization** of REDCap's own model — it adds nothing and loses nothing. So
it is vendor-neutral REDCap, not an invention. Three further reasons:

- **Cohesion** — the lossless `flat ⇄ structured` conversion (`grouping.py`)
  already lives here; its output shape should have its schema here too.
- **One source of truth** — previous repos each redeclare a `RepeatedElement`
  today; defining it once here lets them import the canonical class and delete
  their copies (the duplication this package set out to remove).
- **Dependency layering** — a consumer that wants structured REDCap data but not
  Phenopackets then depends on `linkml-redcap` alone; rarelink is added only for
  the rare-disease semantics and subsequent Phenopackets export. The package
  stays useful to the wider REDCap/LinkML community.

**The guardrail that keeps it neutral.** `StructuredRecord` / `RepeatedElement`
are **abstract, generic and lossless**: `StructuredRecord` = `record_id` + a
single `(instrument, instance)`-tagged `repeated_elements` list (the minimal
lossless representation of REDCap's repeats — a per-instrument-list alternative
would impose *more* structure); `RepeatedElement` = the two REDCap repeat fields.

## 3. The `type=flat` data only (EAV and ODM/XML out of scope)

REDCap's record export offers `type=flat` (one row per record/event/repeat) and
`type=eav` (a long, one-datapoint-per-row entity-attribute-value format — *not*
truly nested). It also serialises to CSV/JSON/XML/ODM.

**Decision:** model the `type=flat` data (in both its flat and structured
serializations, per §2). EAV and XML/ODM are out of scope.

**Why:** flat is the canonical export everyone uses and the shape all the
existing RareLink data is in. EAV is trivially pivot-to-flat and rarely used in
this pipeline; XML/ODM are alternate serialisations of the same content. Crucially
the structural slots here are the *same discriminators* EAV uses, so an
`EavRecord` class can be added later **additively** without breaking anything.

**EAV vs. our compaction (why we did not adopt EAV).** EAV's appeal is that it
omits empty cells — but that is exactly what `group_flat_records(..., drop_empty=
True)` already does (§3a), while keeping the data in the flat/structured shape the
pipeline consumes. EAV would instead force a *pivot* (re-assemble rows by
`(record, instrument, instance)`, un-melt `field_name`/`value` back into columns,
and specially handle checkbox `field___code` entities) before anything could use
it. So EAV trades a clean 1:1 ingest for a sparseness we can produce natively. We
keep flat JSON as the core and treat EAV/XML as optional future *readers*, never
the centre.

## 3a. Compaction: drop empties, keep a template for the import round-trip

The flat export is *wide* — every row carries the full column set, mostly empty
(REDCap pads "no value" with `""`). On real registries the padding is ~90% of the
bytes (measured: a 117-column cohort compacts to ~8% of its cells, ~11% of its
JSON, with `drop_empty=True`).

**Decision:** the supported way to compact the grouped form is
`group_flat_records(..., drop_empty=True)` — omit empty values from each record and
repeated element. We do **not** add named-instrument bucketing to the grouping
helper to save size (that needs the project's field→instrument map and belongs in
`linkml-map`; and on real data it is actually *larger* than drop-empty, since it
keeps the empty slots inside each named block).

**Why it is vendor-neutral and safe.** Dropping `""`/`None` removes REDCap's own
padding, not information — REDCap itself treats empty as absent, and our typed
primitives already permit the empty case (§4). It is safe across records whose
instruments are differently populated: a field present in one disease instance and
absent from another both map correctly, because a `linkml-map` mapper reads the
slots that are present and emits nothing for those that are not — identical in
meaning to reading an empty string. (Verified on the real evaluation cohort: zero
non-empty cells are ever dropped.)

**The template contract.** Dropping empties discards *which* columns existed, so
reconstructing a full-width REDCap **import** file requires the project's
full-width template. `ungroup_records(grouped, template=T)` re-pads every row to
the complete column set; `ungroup_records(grouped)` (no template) returns rows
carrying only the populated fields — fine for inspection or for feeding the
mapper, but **not** a complete REDCap import header. So:
`ungroup(group(rows, drop_empty=True), template=T)` is lossless (verified on real
data); without the template it preserves every datum but not the full width. The
full-width template is exactly what the planned **rarelink-project-copier**
guarantees each scaffolded project ships, so the import round-trip "just works"
per project.

## 4. Maximum typing — never `Any`, never bare `string` where REDCap constrains

REDCap exports every value as a string and uses an empty string for "no value".

**Decision:** provide a typed primitive for each REDCap value space —
- enums `FormCompleteStatus` (0/1/2), `YesNo`, `TrueFalse`, `CheckboxState`;
- types `redcap_date`, `redcap_datetime`, `redcap_time`, `redcap_integer`,
  `redcap_number`, `redcap_email` (each keeps the raw string, constrains the
  format, and permits the empty case);
— so a project's flat schema can give **every** field a defined range. The
structural slots are themselves typed (`record_id: string`,
`redcap_repeat_instance: integer`, etc.). `default_range` is `string` (REDCap's
on-the-wire type), never `Any`.

**Why:** good practice for a schema others build on: a fully-typed flat schema
makes the downstream `linkml-map` transformations checkable and the data
validatable. Projects are encouraged to narrow further (e.g. constrain
`redcap_repeat_instrument` to an enum of their own form names).

More value spaces (e.g. `redcap_number_comma` for comma-decimal locales,
`redcap_phone`, `redcap_zipcode`) can be added additively when a project needs
them, rather than shipping speculative or locale-wrong patterns now.

## 5. The `union_date_string` → `redcap_date` consolidation

Each project currently redeclares a `union_date_string` type (a date-or-empty
string). **Decision:** define it once here as `redcap_date` (plus the datetime/
time siblings). **Why:** removes duplicated type definitions across projects; the
"date or empty string" behaviour is a REDCap fact, not a project choice.

## 6. Grouping helper stays here; transformation specs do not

`group_flat_records` / `ungroup_records` perform the flat ⇄ per-record reshaping
that `linkml-map` structurally cannot (a cardinality change: many rows → one
record + a repeats list).

**Decision:** keep this *generic* helper in the package, but keep all
*declarative field/enum mapping* out of it (that is `linkml-map`'s job, written
per project/rarelink).

**Why:** the grouping depends only on REDCap-native fields (`record_id`,
`redcap_repeat_instrument`, `redcap_repeat_instance`) and is byte-identical for
every project, so it is a REDCap-level utility. Its output is exactly a
`StructuredRecord`-shaped dict (untyped at the field level); the **typed
instrument classes** that give those fields meaning are the consuming project's,
and the conventions/mappings are rarelink's.

## 7. How consumers use it (anchored on `FlatRecord`)

1. **Tabular → REDCap-flat:** a `linkml-map` spec from an external source schema
   to the project's `is_a: FlatRecord` schema, with **SSSOM** for value-level
   term mappings. Output is valid, typed REDCap-flat data.
2. **REDCap-flat → Phenopackets/FHIR:** `group_flat_records` → `linkml-map`
   (to the rarelink structured representation) → the rarelink Phenopacket/FHIR
   engine (+ SSSOM for value→ontology mappings).

See `MAPPING_WORKFLOW.md` for the worked pipeline.

## 8. Backwards compatibility as a first-class constraint

Downstream schemas `import` this package by `id` and reference its elements by
name. **Decision:** treat the schema `id`s and public class/slot/enum/type/PV
names as a stable API — additive minors only, deprecate-don't-remove, breaking
changes ⇒ major bump. Enforced by `tests/test_public_surface.py`, a subset check
that fails CI if any frozen name disappears (so a break can only happen as a
conscious edit). Schemas ship inside the wheel and load via
`importlib.resources`, so a pinned version always sees exactly its own schema.
Full rationale in `COMPATIBILITY.md`.

## 9. Engineering choices favouring simplicity

- **Schema-first, minimal runtime.** Core dependency is just `linkml-runtime`;
  the only runtime code is the small, dependency-free grouping module.
- **Loader API parity.** Each submodule exposes the same `SCHEMA_FILENAME`,
  `schema_path()`, `schema_view()` — nothing to relearn between submodules.
- **`linkml-lint --ignore-warnings` in CI.** The numeric REDCap PV names
  (`"0"/"1"/"2"`) intentionally trip the `standard_naming` style rule; they must
  equal REDCap's stored values, so we suppress the *warning* (errors still fail
  CI) rather than misname the values.

## 10. Ontology conventions removed (→ rarelink)

`OntologyPrefix` (the `snomedct_184099003` variable-naming convention),
`OntologyAnnotation` (the structured `field_annotation` grammar: variable code,
coded choices, ontology versions, FHIR/Phenopacket mappings), and
`BioPortalOntology` (a curated ontology list) were **removed** from the
`data_dictionary` schema. They fail the neutrality test (§2): you cannot point at
them and name a REDCap construct — they are RareLink rules. They will be added to
**rarelink** as an ontology-conventions schema/overlay.

This keeps the package faithful to its purpose — the *canonical, vendor-neutral*
REDCap DD model that non-RareLink consumers (e.g. linkml/schema-automator) can
depend on — and aligns with the planned **rarelink-project-copier**: a
datamodel-agnostic template defining the shared rules for all RareLink-based
repos (rarelink-cdm, extensions like CIEINR, other datamodels like
marfan-charité). Those shared rules, including the ontology conventions, belong
in the RareLink layer, not in the REDCap base.

Note: `BioPortalOntology` was a closed enum of 14 ontologies, but REDCap's
BioPortal autocomplete accepts *any* BioPortal ontology — so the enum actually
mismodelled REDCap. The REDCap-native fact (the `BIOPORTAL:<NAME>` choices-column
syntax) is retained as a description on `Field`.

## Open items to revisit

- A few `Field` / `Choice` / `Instrument` descriptions still use "In RareLink,
  …" illustrative examples. They are honestly framed as examples (not REDCap
  rules) and define no structure, so they are left for now; tidy if a fully
  example-free base is wanted.
