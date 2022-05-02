from peewee import *
from roster_entry import RosterEntry, RosterFunction, ROSTER_DATABASE_LOCATION
from playhouse.shortcuts import model_to_dict
import json

class RosterDatabase:

    db = SqliteDatabase(ROSTER_DATABASE_LOCATION, pragmas={'foreign_keys': 1})

    def __init__(self):
        # self.db.connect()
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

    def get_all_roster_entries(self):
        return list(RosterEntry.select().order_by(RosterEntry.number))

    def get_roster_entry_by_id(self, roster_id: int) -> RosterEntry:
        return RosterEntry.get_or_none(RosterEntry.roster_id == roster_id)

    def get_roster_entry_by_address(self, dcc_address: str) -> RosterEntry:
        return RosterEntry.get_or_none(RosterEntry.dcc_address == dcc_address)
    
    def delete_roster_entry_and_functions(self, roster_id: int):
        RosterEntry.delete().where(RosterEntry.roster_id == roster_id).execute()
        RosterFunction.delete().where(RosterFunction.roster_entry == roster_id).execute()
    
    def clear_all_data(self):
        RosterEntry.delete().execute()
        RosterFunction.delete().execute()