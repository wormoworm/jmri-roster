from peewee import *
from roster_entry import RosterEntry, RosterFunction
from playhouse.shortcuts import model_to_dict
import json

class RosterDatabase:

    db = SqliteDatabase("roster.db", pragmas={'foreign_keys': 1})

    def __init__(self):
        self.db.connect()
        self.db.create_tables([RosterEntry, RosterFunction])

    def close(self):
        self.db.close()

    def insert_roster_entry(self, entry: RosterEntry):
        entry.save(force_insert=True)

    def insert_roster_entry_function(self, function: RosterFunction):
        function.save()

    def get_all_roster_entries(self):
        return RosterEntry.select().join(RosterFunction)

    def get_roster_entry_by_id(self, roster_id: str) -> RosterEntry:
        return RosterEntry.get_or_none(RosterEntry.roster_id == roster_id)

    def get_roster_entry_by_address(self, dcc_address: str) -> RosterEntry:
        return RosterEntry.get_or_none(RosterEntry.dcc_address == dcc_address)
    
    def clear_all_data(self):
        RosterEntry.delete().execute()
        RosterFunction.delete().execute()

if __name__ == "__main__":
    roster_db = RosterDatabase()
    roster_db.clear_all_data()
    test_entry = RosterEntry(roster_id="123", dcc_address="456", name="test_name")
    test_function_1 = RosterFunction(roster_entry="123", number="1", name="F1", lockable=True)
    test_function_2 = RosterFunction(roster_entry="123", number="2", name="F2", lockable=False)
    roster_db.insert_roster_entry(test_entry)
    roster_db.insert_roster_entry_function(test_function_1)
    roster_db.insert_roster_entry_function(test_function_2)

    entry = roster_db.get_roster_entry_by_id("123")
    print(json.dumps(model_to_dict(entry, backrefs=True), indent=4))