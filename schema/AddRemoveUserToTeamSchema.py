from marshmallow import Schema, fields


class AddRemoveUserToTeamSchema(Schema):
    id = fields.Str(required=True)
    users = fields.List(fields.Str(), required=True)
