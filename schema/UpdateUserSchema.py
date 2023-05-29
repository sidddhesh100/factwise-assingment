from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length


class UserSchema(Schema):
    name = fields.Str(validate=Length(max=64, min=1))
    display_name = fields.Str(validate=Length(max=128))
    description = fields.Str(validate=Length(max=128))


class UpdateUserSchema(Schema):
    id = fields.Str(
        required=True,
        validate=Length(equal=14),
    )
    user = fields.Nested(UserSchema, required=True, validate=Length(min=1))

    @validates_schema
    def validate_update_user_schema(self, data, **kwargs):
        if data.get("id") and data.get("id") not in current_app.config["DB_CONN"]["factwise"]["user"].distinct("user_id"):
            raise ValidationError("User id not exist")
        if data.get("user", {}).get("name") and data.get("user", {}).get("name") in current_app.config["DB_CONN"]["factwise"][
            "user"
        ].distinct("name"):
            raise ValidationError("user name already exist")
