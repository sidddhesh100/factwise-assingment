from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class CreateBoardSchema(Schema):
    name = fields.Str(required=True, validate=Length(max=64, min=1))
    description = fields.Str(required=True, validate=Length(max=128))
    team_id = fields.Str(required=True, validate=Length(equal=14))

    @validates_schema
    def validate_create_board_schema(self, data, **kwargs):
        if data.get("name") and data.get("name") in current_app.config["DB_CONN"]["factwise"]["board"].distinct("name"):
            raise ValidationError("Board name already exist")
        if data.get("team_id") and data.get("team_id") not in current_app.config["DB_CONN"]["factwise"]["team"].distinct(
            "team_id"
        ):
            raise ValidationError("Team id does not exist")
