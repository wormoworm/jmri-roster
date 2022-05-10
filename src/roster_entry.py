import os
import pathlib
from datetime import datetime, timedelta
from xmlrpc.client import DateTime
from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField, SqliteDatabase
from utils import *

db = SqliteDatabase(ROSTER_DATABASE_LOCATION)

class RosterEntry(Model):

    # Required properties.
    roster_id = CharField(primary_key=True)
    dcc_address = CharField()
    
    # Optional properties.
    number = CharField(null=True)
    name = CharField(null=True)
    manufacturer = CharField(null=True)
    model = CharField(null=True)
    owner = CharField(null=True)
    comment = CharField(null=True)
    image_file_path = CharField(null=True)
    operating_duration = IntegerField(null=True)
    last_operated = IntegerField(null=True)

    class Meta:
        database = db
    
    # TODO: has_image should optionally fallback to using image file on disk.

    # TODO: Provide get_image() function, which optionally falls back to using image files from disk.

    def get_image_file_full_path(self, search_files: bool = True):
        if self.image_file_path:
            return f"{DIRECTORY_ROSTER}/{self.image_file_path}"
        elif search_files:
            image_file_full_path = search_for_roster_entry_image(self.roster_id)
            if image_file_full_path:
                return image_file_full_path
        return None


    def has_image(self, search_files: bool = True) -> bool:
        return self.get_image_file_full_path(search_files) is not None
        

    def get_friendly_id(self) -> str:
        if self.number:
            return self.number
        return self.id


    def operating_duration_hms(self) -> str:
        return "{:0>8}".format(str(timedelta(seconds=self.operating_duration)))
    

    def last_operated_datetime(self) -> DateTime:
        if self.last_operated:
            return datetime.utcfromtimestamp(self.last_operated)
        return None

class RosterFunction(Model):

    roster_entry = ForeignKeyField(RosterEntry, backref="functions")
    number = IntegerField()
    name = CharField()
    lockable = BooleanField(null=True)

    class Meta:
        database = db