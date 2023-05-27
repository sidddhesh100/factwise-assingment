from marshmallow import Schema, fields
from marshmallow.validate import Length


class CreateUserSchema(Schema):
    name = fields.Str(required=True, validate=Length(max=64))
    display_name = fields.Str(required=True, validate=Length(max=128))
    description = fields.Str(required=True, validate=Length(max=128))
