from marshmallow import Schema, fields
from marshmallow.validate import Length, NoneOf, OneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL

# from flask import current_app


class CreateTeamSchema(Schema):
    name = fields.Str(
        required=True,
        validate=[
            Length(max=64),
            NoneOf(iterable=MongoClient(MONGO_DB_URL)["factwise"]["team"].distinct("name"), error="team name already exist"),
        ],
    )
    description = fields.Str(required=True, validate=Length(max=128))
    admin = fields.Str(
        required=True,
        validate=[
            OneOf(
                choices=MongoClient(MONGO_DB_URL)["factwise"]["user"].distinct("user_id"),
                error="Invalid user id; Admin Id not available in db",
            ),
            NoneOf(iterable=MongoClient(MONGO_DB_URL)["factwise"]["team"].distinct("admin"), error="admin already has a team"),
        ],
    )
