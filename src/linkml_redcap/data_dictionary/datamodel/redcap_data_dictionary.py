# Auto generated from redcap_data_dictionary.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-17T10:18:23
# Schema: redcap_data_dictionary
#
# id: https://w3id.org/linkml/redcap-data-dictionary
# description: A LinkML meta-schema that formally models the structure of REDCap data dictionaries (CSV format). This schema defines the rules, constraints, and relationships of all 18 REDCap data dictionary columns, enabling programmatic validation, generation, and transformation of REDCap instruments. It also provides extension points for ontology-based data models (e.g., RareLink-CDM) that embed coded terminologies directly into REDCap's variable naming, choice encoding, and field annotation structures.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = "0.1.0"

# Namespaces
ECO = CurieNamespace('ECO', 'http://purl.obolibrary.org/obo/ECO_')
GA4GH = CurieNamespace('GA4GH', 'https://www.ga4gh.org/')
HGNC = CurieNamespace('HGNC', 'https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/')
HL7FHIR = CurieNamespace('HL7FHIR', 'https://www.hl7.org/fhir/')
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
ICD10CM = CurieNamespace('ICD10CM', 'http://hl7.org/fhir/sid/icd-10-cm/')
ICD11 = CurieNamespace('ICD11', 'https://icd.who.int/browse/2024-01/mms/en/')
ICF = CurieNamespace('ICF', 'https://www.who.int/classifications/icf/')
ISO3166 = CurieNamespace('ISO3166', 'https://www.iso.org/iso-3166-country-codes.html/')
LOINC = CurieNamespace('LOINC', 'http://loinc.org/')
MAXO = CurieNamespace('MAXO', 'http://purl.obolibrary.org/obo/MAXO_')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
OMIM = CurieNamespace('OMIM', 'https://omim.org/entry/')
ORDO = CurieNamespace('ORDO', 'http://www.orpha.net/ORDO/')
SNOMEDCT = CurieNamespace('SNOMEDCT', 'http://snomed.info/sct/')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
REDCAP_DD = CurieNamespace('redcap_dd', 'https://w3id.org/linkml/redcap-data-dictionary/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = REDCAP_DD


# Types

# Class references
class FieldVariableFieldName(extended_str):
    pass


class InstrumentInstrumentName(extended_str):
    pass


@dataclass(repr=False)
class DataDictionary(YAMLRoot):
    """
    A complete REDCap data dictionary representing one or more instruments (forms). This is the top-level container
    that corresponds to the CSV file uploaded to REDCap. Fields must be grouped contiguously by form_name.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REDCAP_DD["DataDictionary"]
    class_class_curie: ClassVar[str] = "redcap_dd:DataDictionary"
    class_name: ClassVar[str] = "DataDictionary"
    class_model_uri: ClassVar[URIRef] = REDCAP_DD.DataDictionary

    fields: Union[dict[Union[str, FieldVariableFieldName], Union[dict, "Field"]], list[Union[dict, "Field"]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.fields):
            self.MissingRequiredField("fields")
        self._normalize_inlined_as_list(slot_name="fields", slot_type=Field, key_name="variable_field_name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Field(YAMLRoot):
    """
    A single variable (field) in a REDCap data dictionary. This class maps directly to one row of the REDCap data
    dictionary CSV, with each attribute corresponding to one of the 18 standard columns.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REDCAP_DD["Field"]
    class_class_curie: ClassVar[str] = "redcap_dd:Field"
    class_name: ClassVar[str] = "Field"
    class_model_uri: ClassVar[URIRef] = REDCAP_DD.Field

    variable_field_name: Union[str, FieldVariableFieldName] = None
    form_name: str = None
    field_type: Union[str, "FieldType"] = None
    field_label: str = None
    section_header: Optional[str] = None
    choices_calculations_slider_labels: Optional[str] = None
    field_note: Optional[str] = None
    text_validation_type_or_show_slider_number: Optional[Union[str, "TextValidationType"]] = None
    text_validation_min: Optional[str] = None
    text_validation_max: Optional[str] = None
    identifier: Optional[Union[str, "IdentifierStatus"]] = None
    branching_logic: Optional[str] = None
    required_field: Optional[str] = None
    custom_alignment: Optional[Union[str, "CustomAlignment"]] = None
    question_number: Optional[str] = None
    matrix_group_name: Optional[str] = None
    matrix_ranking: Optional[Union[str, "MatrixRanking"]] = None
    field_annotation: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.variable_field_name):
            self.MissingRequiredField("variable_field_name")
        if not isinstance(self.variable_field_name, FieldVariableFieldName):
            self.variable_field_name = FieldVariableFieldName(self.variable_field_name)

        if self._is_empty(self.form_name):
            self.MissingRequiredField("form_name")
        if not isinstance(self.form_name, str):
            self.form_name = str(self.form_name)

        if self._is_empty(self.field_type):
            self.MissingRequiredField("field_type")
        if not isinstance(self.field_type, FieldType):
            self.field_type = FieldType(self.field_type)

        if self._is_empty(self.field_label):
            self.MissingRequiredField("field_label")
        if not isinstance(self.field_label, str):
            self.field_label = str(self.field_label)

        if self.section_header is not None and not isinstance(self.section_header, str):
            self.section_header = str(self.section_header)

        if self.choices_calculations_slider_labels is not None and not isinstance(self.choices_calculations_slider_labels, str):
            self.choices_calculations_slider_labels = str(self.choices_calculations_slider_labels)

        if self.field_note is not None and not isinstance(self.field_note, str):
            self.field_note = str(self.field_note)

        if self.text_validation_type_or_show_slider_number is not None and not isinstance(self.text_validation_type_or_show_slider_number, TextValidationType):
            self.text_validation_type_or_show_slider_number = TextValidationType(self.text_validation_type_or_show_slider_number)

        if self.text_validation_min is not None and not isinstance(self.text_validation_min, str):
            self.text_validation_min = str(self.text_validation_min)

        if self.text_validation_max is not None and not isinstance(self.text_validation_max, str):
            self.text_validation_max = str(self.text_validation_max)

        if self.identifier is not None and not isinstance(self.identifier, IdentifierStatus):
            self.identifier = IdentifierStatus(self.identifier)

        if self.branching_logic is not None and not isinstance(self.branching_logic, str):
            self.branching_logic = str(self.branching_logic)

        if self.required_field is not None and not isinstance(self.required_field, str):
            self.required_field = str(self.required_field)

        if self.custom_alignment is not None and not isinstance(self.custom_alignment, CustomAlignment):
            self.custom_alignment = CustomAlignment(self.custom_alignment)

        if self.question_number is not None and not isinstance(self.question_number, str):
            self.question_number = str(self.question_number)

        if self.matrix_group_name is not None and not isinstance(self.matrix_group_name, str):
            self.matrix_group_name = str(self.matrix_group_name)

        if self.matrix_ranking is not None and not isinstance(self.matrix_ranking, MatrixRanking):
            self.matrix_ranking = MatrixRanking(self.matrix_ranking)

        if self.field_annotation is not None and not isinstance(self.field_annotation, str):
            self.field_annotation = str(self.field_annotation)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Choice(YAMLRoot):
    """
    A single permissible value for a dropdown, radio, or checkbox field. In REDCap CSV format, choices are encoded as
    a pipe-delimited string, but this class provides a structured representation for programmatic generation and
    validation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REDCAP_DD["Choice"]
    class_class_curie: ClassVar[str] = "redcap_dd:Choice"
    class_name: ClassVar[str] = "Choice"
    class_model_uri: ClassVar[URIRef] = REDCAP_DD.Choice

    raw_value: str = None
    label: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.raw_value):
            self.MissingRequiredField("raw_value")
        if not isinstance(self.raw_value, str):
            self.raw_value = str(self.raw_value)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OntologyAnnotation(YAMLRoot):
    """
    Structured metadata embedded in a field's annotation column for ontology-based data models. This formalises the
    annotation pattern used in RareLink and similar frameworks where each field carries its semantic definition, coded
    choices, ontology versions, and mappings to interoperability standards (HL7 FHIR, GA4GH Phenopackets).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REDCAP_DD["OntologyAnnotation"]
    class_class_curie: ClassVar[str] = "redcap_dd:OntologyAnnotation"
    class_name: ClassVar[str] = "OntologyAnnotation"
    class_model_uri: ClassVar[URIRef] = REDCAP_DD.OntologyAnnotation

    variable_code: str = None
    coded_choices: Optional[Union[str, list[str]]] = empty_list()
    ontology_versions: Optional[Union[str, list[str]]] = empty_list()
    fhir_mapping: Optional[str] = None
    phenopacket_mapping: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.variable_code):
            self.MissingRequiredField("variable_code")
        if not isinstance(self.variable_code, str):
            self.variable_code = str(self.variable_code)

        if not isinstance(self.coded_choices, list):
            self.coded_choices = [self.coded_choices] if self.coded_choices is not None else []
        self.coded_choices = [v if isinstance(v, str) else str(v) for v in self.coded_choices]

        if not isinstance(self.ontology_versions, list):
            self.ontology_versions = [self.ontology_versions] if self.ontology_versions is not None else []
        self.ontology_versions = [v if isinstance(v, str) else str(v) for v in self.ontology_versions]

        if self.fhir_mapping is not None and not isinstance(self.fhir_mapping, str):
            self.fhir_mapping = str(self.fhir_mapping)

        if self.phenopacket_mapping is not None and not isinstance(self.phenopacket_mapping, str):
            self.phenopacket_mapping = str(self.phenopacket_mapping)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Instrument(YAMLRoot):
    """
    A logical REDCap instrument (form) grouping related fields. This class is not directly represented in the CSV but
    is derived from the contiguous grouping of fields sharing the same form_name. In RareLink, instruments follow the
    naming convention 'rarelink_N_section_name' and each has a completion status field.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REDCAP_DD["Instrument"]
    class_class_curie: ClassVar[str] = "redcap_dd:Instrument"
    class_name: ClassVar[str] = "Instrument"
    class_model_uri: ClassVar[URIRef] = REDCAP_DD.Instrument

    instrument_name: Union[str, InstrumentInstrumentName] = None
    fields: Union[dict[Union[str, FieldVariableFieldName], Union[dict, Field]], list[Union[dict, Field]]] = empty_dict()
    instrument_label: Optional[str] = None
    is_repeating: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.instrument_name):
            self.MissingRequiredField("instrument_name")
        if not isinstance(self.instrument_name, InstrumentInstrumentName):
            self.instrument_name = InstrumentInstrumentName(self.instrument_name)

        if self._is_empty(self.fields):
            self.MissingRequiredField("fields")
        self._normalize_inlined_as_list(slot_name="fields", slot_type=Field, key_name="variable_field_name", keyed=True)

        if self.instrument_label is not None and not isinstance(self.instrument_label, str):
            self.instrument_label = str(self.instrument_label)

        if self.is_repeating is not None and not isinstance(self.is_repeating, Bool):
            self.is_repeating = Bool(self.is_repeating)

        super().__post_init__(**kwargs)


# Enumerations
class FieldType(EnumDefinitionImpl):
    """
    The complete set of REDCap field types that determine how a variable is rendered and what data it accepts.
    """
    text = PermissibleValue(
        text="text",
        description="""Single-line text input. Can be combined with validation types (date_ymd, integer, number, email, etc.) and BioPortal ontology autocomplete.""")
    notes = PermissibleValue(
        text="notes",
        description="Large multi-line text area for free-text entry.")
    dropdown = PermissibleValue(
        text="dropdown",
        description="Single-select dropdown menu. Requires choices to be specified in the choices column.")
    radio = PermissibleValue(
        text="radio",
        description="Single-select radio button group. Requires choices to be specified in the choices column.")
    checkbox = PermissibleValue(
        text="checkbox",
        description="""Multi-select checkboxes. Requires choices. Each checkbox creates a separate binary variable in the export.""")
    yesno = PermissibleValue(
        text="yesno",
        description="Built-in Yes/No radio buttons (stored as 1/0).")
    truefalse = PermissibleValue(
        text="truefalse",
        description="Built-in True/False radio buttons (stored as 1/0).")
    calc = PermissibleValue(
        text="calc",
        description="Calculated field. The calculation expression is specified in the choices column.")
    file = PermissibleValue(
        text="file",
        description="File upload field for attaching documents or images.")
    slider = PermissibleValue(
        text="slider",
        description="""Visual analogue scale (0-100). Anchor labels are specified in the choices column as 'left | center | right'.""")
    descriptive = PermissibleValue(
        text="descriptive",
        description="Display-only field for instructional text, images, or HTML content. Does not collect data.")
    sql = PermissibleValue(
        text="sql",
        description="Dynamic dropdown populated by a SQL query against the REDCap database.")

    _defn = EnumDefinition(
        name="FieldType",
        description="""The complete set of REDCap field types that determine how a variable is rendered and what data it accepts.""",
    )

class TextValidationType(EnumDefinitionImpl):
    """
    Validation rules for text fields constraining the input format.
    """
    date_ymd = PermissibleValue(
        text="date_ymd",
        description="Date in YYYY-MM-DD format.")
    date_mdy = PermissibleValue(
        text="date_mdy",
        description="Date in MM-DD-YYYY format.")
    date_dmy = PermissibleValue(
        text="date_dmy",
        description="Date in DD-MM-YYYY format.")
    datetime_ymd = PermissibleValue(
        text="datetime_ymd",
        description="Datetime in YYYY-MM-DD HH:MM format.")
    datetime_mdy = PermissibleValue(
        text="datetime_mdy",
        description="Datetime in MM-DD-YYYY HH:MM format.")
    datetime_dmy = PermissibleValue(
        text="datetime_dmy",
        description="Datetime in DD-MM-YYYY HH:MM format.")
    datetime_seconds_ymd = PermissibleValue(
        text="datetime_seconds_ymd",
        description="Datetime with seconds in YYYY-MM-DD HH:MM:SS format.")
    time = PermissibleValue(
        text="time",
        description="Time in HH:MM format.")
    integer = PermissibleValue(
        text="integer",
        description="Whole number (no decimals).")
    number = PermissibleValue(
        text="number",
        description="Decimal number.")
    number_1dp = PermissibleValue(
        text="number_1dp",
        description="Number with 1 decimal place.")
    number_2dp = PermissibleValue(
        text="number_2dp",
        description="Number with 2 decimal places.")
    phone = PermissibleValue(
        text="phone",
        description="Phone number format.")
    email = PermissibleValue(
        text="email",
        description="Email address format.")
    zipcode = PermissibleValue(
        text="zipcode",
        description="US ZIP code format.")
    alpha_only = PermissibleValue(
        text="alpha_only",
        description="Letters only (no numbers or special characters).")

    _defn = EnumDefinition(
        name="TextValidationType",
        description="Validation rules for text fields constraining the input format.",
    )

class CustomAlignment(EnumDefinitionImpl):
    """
    Field alignment options for the data entry form.
    """
    LV = PermissibleValue(
        text="LV",
        description="Left Vertical")
    LH = PermissibleValue(
        text="LH",
        description="Left Horizontal")
    RV = PermissibleValue(
        text="RV",
        description="Right Vertical (default)")
    RH = PermissibleValue(
        text="RH",
        description="Right Horizontal")

    _defn = EnumDefinition(
        name="CustomAlignment",
        description="Field alignment options for the data entry form.",
    )

class IdentifierStatus(EnumDefinitionImpl):
    """
    Whether a field contains Protected Health Information.
    """
    y = PermissibleValue(
        text="y",
        description="Field contains identifying information (PHI).")

    _defn = EnumDefinition(
        name="IdentifierStatus",
        description="Whether a field contains Protected Health Information.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "",
            PermissibleValue(
                text="",
                description="Field does not contain identifying information."))

class MatrixRanking(EnumDefinitionImpl):
    """
    Whether matrix ranking is enabled.
    """
    y = PermissibleValue(
        text="y",
        description="Ranking is enabled for this matrix group.")

    _defn = EnumDefinition(
        name="MatrixRanking",
        description="Whether matrix ranking is enabled.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "",
            PermissibleValue(
                text="",
                description="Ranking is not enabled."))

class OntologyPrefix(EnumDefinitionImpl):
    """
    Recognised ontology prefixes used in ontology-based REDCap variable naming. In the RareLink convention, variable
    names encode their semantic source as: prefix_conceptid (e.g., snomedct_184099003). This enum defines the valid
    prefixes.
    """
    snomedct = PermissibleValue(
        text="snomedct",
        description="SNOMED CT concept",
        meaning=SNOMEDCT["0"])
    loinc = PermissibleValue(
        text="loinc",
        description="LOINC observation code",
        meaning=LOINC["0"])
    hp = PermissibleValue(
        text="hp",
        description="Human Phenotype Ontology term",
        meaning=HP["0000000"])
    mondo = PermissibleValue(
        text="mondo",
        description="Monarch Disease Ontology term",
        meaning=MONDO["0000000"])
    ncit = PermissibleValue(
        text="ncit",
        description="NCI Thesaurus concept",
        meaning=NCIT["C0"])
    hl7fhir = PermissibleValue(
        text="hl7fhir",
        description="HL7 FHIR element reference",
        meaning=HL7FHIR["0"])
    ga4gh = PermissibleValue(
        text="ga4gh",
        description="GA4GH schema element reference",
        meaning=GA4GH["0"])
    ordo = PermissibleValue(
        text="ordo",
        description="Orphanet Rare Disease Ontology term",
        meaning=ORDO["0"])
    omim = PermissibleValue(
        text="omim",
        description="OMIM entry reference",
        meaning=OMIM["0"])
    hgnc = PermissibleValue(
        text="hgnc",
        description="HGNC gene symbol",
        meaning=HGNC["0"])
    maxo = PermissibleValue(
        text="maxo",
        description="Medical Action Ontology term",
        meaning=MAXO["0"])
    icf = PermissibleValue(
        text="icf",
        description="ICF classification code",
        meaning=ICF["0"])
    ln = PermissibleValue(
        text="ln",
        description="LOINC panel or group code (alternative prefix)",
        meaning=LOINC["0"])

    _defn = EnumDefinition(
        name="OntologyPrefix",
        description="""Recognised ontology prefixes used in ontology-based REDCap variable naming. In the RareLink convention, variable names encode their semantic source as: prefix_conceptid (e.g., snomedct_184099003). This enum defines the valid prefixes.""",
    )

class BioPortalOntology(EnumDefinitionImpl):
    """
    Ontology identifiers available through REDCap's BioPortal integration for text field autocomplete. Used in the
    choices column as 'BIOPORTAL:ONTOLOGY_NAME'.
    """
    HP = PermissibleValue(
        text="HP",
        description="Human Phenotype Ontology")
    MONDO = PermissibleValue(
        text="MONDO",
        description="Monarch Disease Ontology")
    SNOMEDCT = PermissibleValue(
        text="SNOMEDCT",
        description="SNOMED CT")
    ICD10CM = PermissibleValue(
        text="ICD10CM",
        description="ICD-10 Clinical Modification")
    OMIM = PermissibleValue(
        text="OMIM",
        description="Online Mendelian Inheritance in Man")
    ORDO = PermissibleValue(
        text="ORDO",
        description="Orphanet Rare Disease Ontology")
    LOINC = PermissibleValue(
        text="LOINC",
        description="Logical Observation Identifiers Names and Codes")
    UO = PermissibleValue(
        text="UO",
        description="Units of Measurement Ontology")
    NCIT = PermissibleValue(
        text="NCIT",
        description="NCI Thesaurus")
    NCBITAXON = PermissibleValue(
        text="NCBITAXON",
        description="NCBI Taxonomy")
    ECO = PermissibleValue(
        text="ECO",
        description="Evidence and Conclusion Ontology")
    MAXO = PermissibleValue(
        text="MAXO",
        description="Medical Action Ontology")
    ICF = PermissibleValue(
        text="ICF",
        description="International Classification of Functioning")

    _defn = EnumDefinition(
        name="BioPortalOntology",
        description="""Ontology identifiers available through REDCap's BioPortal integration for text field autocomplete. Used in the choices column as 'BIOPORTAL:ONTOLOGY_NAME'.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "HGNC-NR",
            PermissibleValue(
                text="HGNC-NR",
                description="HGNC gene nomenclature (non-redundant)"))

# Slots
class slots:
    pass

slots.dataDictionary__fields = Slot(uri=REDCAP_DD.fields, name="dataDictionary__fields", curie=REDCAP_DD.curie('fields'),
                   model_uri=REDCAP_DD.dataDictionary__fields, domain=None, range=Union[dict[Union[str, FieldVariableFieldName], Union[dict, Field]], list[Union[dict, Field]]])

slots.field__variable_field_name = Slot(uri=REDCAP_DD.variable_field_name, name="field__variable_field_name", curie=REDCAP_DD.curie('variable_field_name'),
                   model_uri=REDCAP_DD.field__variable_field_name, domain=None, range=URIRef,
                   pattern=re.compile(r'^[a-z][a-z0-9_]*$'))

slots.field__form_name = Slot(uri=REDCAP_DD.form_name, name="field__form_name", curie=REDCAP_DD.curie('form_name'),
                   model_uri=REDCAP_DD.field__form_name, domain=None, range=str,
                   pattern=re.compile(r'^[a-z][a-z0-9_]*$'))

slots.field__section_header = Slot(uri=REDCAP_DD.section_header, name="field__section_header", curie=REDCAP_DD.curie('section_header'),
                   model_uri=REDCAP_DD.field__section_header, domain=None, range=Optional[str])

slots.field__field_type = Slot(uri=REDCAP_DD.field_type, name="field__field_type", curie=REDCAP_DD.curie('field_type'),
                   model_uri=REDCAP_DD.field__field_type, domain=None, range=Union[str, "FieldType"])

slots.field__field_label = Slot(uri=REDCAP_DD.field_label, name="field__field_label", curie=REDCAP_DD.curie('field_label'),
                   model_uri=REDCAP_DD.field__field_label, domain=None, range=str)

slots.field__choices_calculations_slider_labels = Slot(uri=REDCAP_DD.choices_calculations_slider_labels, name="field__choices_calculations_slider_labels", curie=REDCAP_DD.curie('choices_calculations_slider_labels'),
                   model_uri=REDCAP_DD.field__choices_calculations_slider_labels, domain=None, range=Optional[str])

slots.field__field_note = Slot(uri=REDCAP_DD.field_note, name="field__field_note", curie=REDCAP_DD.curie('field_note'),
                   model_uri=REDCAP_DD.field__field_note, domain=None, range=Optional[str])

slots.field__text_validation_type_or_show_slider_number = Slot(uri=REDCAP_DD.text_validation_type_or_show_slider_number, name="field__text_validation_type_or_show_slider_number", curie=REDCAP_DD.curie('text_validation_type_or_show_slider_number'),
                   model_uri=REDCAP_DD.field__text_validation_type_or_show_slider_number, domain=None, range=Optional[Union[str, "TextValidationType"]])

slots.field__text_validation_min = Slot(uri=REDCAP_DD.text_validation_min, name="field__text_validation_min", curie=REDCAP_DD.curie('text_validation_min'),
                   model_uri=REDCAP_DD.field__text_validation_min, domain=None, range=Optional[str])

slots.field__text_validation_max = Slot(uri=REDCAP_DD.text_validation_max, name="field__text_validation_max", curie=REDCAP_DD.curie('text_validation_max'),
                   model_uri=REDCAP_DD.field__text_validation_max, domain=None, range=Optional[str])

slots.field__identifier = Slot(uri=REDCAP_DD.identifier, name="field__identifier", curie=REDCAP_DD.curie('identifier'),
                   model_uri=REDCAP_DD.field__identifier, domain=None, range=Optional[Union[str, "IdentifierStatus"]])

slots.field__branching_logic = Slot(uri=REDCAP_DD.branching_logic, name="field__branching_logic", curie=REDCAP_DD.curie('branching_logic'),
                   model_uri=REDCAP_DD.field__branching_logic, domain=None, range=Optional[str])

slots.field__required_field = Slot(uri=REDCAP_DD.required_field, name="field__required_field", curie=REDCAP_DD.curie('required_field'),
                   model_uri=REDCAP_DD.field__required_field, domain=None, range=Optional[str])

slots.field__custom_alignment = Slot(uri=REDCAP_DD.custom_alignment, name="field__custom_alignment", curie=REDCAP_DD.curie('custom_alignment'),
                   model_uri=REDCAP_DD.field__custom_alignment, domain=None, range=Optional[Union[str, "CustomAlignment"]])

slots.field__question_number = Slot(uri=REDCAP_DD.question_number, name="field__question_number", curie=REDCAP_DD.curie('question_number'),
                   model_uri=REDCAP_DD.field__question_number, domain=None, range=Optional[str])

slots.field__matrix_group_name = Slot(uri=REDCAP_DD.matrix_group_name, name="field__matrix_group_name", curie=REDCAP_DD.curie('matrix_group_name'),
                   model_uri=REDCAP_DD.field__matrix_group_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[a-z0-9_]*$'))

slots.field__matrix_ranking = Slot(uri=REDCAP_DD.matrix_ranking, name="field__matrix_ranking", curie=REDCAP_DD.curie('matrix_ranking'),
                   model_uri=REDCAP_DD.field__matrix_ranking, domain=None, range=Optional[Union[str, "MatrixRanking"]])

slots.field__field_annotation = Slot(uri=REDCAP_DD.field_annotation, name="field__field_annotation", curie=REDCAP_DD.curie('field_annotation'),
                   model_uri=REDCAP_DD.field__field_annotation, domain=None, range=Optional[str])

slots.choice__raw_value = Slot(uri=REDCAP_DD.raw_value, name="choice__raw_value", curie=REDCAP_DD.curie('raw_value'),
                   model_uri=REDCAP_DD.choice__raw_value, domain=None, range=str,
                   pattern=re.compile(r'^[a-z0-9_]*$'))

slots.choice__label = Slot(uri=REDCAP_DD.label, name="choice__label", curie=REDCAP_DD.curie('label'),
                   model_uri=REDCAP_DD.choice__label, domain=None, range=str)

slots.ontologyAnnotation__variable_code = Slot(uri=REDCAP_DD.variable_code, name="ontologyAnnotation__variable_code", curie=REDCAP_DD.curie('variable_code'),
                   model_uri=REDCAP_DD.ontologyAnnotation__variable_code, domain=None, range=str)

slots.ontologyAnnotation__coded_choices = Slot(uri=REDCAP_DD.coded_choices, name="ontologyAnnotation__coded_choices", curie=REDCAP_DD.curie('coded_choices'),
                   model_uri=REDCAP_DD.ontologyAnnotation__coded_choices, domain=None, range=Optional[Union[str, list[str]]])

slots.ontologyAnnotation__ontology_versions = Slot(uri=REDCAP_DD.ontology_versions, name="ontologyAnnotation__ontology_versions", curie=REDCAP_DD.curie('ontology_versions'),
                   model_uri=REDCAP_DD.ontologyAnnotation__ontology_versions, domain=None, range=Optional[Union[str, list[str]]])

slots.ontologyAnnotation__fhir_mapping = Slot(uri=REDCAP_DD.fhir_mapping, name="ontologyAnnotation__fhir_mapping", curie=REDCAP_DD.curie('fhir_mapping'),
                   model_uri=REDCAP_DD.ontologyAnnotation__fhir_mapping, domain=None, range=Optional[str])

slots.ontologyAnnotation__phenopacket_mapping = Slot(uri=REDCAP_DD.phenopacket_mapping, name="ontologyAnnotation__phenopacket_mapping", curie=REDCAP_DD.curie('phenopacket_mapping'),
                   model_uri=REDCAP_DD.ontologyAnnotation__phenopacket_mapping, domain=None, range=Optional[str])

slots.instrument__instrument_name = Slot(uri=REDCAP_DD.instrument_name, name="instrument__instrument_name", curie=REDCAP_DD.curie('instrument_name'),
                   model_uri=REDCAP_DD.instrument__instrument_name, domain=None, range=URIRef,
                   pattern=re.compile(r'^[a-z][a-z0-9_]*$'))

slots.instrument__instrument_label = Slot(uri=REDCAP_DD.instrument_label, name="instrument__instrument_label", curie=REDCAP_DD.curie('instrument_label'),
                   model_uri=REDCAP_DD.instrument__instrument_label, domain=None, range=Optional[str])

slots.instrument__is_repeating = Slot(uri=REDCAP_DD.is_repeating, name="instrument__is_repeating", curie=REDCAP_DD.curie('is_repeating'),
                   model_uri=REDCAP_DD.instrument__is_repeating, domain=None, range=Optional[Union[bool, Bool]])

slots.instrument__fields = Slot(uri=REDCAP_DD.fields, name="instrument__fields", curie=REDCAP_DD.curie('fields'),
                   model_uri=REDCAP_DD.instrument__fields, domain=None, range=Union[dict[Union[str, FieldVariableFieldName], Union[dict, Field]], list[Union[dict, Field]]])

