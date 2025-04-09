from peewee import *
from datetime import datetime

db = SqliteDatabase('db/currency.db')


class BaseModel(Model):
    class Meta:
        database = db


class ExchangeRate(BaseModel):
    currency = CharField(unique=True)
    rate = FloatField()
    updated_at = DateTimeField(default=datetime.now)
