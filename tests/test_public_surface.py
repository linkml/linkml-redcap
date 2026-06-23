"""Backwards-compatibility guard.

Downstream schemas ``import`` linkml-redcap and reference its classes, slots,
enums and types by NAME, and reference each schema by its ``id`` URI. Renaming
or removing any of these, or changing a schema id, is a breaking change.

These tests lock the *public surface* as a subset check: every name listed here
must continue to exist. Adding new elements is always fine; removing or renaming
one fails CI and forces a conscious, documented (major-version) decision.

When a deliberate breaking change is made, update the frozen sets below in the
same commit and bump the major version.
"""

from linkml_redcap.data_dictionary import schema_view as dd_view
from linkml_redcap.record import schema_view as record_view

# --- frozen schema ids (NEVER change these once published) ------------------
DD_SCHEMA_ID = "https://w3id.org/linkml/redcap-data-dictionary"
RECORD_SCHEMA_ID = "https://w3id.org/linkml/redcap-record"

# --- frozen public names ----------------------------------------------------
DD_CLASSES = {"DataDictionary", "Field", "Choice", "Instrument"}
DD_ENUMS = {
    "FieldType",
    "TextValidationType",
    "CustomAlignment",
    "IdentifierStatus",
    "MatrixRanking",
}

RECORD_CLASSES = {"FlatRecord", "StructuredRecord", "RepeatedElement"}
RECORD_SLOTS = {
    "record_id",
    "redcap_event_name",
    "redcap_repeat_instrument",
    "redcap_repeat_instance",
    "redcap_data_access_group",
    "redcap_survey_identifier",
    "repeated_elements",
}
RECORD_ENUMS = {"FormCompleteStatus", "YesNo", "TrueFalse", "CheckboxState"}
RECORD_TYPES = {
    "redcap_date",
    "redcap_datetime",
    "redcap_time",
    "redcap_integer",
    "redcap_number",
    "redcap_email",
}


def _missing(expected, actual):
    return expected - set(actual)


def test_dd_schema_id_stable():
    assert dd_view().schema.id == DD_SCHEMA_ID


def test_dd_public_surface_present():
    sv = dd_view()
    assert not _missing(DD_CLASSES, sv.all_classes())
    assert not _missing(DD_ENUMS, sv.all_enums())


def test_record_schema_id_stable():
    assert record_view().schema.id == RECORD_SCHEMA_ID


def test_record_public_surface_present():
    sv = record_view()
    assert not _missing(RECORD_CLASSES, sv.all_classes())
    assert not _missing(RECORD_SLOTS, sv.all_slots())
    assert not _missing(RECORD_ENUMS, sv.all_enums())
    assert not _missing(RECORD_TYPES, sv.all_types())


def test_form_complete_status_values_stable():
    enum = record_view().get_enum("FormCompleteStatus")
    assert {"0", "1", "2"} <= set(enum.permissible_values)
