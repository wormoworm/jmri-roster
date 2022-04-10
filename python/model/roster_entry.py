from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField, SqliteDatabase

db = SqliteDatabase("roster.db")

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
        return self.image_file_path is not None

class RosterFunction(Model):

    roster_entry = ForeignKeyField(RosterEntry, backref="functions")
    number = IntegerField()
    name = CharField()
    lockable = BooleanField(null=True)

    class Meta:
        database = db