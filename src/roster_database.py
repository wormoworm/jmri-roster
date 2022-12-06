from peewee import *
from roster_entry import RosterEntry, RosterFunction
from playhouse.shortcuts import model_to_dict
from typing import List
from utils import ROSTER_DATABASE_LOCATION
import logging

class RosterDatabase:

    db = SqliteDatabase(ROSTER_DATABASE_LOCATION, pragmas={'foreign_keys': 1})

    def __init__(self, drop_tables: bool = False):
        if drop_tables:
            # If requested, remove any existing tables. This allows us to change database structure between versions without having to worry about migrations.
            logging.info("Removing existing tables...")
            self.db.drop_tables([RosterEntry, RosterFunction])
        self.db.create_tables([RosterEntry, RosterFunction])

    def close(self):
        self.db.close()

    def insert_roster_entry(self, entry: RosterEntry):
        # Delete the roster entry and associated functions if they already exist. This is pretty hacky,
        # but there doesn't seem to be any UPSERT-type functionality with the save() function in Peewee.
        # To get UPSERT, I would need to pass in the raw parameters and build the object here, which is also a but ugly.
        self.delete_roster_entry_and_functions(entry.roster_id)
        entry.save(force_insert=True)

    def insert_roster_entry_function(self, function: RosterFunction):
        function.save()

    def get_roster_entries(self, owner: str = None, manufacturer: str = None, model: str = None, classification: str = None, decoder: str = None):
        query = RosterEntry.select().order_by(RosterEntry.number)
        if owner:
            query = query.where(RosterEntry.owner == owner)
        if manufacturer:
            query = query.where(RosterEntry.manufacturer == manufacturer)
        if model:
            query = query.where(RosterEntry.model == model)
        if classification:
            query = query.where(RosterEntry.classification == classification)
        if decoder:
            query = query.where(RosterEntry.decoder == decoder)

        entries_array = []
        for entry in query.execute():
            entries_array.append(entry)
        return entries_array

    def get_roster_entry_by_id(self, roster_id: int) -> RosterEntry:
        return RosterEntry.get(RosterEntry.roster_id == roster_id)

    def get_roster_entry_by_address(self, dcc_address: str) -> RosterEntry:
        return RosterEntry.get(RosterEntry.dcc_address == dcc_address)
    
    def delete_roster_entry_and_functions(self, roster_id: int):
        RosterEntry.delete().where(RosterEntry.roster_id == roster_id).execute()
        RosterFunction.delete().where(RosterFunction.roster_entry == roster_id).execute()
    
    def get_owners(self) -> List[str]:
        return self.get_distinct_values(RosterEntry.owner)
    
    def get_manufacturers(self) -> List[str]:
        return self.get_distinct_values(RosterEntry.manufacturer)
    
    def get_models(self) -> List[str]:
        return self.get_distinct_values(RosterEntry.model)
    
    def get_classifications(self) -> List[str]:
        return self.get_distinct_values(RosterEntry.classification)
    
    def get_decoders(self) -> List[str]:
        return self.get_distinct_values(RosterEntry.decoder)

    def get_distinct_values(self, column) -> List[str]:
        entries = RosterEntry().select(column.distinct()).execute()
        return list(filter(None, map(lambda entry: model_to_dict(entry)[column.name], entries)))
    
    # def drop_tables(self):
    #     self.db.drop_tables((RosterEntry, RosterFunction))
    
    def clear_tables(self):
        RosterEntry.delete().execute()
        RosterFunction.delete().execute()