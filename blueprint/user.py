import json

from flasgger import swag_from
from flask import Blueprint, Response, request
from marshmallow import ValidationError

from constant import APPLICATION_JSON_MIME_TYPE
from schema.CreateUserSchema import CreateUserSchema
from schema.UpdateUserSchema import UpdateUserSchema
from user_base import UserBase

user = Blueprint(name="user", import_name=__name__, url_prefix="/user")
user_base = UserBase()


@user.route("/create_user/", methods=["POST"])
@swag_from("../documentation/user/create_user.yml")
def create_user():
    data = request.get_json()
    try:
        CreateUserSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = user_base.create_user(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/user/get_user_list.yml")
@user.route("/get_user_list/", methods=["GET"])
def get_user_list():
    response = user_base.list_users()
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/user/describe_user.yml")
@user.route("/describe_user/", methods=["GET"])
def describe_user():
    user_id = request.args.get("id")
    response = user_base.describe_user(user_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/user/update_user.yml")
@user.route("/update_user/", methods=["PUT"])
def update_user():
    data = request.get_json()
    try:
        UpdateUserSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = user_base.update_user(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/user/get_team_details_for_user.yml")
@user.route("/get_team_details_for_user/", methods=["GET"])
def get_users_team():
    user_id = request.args.get("id", "")
    response = user_base.get_user_teams(user_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)
