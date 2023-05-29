from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class CreateTeamSchema(Schema):
    name = fields.Str(required=True, validate=Length(max=64, min=1))
    description = fields.Str(required=True, validate=Length(max=128))
    admin = fields.Str(required=True, validate=Length(equal=14))

    @validates_schema
    def validate_create_team_schema(self, data, **kwargs):
        if data.get("name") and data.get("name") in current_app.config["DB_CONN"]["factwise"]["team"].distinct("name"):
            raise ValidationError("User name already exist")
        if data.get("admin") and data.get("admin") not in current_app.config["DB_CONN"]["factwise"]["user"].distinct("user_id"):
            raise ValidationError("Invalid user id; Admin Id not available in db")
        if data.get("admin") and data.get("admin") in current_app.config["DB_CONN"]["factwise"]["team"].distinct("admin"):
            raise ValidationError("admin already has a team")
