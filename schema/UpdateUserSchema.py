# from flask import current_app
from marshmallow import Schema, fields
from marshmallow.validate import Length, NoneOf, OneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL


class UserSchema(Schema):
    name = fields.Str(
        validate=[
            Length(max=64),
            NoneOf(iterable=MongoClient(MONGO_DB_URL)["factwise"]["user"].distinct("name"), error="user name already exist"),
        ]
    )
    display_name = fields.Str(validate=Length(max=128))
    description = fields.Str(validate=Length(max=128))


class UpdateUserSchema(Schema):
    id = fields.Str(
        required=True,
        validate=OneOf(choices=MongoClient(MONGO_DB_URL)["factwise"]["user"].distinct("user_id"), error="User id not exist"),
    )
    user = fields.Nested(UserSchema, required=True)
