import json

from flask import Blueprint, Response, request
from marshmallow import ValidationError

from constant import APPLICATION_JSON_MIME_TYPE
from schema.CreateUserSchema import CreateUserSchema
from schema.UpdateUserSchema import UpdateUserSchema
from user_base import UserBase

user = Blueprint(name="user", import_name=__name__, url_prefix="/user")


@user.route("/create_user/", methods=["POST"])
def create_user():
    body = request.get_json()
    try:
        CreateUserSchema.load(body)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = UserBase.create_user(body)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@user.route("/get_user_list/", methods=["GET"])
def get_user_list():
    response = UserBase.list_users()
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@user.route("/describe_user/", methods=["GET"])
def describe_user():
    user_id = request.args.get("id")
    response = UserBase.describe_user(user_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@user.route("/update_user/", methods=["PUT"])
def update_user():
    body = request.get_json()
    try:
        UpdateUserSchema
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = UserBase.update_user(body)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@user.route("/get_team_details_for_user", methods=["GET"])
def get_users_team():
    user_id = request.args.get("id", "")
    response = UserBase.get_user_teams(user_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)
