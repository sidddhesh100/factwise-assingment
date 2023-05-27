from marshmallow import Schema, fields
from marshmallow.validate import Length


class CreateTaskSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True, validate=Length(max=128))
    user_id = fields.Str(required=True)
