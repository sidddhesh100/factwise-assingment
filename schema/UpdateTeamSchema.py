from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class TeamSchema(Schema):
    name = fields.Str(validate=Length(max=64))
    description = fields.Str(validate=Length(max=128))
    admin = fields.Str(validate=Length(equal=14))


class UpdateTeamSchema(Schema):
    id = fields.Str(
        required=True,
        validate=Length(equal=14),
    )
    team = fields.Nested(TeamSchema, required=True, validate=Length(min=1))

    @validates_schema
    def validate_update_team_schema(self, data, **kwargs):
        if data.get("id") and data.get("id") not in current_app.config["DB_CONN"]["factwise"]["team"].distinct("team_id"):
            raise ValidationError("Invalid team id")
        if data.get("team", {}).get("admin") and data.get("team", {}).get("admin") not in current_app.config["DB_CONN"][
            "factwise"
        ]["user"].distinct("user_id"):
            raise ValidationError("Invalid user id")
