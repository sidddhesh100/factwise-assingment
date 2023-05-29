from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class CreateUserSchema(Schema):
    name = fields.Str(required=True, validate=Length(max=64, min=1))
    display_name = fields.Str(required=True, validate=Length(max=128))
    description = fields.Str(required=True, validate=Length(max=128))

    @validates_schema
    def validate_create_user_schema(self, data, **kwargs):
        if data.get("name") in current_app.config["DB_CONN"]["factwise"]["user"].distinct("name"):
            raise ValidationError("user name already exist")
