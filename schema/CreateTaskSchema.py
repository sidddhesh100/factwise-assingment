from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length, OneOf
from pymongo import MongoClient

from constant import MONGO_DB_URL


class CreateTaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=OneOf(
            choices=MongoClient(MONGO_DB_URL)["factwise"]["board"].distinct("name"),
            error="Board not available for the requested title",
        ),
    )
    description = fields.Str(required=True, validate=Length(max=128))
    user_id = fields.Str(
        required=True,
    )

    @validates_schema
    def validate_user_id(self, data, **kwargs):
        board = MongoClient(MONGO_DB_URL)["factwise"]["board"].find_one({"name": data.get("title", "")})
        if data.get("user_id") not in MongoClient(MONGO_DB_URL)["factwise"]["team"].distinct(
            "users.user_id", {"team_id": board.get("team_id")}
        ):
            raise ValidationError("user_id not belong to the team to whom the board is assigned")
