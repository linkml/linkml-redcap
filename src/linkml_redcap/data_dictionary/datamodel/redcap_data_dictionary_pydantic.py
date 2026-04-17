from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.7.0"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'redcap_dd',
     'default_range': 'string',
     'description': 'A LinkML meta-schema that formally models the structure of '
                    'REDCap data dictionaries (CSV format). This schema defines '
                    'the rules, constraints, and relationships of all 18 REDCap '
                    'data dictionary columns, enabling programmatic validation, '
                    'generation, and transformation of REDCap instruments. It also '
                    'provides extension points for ontology-based data models '
                    '(e.g., RareLink-CDM) that embed coded terminologies directly '
                    "into REDCap's variable naming, choice encoding, and field "
                    'annotation structures.',
     'id': 'https://w3id.org/linkml/redcap-data-dictionary',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'redcap_data_dictionary',
     'prefixes': {'ECO': {'prefix_prefix': 'ECO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/ECO_'},
                  'GA4GH': {'prefix_prefix': 'GA4GH',
                            'prefix_reference': 'https://www.ga4gh.org/'},
                  'HGNC': {'prefix_prefix': 'HGNC',
                           'prefix_reference': 'https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/'},
                  'HL7FHIR': {'prefix_prefix': 'HL7FHIR',
                              'prefix_reference': 'https://www.hl7.org/fhir/'},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'ICD10CM': {'prefix_prefix': 'ICD10CM',
                              'prefix_reference': 'http://hl7.org/fhir/sid/icd-10-cm/'},
                  'ICD11': {'prefix_prefix': 'ICD11',
                            'prefix_reference': 'https://icd.who.int/browse/2024-01/mms/en/'},
                  'ICF': {'prefix_prefix': 'ICF',
                          'prefix_reference': 'https://www.who.int/classifications/icf/'},
                  'ISO3166': {'prefix_prefix': 'ISO3166',
                              'prefix_reference': 'https://www.iso.org/iso-3166-country-codes.html/'},
                  'LOINC': {'prefix_prefix': 'LOINC',
                            'prefix_reference': 'http://loinc.org/'},
                  'MAXO': {'prefix_prefix': 'MAXO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/MAXO_'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/NCIT_'},
                  'OMIM': {'prefix_prefix': 'OMIM',
                           'prefix_reference': 'https://omim.org/entry/'},
                  'ORDO': {'prefix_prefix': 'ORDO',
                           'prefix_reference': 'http://www.orpha.net/ORDO/'},
                  'SNOMEDCT': {'prefix_prefix': 'SNOMEDCT',
                               'prefix_reference': 'http://snomed.info/sct/'},
                  'UO': {'prefix_prefix': 'UO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/UO_'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'redcap_dd': {'prefix_prefix': 'redcap_dd',
                                'prefix_reference': 'https://w3id.org/linkml/redcap-data-dictionary/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://github.com/BIH-CEI/rarelink',
                  'https://rarelink.readthedocs.io',
                  'https://projectredcap.org'],
     'source_file': 'src/linkml_redcap/data_dictionary/schema/redcap_data_dictionary.yaml',
     'title': 'REDCap Data Dictionary LinkML Schema'} )

class FieldType(str, Enum):
    """
    The complete set of REDCap field types that determine how a variable is rendered and what data it accepts.
    """
    text = "text"
    """
    Single-line text input. Can be combined with validation types (date_ymd, integer, number, email, etc.) and BioPortal ontology autocomplete.
    """
    notes = "notes"
    """
    Large multi-line text area for free-text entry.
    """
    dropdown = "dropdown"
    """
    Single-select dropdown menu. Requires choices to be specified in the choices column.
    """
    radio = "radio"
    """
    Single-select radio button group. Requires choices to be specified in the choices column.
    """
    checkbox = "checkbox"
    """
    Multi-select checkboxes. Requires choices. Each checkbox creates a separate binary variable in the export.
    """
    yesno = "yesno"
    """
    Built-in Yes/No radio buttons (stored as 1/0).
    """
    truefalse = "truefalse"
    """
    Built-in True/False radio buttons (stored as 1/0).
    """
    calc = "calc"
    """
    Calculated field. The calculation expression is specified in the choices column.
    """
    file = "file"
    """
    File upload field for attaching documents or images.
    """
    slider = "slider"
    """
    Visual analogue scale (0-100). Anchor labels are specified in the choices column as 'left | center | right'.
    """
    descriptive = "descriptive"
    """
    Display-only field for instructional text, images, or HTML content. Does not collect data.
    """
    sql = "sql"
    """
    Dynamic dropdown populated by a SQL query against the REDCap database.
    """


class TextValidationType(str, Enum):
    """
    Validation rules for text fields constraining the input format.
    """
    date_ymd = "date_ymd"
    """
    Date in YYYY-MM-DD format.
    """
    date_mdy = "date_mdy"
    """
    Date in MM-DD-YYYY format.
    """
    date_dmy = "date_dmy"
    """
    Date in DD-MM-YYYY format.
    """
    datetime_ymd = "datetime_ymd"
    """
    Datetime in YYYY-MM-DD HH:MM format.
    """
    datetime_mdy = "datetime_mdy"
    """
    Datetime in MM-DD-YYYY HH:MM format.
    """
    datetime_dmy = "datetime_dmy"
    """
    Datetime in DD-MM-YYYY HH:MM format.
    """
    datetime_seconds_ymd = "datetime_seconds_ymd"
    """
    Datetime with seconds in YYYY-MM-DD HH:MM:SS format.
    """
    time = "time"
    """
    Time in HH:MM format.
    """
    integer = "integer"
    """
    Whole number (no decimals).
    """
    number = "number"
    """
    Decimal number.
    """
    number_1dp = "number_1dp"
    """
    Number with 1 decimal place.
    """
    number_2dp = "number_2dp"
    """
    Number with 2 decimal places.
    """
    phone = "phone"
    """
    Phone number format.
    """
    email = "email"
    """
    Email address format.
    """
    zipcode = "zipcode"
    """
    US ZIP code format.
    """
    alpha_only = "alpha_only"
    """
    Letters only (no numbers or special characters).
    """


class CustomAlignment(str, Enum):
    """
    Field alignment options for the data entry form.
    """
    LV = "LV"
    """
    Left Vertical
    """
    LH = "LH"
    """
    Left Horizontal
    """
    RV = "RV"
    """
    Right Vertical (default)
    """
    RH = "RH"
    """
    Right Horizontal
    """


class IdentifierStatus(str, Enum):
    """
    Whether a field contains Protected Health Information.
    """
    y = "y"
    """
    Field contains identifying information (PHI).
    """
    empty = ""
    """
    Field does not contain identifying information.
    """


class MatrixRanking(str, Enum):
    """
    Whether matrix ranking is enabled.
    """
    y = "y"
    """
    Ranking is enabled for this matrix group.
    """
    empty = ""
    """
    Ranking is not enabled.
    """


class OntologyPrefix(str, Enum):
    """
    Recognised ontology prefixes used in ontology-based REDCap variable naming. In the RareLink convention, variable names encode their semantic source as: prefix_conceptid (e.g., snomedct_184099003). This enum defines the valid prefixes.
    """
    snomedct = "snomedct"
    """
    SNOMED CT concept
    """
    loinc = "loinc"
    """
    LOINC observation code
    """
    hp = "hp"
    """
    Human Phenotype Ontology term
    """
    mondo = "mondo"
    """
    Monarch Disease Ontology term
    """
    ncit = "ncit"
    """
    NCI Thesaurus concept
    """
    hl7fhir = "hl7fhir"
    """
    HL7 FHIR element reference
    """
    ga4gh = "ga4gh"
    """
    GA4GH schema element reference
    """
    ordo = "ordo"
    """
    Orphanet Rare Disease Ontology term
    """
    omim = "omim"
    """
    OMIM entry reference
    """
    hgnc = "hgnc"
    """
    HGNC gene symbol
    """
    maxo = "maxo"
    """
    Medical Action Ontology term
    """
    icf = "icf"
    """
    ICF classification code
    """
    ln = "ln"
    """
    LOINC panel or group code (alternative prefix)
    """


class BioPortalOntology(str, Enum):
    """
    Ontology identifiers available through REDCap's BioPortal integration for text field autocomplete. Used in the choices column as 'BIOPORTAL:ONTOLOGY_NAME'.
    """
    HP = "HP"
    """
    Human Phenotype Ontology
    """
    MONDO = "MONDO"
    """
    Monarch Disease Ontology
    """
    SNOMEDCT = "SNOMEDCT"
    """
    SNOMED CT
    """
    ICD10CM = "ICD10CM"
    """
    ICD-10 Clinical Modification
    """
    OMIM = "OMIM"
    """
    Online Mendelian Inheritance in Man
    """
    ORDO = "ORDO"
    """
    Orphanet Rare Disease Ontology
    """
    LOINC = "LOINC"
    """
    Logical Observation Identifiers Names and Codes
    """
    HGNC_NR = "HGNC-NR"
    """
    HGNC gene nomenclature (non-redundant)
    """
    UO = "UO"
    """
    Units of Measurement Ontology
    """
    NCIT = "NCIT"
    """
    NCI Thesaurus
    """
    NCBITAXON = "NCBITAXON"
    """
    NCBI Taxonomy
    """
    ECO = "ECO"
    """
    Evidence and Conclusion Ontology
    """
    MAXO = "MAXO"
    """
    Medical Action Ontology
    """
    ICF = "ICF"
    """
    International Classification of Functioning
    """



class DataDictionary(ConfiguredBaseModel):
    """
    A complete REDCap data dictionary representing one or more instruments (forms). This is the top-level container that corresponds to the CSV file uploaded to REDCap. Fields must be grouped contiguously by form_name.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/redcap-data-dictionary',
         'rules': [{'description': 'The first field in the data dictionary must be the '
                                   'record identifier (typically record_id) and must '
                                   "be of field_type 'text'."},
                   {'description': 'All fields belonging to the same form_name must be '
                                   'in contiguous rows. No interleaving of forms is '
                                   'permitted.'}],
         'tree_root': True})

    fields: list[Field] = Field(default=..., description="""Ordered list of all fields (variables) in the data dictionary. Fields within the same form must be in contiguous rows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataDictionary', 'Instrument']} })


class Field(ConfiguredBaseModel):
    """
    A single variable (field) in a REDCap data dictionary. This class maps directly to one row of the REDCap data dictionary CSV, with each attribute corresponding to one of the 18 standard columns.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/redcap-data-dictionary'})

    variable_field_name: str = Field(default=..., description="""The unique variable name for this field. Must contain only lowercase letters, numbers, and underscores. Cannot start with a number. Must be unique across the entire project.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    form_name: str = Field(default=..., description="""The instrument (form) this field belongs to. Must be lowercase with underscores only. All fields for a form must be contiguous.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    section_header: Optional[str] = Field(default=None, description="""Optional section header text displayed above this field to visually group fields within a form. Supports HTML/rich text.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    field_type: FieldType = Field(default=..., description="""The type of input field. Determines how the field is rendered in the data entry form and what data it can accept.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    field_label: str = Field(default=..., description="""The display label shown to users during data entry. Supports HTML/rich text formatting. For ontology-based models, this typically includes a section number and human-readable name (e.g., '2.1 Date of birth').""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    choices_calculations_slider_labels: Optional[str] = Field(default=None, description="""For dropdown, radio, and checkbox fields: pipe-delimited list of 'raw_value, label' pairs (e.g., '1, Yes | 2, No | 3, Unknown'). For calc fields: the calculation expression. For slider fields: 'left | center | right' anchor labels. For text fields with BioPortal ontology autocomplete: 'BIOPORTAL:ONTOLOGY_NAME' (e.g., 'BIOPORTAL:HP').""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    field_note: Optional[str] = Field(default=None, description="""Supplementary text displayed below the field during data entry. Typically provides instructions, expected formats, or context.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    text_validation_type_or_show_slider_number: Optional[TextValidationType] = Field(default=None, description="""For text fields: the validation type constraining input format. For slider fields: whether to show the numeric value ('number').""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    text_validation_min: Optional[str] = Field(default=None, description="""Minimum allowed value for validated text fields (dates, numbers).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    text_validation_max: Optional[str] = Field(default=None, description="""Maximum allowed value for validated text fields (dates, numbers).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    identifier: Optional[IdentifierStatus] = Field(default=None, description="""Whether this field contains identifying information (PHI). Set to 'y' for identifier fields. Affects data export behaviour.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    branching_logic: Optional[str] = Field(default=None, description="""Conditional display logic. Uses REDCap's branching syntax (e.g., '[field_name] = ''value'''). When specified, the field is only shown if the condition evaluates to true.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    required_field: Optional[str] = Field(default=None, description="""Whether the field is required for form completion. Set to 'y' for required fields. Can also contain conditional expressions for conditionally required fields.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    custom_alignment: Optional[CustomAlignment] = Field(default=None, description="""Controls the alignment of the field on the form. LV = Left Vertical, LH = Left Horizontal, RV = Right Vertical (default), RH = Right Horizontal.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    question_number: Optional[str] = Field(default=None, description="""Custom question number for surveys. Overrides auto-numbering. Any text entered here is displayed as the question number.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    matrix_group_name: Optional[str] = Field(default=None, description="""Groups multiple radio/checkbox fields into a matrix display. All fields with the same matrix_group_name must be contiguous and use the same field_type and choices.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    matrix_ranking: Optional[MatrixRanking] = Field(default=None, description="""Whether ranking is enabled for this matrix group. When enabled, no two fields in the matrix can have the same selected value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })
    field_annotation: Optional[str] = Field(default=None, description="""Free-text annotation field. In ontology-based models (e.g., RareLink), this contains structured metadata including the semantic variable code, ontology-coded choices, ontology versions, and mappings to interoperability standards.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Field']} })

    @field_validator('variable_field_name')
    def pattern_variable_field_name(cls, v):
        pattern=re.compile(r"^[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid variable_field_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid variable_field_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('form_name')
    def pattern_form_name(cls, v):
        pattern=re.compile(r"^[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid form_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid form_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('matrix_group_name')
    def pattern_matrix_group_name(cls, v):
        pattern=re.compile(r"^[a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid matrix_group_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid matrix_group_name format: {v}"
            raise ValueError(err_msg)
        return v


class Choice(ConfiguredBaseModel):
    """
    A single permissible value for a dropdown, radio, or checkbox field. In REDCap CSV format, choices are encoded as a pipe-delimited string, but this class provides a structured representation for programmatic generation and validation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/redcap-data-dictionary'})

    raw_value: str = Field(default=..., description="""The stored value (code) for this choice. In ontology-based models, this typically encodes the ontology prefix and concept ID (e.g., 'snomedct_248152002'). Must contain only lowercase letters, numbers, and underscores to comply with REDCap naming rules.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Choice']} })
    label: str = Field(default=..., description="""The human-readable display label for this choice (e.g., 'Female', 'Male', 'Unknown').""", json_schema_extra = { "linkml_meta": {'domain_of': ['Choice']} })

    @field_validator('raw_value')
    def pattern_raw_value(cls, v):
        pattern=re.compile(r"^[a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid raw_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid raw_value format: {v}"
            raise ValueError(err_msg)
        return v


class OntologyAnnotation(ConfiguredBaseModel):
    """
    Structured metadata embedded in a field's annotation column for ontology-based data models. This formalises the annotation pattern used in RareLink and similar frameworks where each field carries its semantic definition, coded choices, ontology versions, and mappings to interoperability standards (HL7 FHIR, GA4GH Phenopackets).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/redcap-data-dictionary'})

    variable_code: str = Field(default=..., description="""The ontology code defining the semantic meaning of this field. Format: 'ONTOLOGY:CODE | Human-Readable Label |' Example: 'SNOMED:184099003 | Date of Birth |'""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyAnnotation']} })
    coded_choices: Optional[list[str]] = Field(default=None, description="""List of ontology-coded choices with their labels. Each entry follows the format 'ONTOLOGY:CODE | Label'. Set to 'n/a' for free-text fields without coded choices.""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyAnnotation']} })
    ontology_versions: Optional[list[str]] = Field(default=None, description="""The ontology version(s) referenced by this field's variable code and/or choices. Example: 'SNOMED CT 2025AB'""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyAnnotation']} })
    fhir_mapping: Optional[str] = Field(default=None, description="""The HL7 FHIR resource path this field maps to. Example: 'Patient.birthDate'""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyAnnotation']} })
    phenopacket_mapping: Optional[str] = Field(default=None, description="""The GA4GH Phenopacket Schema element this field maps to. Example: 'Individual.date_of_birth'""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyAnnotation']} })


class Instrument(ConfiguredBaseModel):
    """
    A logical REDCap instrument (form) grouping related fields. This class is not directly represented in the CSV but is derived from the contiguous grouping of fields sharing the same form_name. In RareLink, instruments follow the naming convention 'rarelink_N_section_name' and each has a completion status field.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/redcap-data-dictionary'})

    instrument_name: str = Field(default=..., description="""The form_name shared by all fields in this instrument.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    instrument_label: Optional[str] = Field(default=None, description="""Human-readable label for the instrument. REDCap derives this by capitalising and replacing underscores with spaces.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    is_repeating: Optional[bool] = Field(default=None, description="""Whether this instrument supports repeating instances. In RareLink, sections 4-8 (care pathway, disease, genetic findings, phenotypic features, measurements, family history) are repeating instruments.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    fields: list[Field] = Field(default=..., description="""All fields belonging to this instrument.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataDictionary', 'Instrument']} })

    @field_validator('instrument_name')
    def pattern_instrument_name(cls, v):
        pattern=re.compile(r"^[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid instrument_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid instrument_name format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
DataDictionary.model_rebuild()
Field.model_rebuild()
Choice.model_rebuild()
OntologyAnnotation.model_rebuild()
Instrument.model_rebuild()
