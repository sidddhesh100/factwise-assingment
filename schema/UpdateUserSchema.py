# from flask import current_app
from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class UserSchema(Schema):
    name = fields.Str(validate=Length(max=64))
    display_name = fields.Str(validate=Length(max=128))


class UpdateUserSchema(Schema):
    id = fields.Str(required=True)
    user = fields.Nested(UserSchema, required=True)
