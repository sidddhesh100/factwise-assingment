from marshmallow import Schema, fields
from marshmallow.validate import Length, NoneOf, OneOf

# from flask import current_app


class CreateTeamSchema(Schema):
    name = fields.Str(required=True, validate=Length(max=64))
    # NoneOf(iterable=current_app.config["factwise"]["team"].distinct("team_name"), error="team name already exist")])
    description = fields.Str(required=True, validate=Length(max=128))
    admin = fields.Str(
        required=True,
    )
    #    validate=OneOf(choices=current_app.config["factwise"]["user"].distinct("user_id"), error="Invalide user id"))
