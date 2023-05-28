from marshmallow import Schema, fields
from marshmallow.validate import Length, NoneOf, OneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL


class CreateBoardSchema(Schema):
    name = fields.Str(
        required=True,
        validate=[
            Length(max=64),
            NoneOf(iterable=MongoClient(MONGO_DB_URL)["factwise"]["board"].distinct("name"), error="Board name already exist"),
        ],
    )
    description = fields.Str(required=True, validate=Length(max=128))
    team_id = fields.Str(
        required=True,
        validate=[
            # NoneOf(
            #     iterable=MongoClient(MONGO_DB_URL)["factwise"]["board"].distinct("team_id"),
            #     error="team alredy had a board please enter different team id ",
            # ),
            OneOf(choices=MongoClient(MONGO_DB_URL)["factwise"]["team"].distinct("team_id"), error="Team id does not exist"),
        ],
    )
