import os
import pathlib
from datetime import datetime, timedelta
from xmlrpc.client import DateTime
from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField, SqliteDatabase

ROSTER_DATABASE_LOCATION = os.getenv("ROSTER_DATABASE_LOCATION", "/data/roster.db")
os.makedirs(os.path.dirname(ROSTER_DATABASE_LOCATION), exist_ok=True)

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

    def has_image(self) -> bool:
        if self.image_file_path:
            return True
        return False

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