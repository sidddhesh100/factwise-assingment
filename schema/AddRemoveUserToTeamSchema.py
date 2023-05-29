from marshmallow import Schema, fields
from marshmallow.validate import Length


class AddRemoveUserToTeamSchema(Schema):
    id = fields.Str(required=True, validate=Length(equal=14))
    users = fields.List(fields.Str(), required=True, validate=Length(min=1))
