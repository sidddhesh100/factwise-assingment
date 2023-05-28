from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL


class TeamSchema(Schema):
    name = fields.Str(validate=Length(max=64))
    description = fields.Str(validate=Length(max=128))
    admin = fields.Str(
        validate=OneOf(choices=MongoClient(MONGO_DB_URL)["factwise"]["user"].distinct("user_id"), error="Invalide user id"),
    )


class UpdateTeamSchema(Schema):
    id = fields.Str(
        required=True,
        validate=OneOf(choices=MongoClient(MONGO_DB_URL)["factwise"]["team"].distinct("team_id"), error="User id not exist"),
    )
    team = fields.Nested(TeamSchema, required=True)
