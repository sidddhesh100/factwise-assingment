from marshmallow import Schema, fields
from marshmallow.validate import Length, NoneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL


class CreateUserSchema(Schema):
    name = fields.Str(
        required=True,
        validate=[
            Length(max=64),
            NoneOf(iterable=MongoClient(MONGO_DB_URL)["factwise"]["user"].distinct("name"), error="user name already exist"),
        ],
    )
    display_name = fields.Str(required=True, validate=Length(max=128))
    description = fields.Str(required=True, validate=Length(max=128))
