from pathlib import Path
from .redcap_data_dictionary import *

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "redcap_data_dictionary.yaml"
