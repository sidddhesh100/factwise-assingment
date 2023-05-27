from marshmallow import Schema, fields
from marshmallow.validate import Length


class CreateBoardSchema(Schema):
    name = fields.Str(required=True, validate=Length(64))
    description = fields.Str(required=True, validate=Length(128))
    team_id = fields.Str(required=True)
