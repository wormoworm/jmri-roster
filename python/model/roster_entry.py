from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField, SqliteDatabase

db = SqliteDatabase("roster.db")

class RosterEntry(Model):

    # Required properties.
    roster_id= CharField(primary_key=True)
    dcc_address: IntegerField()
    
    # Optional properties.
    number = IntegerField(null=True)
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
    

# class RosterEntryFunction:

#     roster_entry = ForeignKeyField(RosterEntry)
#     roster_function = ForeignKeyField(RosterFunction)

#     class Meta:
#         database = db

    # number: int
    # name: str
    # lockable: bool

    # def __init__(self, number: int, name: str, lockable: bool):
    #     self.number = number
    #     self.name = name
    #     self.lockable = lockable