import os
import pathlib
import logging
import json
from typing import OrderedDict
import xmltodict
from roster_entry import RosterEntry, RosterFunction
from roster_database import RosterDatabase
from roster_watcher import RosterWatcher
from datetime import datetime
from rich.logging import RichHandler
from utils import ROSTER_DATABASE_LOCATION

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
MONITOR_CHANGES = os.getenv("MONITOR_CHANGES", "True").lower() == "true"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

DECODER_NAME_MAP = {
    "D13SRJ": "NCE D13SRJ",
    "LokSound 5": "ESU LokSound 5",
    "MX600R version 31+": "Zimo MX600R",
    "MX600R version 37+": "Zimo MX600R",
    "MX600R version 39+": "Zimo MX600R",
    "MX616N version 37+": "Zimo MX616N",
    "MX617 version 37+": "Zimo MX617N",
    "MX617F version 37+": "Zimo MX617F",
    "MX617N version 37+": "Zimo MX617N",
    "MX618N18 version 37+": "Zimo MX618N18",
    "MX644 version 36+": "Zimo MX644D",
    "MX645 version 37+": "Zimo MX645R",
    "MX645R version 36+": "Zimo MX645R",
    "MX648 version 37+": "Zimo MX648R",
    "R8249": "Hornby R8429",
    "Silver+ 21 10321-01": "Lenz Silver+ 21 NEM660",
    "Silver+ mini NEM651 10311-01": "Lenz Silver+ mini NEM651",
    "Silver+ NEM652 10331-01": "Lenz Silver+ NEM652",
    "Standard+ NEM652 10231-01": "Lenz Standard+ NEM652",
    "Standard+ V2 NEM652 10231-02": "Lenz Standard+ V2 NEM652"
}


def does_file_exist(path):
    return os.path.isfile(path)

def roster_iso_datetime_string_to_epoch_second(iso_time: str) -> int:
    try:
        # Take only the first 19 characters of the datetime - this gets rids of the unnecessary milliseconds and timezone offset components.
        utc_time = datetime.strptime(iso_time[0:19], "%Y-%m-%dT%H:%M:%S")
        return (utc_time - datetime(1970, 1, 1)).total_seconds()
    except ValueError as e:
        logging.debug(f"Could not parse ISO datetime: {str(e)}")
        return None
    


def roster_locale_datetime_string_to_epoch_second(last_operated_string: str) -> int:
    try:
        utc_time = datetime.strptime(last_operated_string, "%a %b %d %H:%M:%S %Z %Y")
        return (utc_time - datetime(1970, 1, 1)).total_seconds()
    except ValueError as e:
        logging.debug(f"Could not parse locale datetime: {str(e)}")
        return None

class RosterImporter:

    roster_db: RosterDatabase

    def __init__(self) -> None:
        self.roster_db = RosterDatabase()
    
    def should_process_file(self, file_path: str):
        return pathlib.Path(file_path).suffix.lower() == ".xml"

    def process_existing_files(self, roster_directory: str):
        logging.debug("Scanning for existing files in %s", roster_directory)
        for file in os.listdir(roster_directory):
            self.process_file(roster_directory + "/" + file)

    def process_file(self, file_path):
        logging.info("About to process file: %s", os.path.abspath(file_path))
        if not self.should_process_file(file_path):
            logging.debug("Ignoring file: %s", file_path)
            return None

        # Check the file still exists. The file watcher seems to deliver multiple events per file change, and they seem to all arrive at the same time. So after we have moved the file during the first call to this function, the file will no longer exist.
        if not does_file_exist(file_path):
            return None
        with open(file_path, encoding="utf-8") as file:
            file_dict = xmltodict.parse(file.read())
            self.import_roster_entry_from_dict(file_dict)
    
    def import_roster_entry_from_dict(self, roster_dict: dict):
        locomotive = roster_dict["locomotive-config"]["locomotive"]
        logging.debug(json.dumps(locomotive, indent=4))
        roster_entry = RosterEntry(
            roster_id = locomotive.get("@id"),
            dcc_address = locomotive.get("@dccAddress"),
            number = locomotive.get("@roadNumber"),
            manufacturer = locomotive.get("@mfg"),
            model = locomotive.get("@model"),
            owner = locomotive.get("@owner"),
            comment = locomotive.get("@comment"),
            decoder = process_decoder_model(locomotive.get("decoder").get("@model"))
        )
        # Add the image file path, if set and not empty. We convert this to a path that is relative to the roster folder.
        locomotive_image_file_path = locomotive.get("@imageFilePath")
        if locomotive_image_file_path:
            roster_entry.image_file_path = locomotive.get("@imageFilePath").split("/")[-1]

        # Check for any extra attributes.
        attribute_pairs = locomotive.get("attributepairs")
        if attribute_pairs:
            try:
                key_value_pair = attribute_pairs.get("keyvaluepair")
                if isinstance(key_value_pair, list):    # There is more than one key-value attribute to process.
                    for key_value in key_value_pair:
                        self.process_key_value_pair(key_value, roster_entry)
                elif isinstance(key_value_pair, OrderedDict):
                    self.process_key_value_pair(key_value_pair, roster_entry) # There is only one key-value attribute.
                else:
                    logging.debug("KVP type (%s) not supported", type(key_value_pair))
            except (KeyError, AttributeError) as e:
                logging.warning("Error getting KVPs: %s", e)

        self.roster_db.insert_roster_entry(roster_entry)
        
        # Also insert any functions.
        function_labels = locomotive.get("functionlabels")
        if function_labels:
            try:
                function_label_object = function_labels.get("functionlabel")
                if isinstance(function_label_object, list):    # There is more than one function to process.
                    for function_label in function_label_object:
                        self.process_function(function_label, roster_entry)
                elif isinstance(function_label_object, OrderedDict):
                    self.process_function(function_label_object, roster_entry) # There is only one function.
                else:
                    logging.debug(f"Functionlabel type ({type(key_value_pair)}) not supported")
            except (KeyError, AttributeError) as e:
                logging.warning("Error getting functions: %s", e)

        logging.info("Imported entry with ID %s", roster_entry.roster_id)
        
    
    def process_key_value_pair(self, pair: dict, roster_entry: RosterEntry):
        if pair["key"] == "Name":
            roster_entry.name = pair["value"]
        elif pair["key"] == "Class":
            roster_entry.classification = pair["value"]
        elif pair["key"] == "OperatingDuration":
            roster_entry.operating_duration = pair["value"]
        elif pair["key"] == "LastOperated":
            roster_entry.last_operated = parse_roster_datetime(pair["value"])

    
    def process_function(self, function_dict: dict, roster_entry: RosterEntry):
        function = RosterFunction()
        function.roster_entry = roster_entry.roster_id
        function.number = function_dict.get("@num")
        function.name = function_dict.get("#text")
        function.lockable = function_dict.get("@lockable").lower() == "true"
        self.roster_db.insert_roster_entry_function(function)


def process_decoder_model(decoder: str) -> str:
    if decoder in DECODER_NAME_MAP:
        return DECODER_NAME_MAP[decoder]
    else:
        return decoder

        
def parse_roster_datetime(datetime: str) -> int:
    # This field can annoyingly be in one of two formats, so we try one and then the other.
    timestamp_from_iso = roster_iso_datetime_string_to_epoch_second(datetime)
    if timestamp_from_iso:
        return timestamp_from_iso
    else:
        logging.debug(f"Could not parse datetime string as ISO, trying locale format instead...")
        return roster_locale_datetime_string_to_epoch_second(datetime)



importer = RosterImporter()

def callback(file_path: str):
    importer.process_file(file_path=file_path)

if __name__ == "__main__":
    # Housekeeping
    logging.basicConfig(
        level="DEBUG" if DEBUG else "INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(omit_repeated_times=False)],
    )
    # Do a dummy initialisation of the database here, so we can request that the tables be dropped.
    RosterDatabase(drop_tables = True)
    # First, import the roster from the roster directory. This takes care of any roster changes that may have occurred whilst we were not running
    importer.process_existing_files(DIRECTORY_ROSTER)
    # Only watch for roster changes if specified.
    if MONITOR_CHANGES:
        RosterWatcher().watch(DIRECTORY_ROSTER, callback=callback)



# TODO: Maybe filter what goes into the dict in future? Do we need to?
# class SkipValuesSection:

#     def __call__(self, path, key, value):
#         logging.debug("Path: %s\n-----", path)
#         # if key is not "values":
#         return key, value
#         # return None