from peewee import SqliteDatabase, Model, CharField, DateTimeField, SmallIntegerField
from datetime import datetime

database = SqliteDatabase('MR.db')


class Music(Model):
    name = CharField(max_length=100)
    category = CharField(max_length=100)
    singer = CharField(max_length=100)
    album = CharField(max_length=100, default=None, null=True)
    rate = SmallIntegerField()
    created_time = DateTimeField(default=datetime.now(), null=True)

    class Meta:
        database = database


def create_tables():
    database.create_tables([Music])
