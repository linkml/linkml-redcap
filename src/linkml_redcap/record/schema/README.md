# Schema Directory — `record`

`redcap_record.yaml` is the reusable LinkML **envelope for REDCap record data**
(as opposed to `data_dictionary/`, which models the data dictionary that
*describes* the data).

It defines, once, the structural pieces shared by every REDCap project so they
can be imported instead of redeclared:

- **`FlatRecord`** — the flat-export row envelope (`record_id`,
  `redcap_event_name`, `redcap_repeat_instrument`, `redcap_repeat_instance`,
  `redcap_data_access_group`, `redcap_survey_identifier`). Source root for a
  flat → structured mapping.
- **`StructuredRecord`** — the nested per-record root. Target root for a
  flat → structured mapping.
- **`RepeatedElement`** — the `(instrument, instance)` wrapper for one repeating
  instance (replaces the identical class copied into each project schema).
- Enums **`FormCompleteStatus`** (0/1/2), **`YesNo`**, **`TrueFalse`**,
  **`CheckboxState`** — REDCap's universal value spaces.
- Types **`redcap_date`**, **`redcap_datetime`**, **`redcap_time`**,
  **`redcap_integer`**, **`redcap_number`**, **`redcap_email`** — one typed
  primitive per REDCap value space (with the empty-string "no value" case),
  replacing the per-project `union_date_string`.

See `instructions/MAPPING_WORKFLOW.md` for how a project imports this and uses
`linkml-map` to convert flat ⇄ structured.
