from marshmallow import Schema, fields


class AddRemoveUserToTeamSchema(Schema):
    id = fields.Str(required=True)
    user = fields.List(fields.Str(), required=True)
