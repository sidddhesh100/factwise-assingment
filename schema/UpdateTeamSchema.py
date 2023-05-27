from flask import current_app
from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class TeamSchema(Schema):
    name = fields.Str(validate=Length(max=64))
    description = fields.Str(validate=Length(max=128))
    admin = fields.Str(
        required=True,
        #    validate=OneOf(choices=current_app.config["factwise"]["user"].distinct("user_id"), error="Invalide user id")
    )


class UpdateTeamSchema(Schema):
    id = fields.Str(required=True)
    team = fields.Nested(TeamSchema, required=True)
