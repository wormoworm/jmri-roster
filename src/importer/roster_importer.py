import os
import pathlib
import logging
import json
from typing import OrderedDict
import xmltodict
from model.roster_entry import RosterEntry, RosterFunction
from model.roster_database import RosterDatabase
from playhouse.shortcuts import model_to_dict
from datetime import datetime

def does_file_exist(path):
    return os.path.isfile(path)

def roster_iso_time_string_to_epoch_second(iso_time: str) -> int:
    time_without_offset = iso_time.split("+")[0]
    utc_time = datetime.strptime(time_without_offset, "%Y-%m-%dT%H:%M:%S.%f")
    return (utc_time - datetime(1970, 1, 1)).total_seconds()
class RosterImporter:

    roster_db = RosterDatabase()
    
    def should_process_file(self, file_path: str):
        return pathlib.Path(file_path).suffix.lower() == ".xml"

    def process_existing_files(self, roster_directory: str):
        logging.debug("Scanning for existing files in %s", roster_directory)
        for file in os.listdir(roster_directory):
            self.process_file(roster_directory + "/" + file)

    def process_file(self, file_path):
        logging.debug("About to process file: %s", os.path.abspath(file_path))
        
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
            roster_id = int(locomotive.get("@id")),
            dcc_address = locomotive.get("@dccAddress"),
            number = locomotive.get("@roadNumber"),
            manufacturer = locomotive.get("@mfg"),
            model = locomotive.get("@model"),
            owner = locomotive.get("@owner"),
            comment = locomotive.get("@comment")
        )
        # Add the image file path, if set and not empty. We convert this to a path that is relative to the roster folder.
        locomotive_image_file_path = locomotive.get("@imageFilePath")
        if locomotive_image_file_path:
            roster_entry.image_file_path = locomotive.get("@imageFilePath").split("/")[-1]

        # Check for any extra attributes.
        try:
            key_value_pair = locomotive.get("attributepairs").get("keyvaluepair")
            if isinstance(key_value_pair, list):    # There is more than one key-value attribute to process.
                for key_value in key_value_pair:
                    self.process_key_value_pair(key_value, roster_entry)
            elif isinstance(key_value_pair, OrderedDict):
                self.process_key_value_pair(key_value_pair, roster_entry) # There is only one key-value attribute.
            else:
                logging.debug("KVP type (%s) not supported", type(key_value_pair))
        except KeyError as e:
            logging.error("Error getting KVPs: %s", e)

        self.roster_db.insert_roster_entry(roster_entry)
        
        # Also insert any functions.
        try:
            for function_json in locomotive.get("functionlabels").get("functionlabel"):
                function = RosterFunction()
                function.roster_entry = roster_entry.roster_id
                function.number = function_json.get("@num")
                function.name = function_json.get("#text")
                function.lockable = function_json.get("@lockable").lower() == "true"
                self.roster_db.insert_roster_entry_function(function)
        except KeyError as e:
            logging.error("Error getting functions: %s", e)

        logging.info("Imported entry with ID %s", roster_entry.roster_id)

        # entry = self.roster_db.get_roster_entry_by_id("66957")
        # print(json.dumps(model_to_dict(entry, backrefs=True), indent=4))
    
    def process_key_value_pair(self, pair: dict, roster_entry: RosterEntry):
        if pair["key"] == "Name":
            roster_entry.name = pair["value"]
        elif pair["key"] == "OperatingDuration":
            roster_entry.operating_duration = pair["value"]
        elif pair["key"] == "LastOperated": # TODO: Convert to epoch seconds.
            roster_entry.last_operated = roster_iso_time_string_to_epoch_second(pair["value"])


# TODO: Maybe filter what goes into the dict in future? Do we need to?
# class SkipValuesSection:

#     def __call__(self, path, key, value):
#         logging.debug("Path: %s\n-----", path)
#         # if key is not "values":
#         return key, value
#         # return None