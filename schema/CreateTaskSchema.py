from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class CreateTaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=Length(min=1),
    )
    description = fields.Str(required=True, validate=Length(max=128))
    user_id = fields.Str(required=True, validate=Length(equal=14))

    @validates_schema
    def validate_user_id(self, data, **kwargs):
        board = current_app.config["DB_CONN"]["factwise"]["board"].find_one({"name": data.get("title", "")})
        if data.get("user_id") not in current_app.config["DB_CONN"]["factwise"]["team"].distinct(
            "users.user_id", {"team_id": board.get("team_id")}
        ):
            raise ValidationError("user_id not belong to the team to whom the board is assigned")
        if data.get("title") not in current_app.config["DB_CONN"]["factwise"]["board"].distinct("name"):
            raise ValidationError("Board not available for the requested title")
