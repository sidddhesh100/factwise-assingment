from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf

from constant.constant import COMPLETE, IN_PROGRESS, OPEN


class UpdateTaskStatusSchema(Schema):
    id = fields.Str(required=True, validate=Length(equal=14))
    status = fields.Str(
        required=True,
        validate=OneOf(
            choices=[OPEN, COMPLETE, IN_PROGRESS],
            error=f"Invalid task status; It should be one of these {OPEN}, {COMPLETE}, and {IN_PROGRESS}",
        ),
    )
