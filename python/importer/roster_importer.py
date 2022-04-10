import os
import logging
import json
from turtle import end_fill
from typing import OrderedDict
from isort import file
import xmltodict
from model.roster_entry import RosterEntry, RosterFunction
from model.roster_database import RosterDatabase

def does_file_exist(path):
    return os.path.isfile(path)

class RosterImporter:

    roster_db = RosterDatabase()

    def process_existing_files(self, roster_directory: str):
        logging.debug("Scanning for existing files in %s", roster_directory)
        for file in os.listdir(roster_directory):
            self.process_file(roster_directory + "/" + file)

    def process_file(self, file_path):
        logging.debug("About to process file: %s", os.path.abspath(file_path))
        # Check the file still exists. The file watcher seems to deliver multiple events per file change, and they seem to all arrive at the same time. So after we have moved the file during the first call to this function, the file will no longer exist.
        if not does_file_exist(file_path):
            return None
        with open(file_path, encoding="utf-8") as file:
            # xml_dict = parse(file.read(), postprocessor=SkipValuesSection())
            file_dict = xmltodict.parse(file.read())
            # logging.debug("File contents:\n----------%s\n----------", json.dumps(file_dict, indent=4))
            self.import_roster_entry_from_dict(file_dict)
    
    def import_roster_entry_from_dict(self, roster_dict: dict):
        locomotive = roster_dict["locomotive-config"]["locomotive"]
        # logging.debug(json.dumps(locomotive, indent=4))
        roster_entry = RosterEntry(
            roster_id=locomotive.get("@id"),
            dcc_address=locomotive.get("@dccAddress"),
            number=locomotive.get("@roadNumber"),
            manufacturer=locomotive.get("@mfg"),
            model=locomotive.get("@model"),
            owner=locomotive.get("@owner"),
            comment=locomotive.get("@comment")
        )

        # Check for any extra attributes
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
        logging.debug("AP type: %s", type(locomotive.get("attributepairs").get("keyvaluepair")))
        
        # TODO: Functions
        # roster_entry = RosterEntry(roster_id=locomotive.get("@id"))
        self.roster_db.insert_roster_entry(roster_entry)
        # logging.debug(roster_entry)
    
    def process_key_value_pair(self, pair: dict, roster_entry: RosterEntry):
        logging.debug("KVP key: %s", pair["key"])
        if pair["key"] == "Name":
            roster_entry.name = pair["value"]
        elif pair["key"] == "OperatingDuration":
            roster_entry.operating_duration = pair["value"]
        elif pair["key"] == "LastOperated": # TODO: Convert to epoch seconds.
            roster_entry.last_operated = pair["value"]


# TODO: Maybe filter what goes into the dict in future? Do we need to?
# class SkipValuesSection:

#     def __call__(self, path, key, value):
#         logging.debug("Path: %s\n-----", path)
#         # if key is not "values":
#         return key, value
#         # return None