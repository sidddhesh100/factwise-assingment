from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from constant import CLOSED, COMPLETE, IN_PROGRESS, OPEN


class UpdateTaskStatusSchema(Schema):
    id = fields.Str(required=True)
    status = fields.Str(
        required=True,
        validate=OneOf(
            choices=[OPEN, COMPLETE, IN_PROGRESS, CLOSED],
            error=f"Invalid task status; It should be one of these {OPEN}, {COMPLETE}, {IN_PROGRESS},  {CLOSED}",
        ),
    )
