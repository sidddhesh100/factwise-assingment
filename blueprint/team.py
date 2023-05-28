import json

from flasgger import swag_from
from flask import Blueprint, Response, current_app, request
from marshmallow import ValidationError

from constant import APPLICATION_JSON_MIME_TYPE
from schema.AddRemoveUserToTeamSchema import AddRemoveUserToTeamSchema
from schema.CreateTeamSchema import CreateTeamSchema
from schema.UpdateTeamSchema import UpdateTeamSchema
from team_base import TeamBase

team = Blueprint(name="team", import_name=__name__, url_prefix="/team")
team_base = TeamBase()


@swag_from("../documentation/team/create_team.yml")
@team.route("/create_team/", methods=["POST"])
def create_team():
    data = request.get_json()
    current_app.logger.info(f"request: {data}")
    try:
        CreateTeamSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = team_base.create_team(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/get_team_list.yml")
@team.route("/get_team_list/", methods=["GET"])
def get_team_list():
    team_list = team_base.list_teams()
    return Response(json.dumps(team_list), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/describe_team.yml")
@team.route("/describe_team/", methods=["GET"])
def describe_team():
    team_id = request.args.get("id")
    response = team_base.describe_team(team_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/update_team.yml")
@team.route("/update_team/", methods=["PUT"])
def update_team():
    data = request.get_json()
    try:
        UpdateTeamSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = team_base.update_team(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/add_users_to_team.yml")
@team.route("/add_users_to_team/", methods=["POST"])
def add_users_to_team():
    data = request.get_json()
    try:
        AddRemoveUserToTeamSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = team_base.add_users_to_team(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/remove_users_from_team.yml")
@team.route("/remove_users_from_team/", methods=["DELETE"])
def remove_users_from_team():
    data = request.get_json()
    try:
        AddRemoveUserToTeamSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = team_base.remove_users_from_team(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/team/list_team_user.yml")
@team.route("/list_team_user/", methods=["GET"])
def list_team_user():
    team_id = request.args.get("id", "")
    response = team_base.list_team_users(team_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)
