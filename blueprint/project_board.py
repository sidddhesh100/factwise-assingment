import json

from flasgger import swag_from
from flask import Blueprint, Response, request
from marshmallow import ValidationError

from constant import APPLICATION_JSON_MIME_TYPE
from project_board_base import ProjectBoardBase
from schema.CreateBoardSchema import CreateBoardSchema
from schema.CreateTaskSchema import CreateTaskSchema
from schema.UpdateTaskStatusSchema import UpdateTaskStatusSchema

project_board = Blueprint(name="project_board", import_name=__name__, url_prefix="/project/board")
project_board_base = ProjectBoardBase()


@swag_from("../documentation/board/create_board.yml")
@project_board.route("/create_board/", methods=["POST"])
def create_board():
    data = request.get_json()
    try:
        CreateBoardSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = project_board_base.create_board(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/board/close_board.yml")
@project_board.route("/close_board/", methods=["GET"])
def close_board():
    board_id = request.args.get("id")
    response = project_board_base.close_board(board_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/board/add_task.yml")
@project_board.route("/add_task/", methods=["POST"])
def add_task():
    data = request.get_json()
    try:
        CreateTaskSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = project_board_base.add_task(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/board/update_task_status.yml")
@project_board.route("/update_task_status/", methods=["POST"])
def update_task_status():
    data = request.get_json()
    try:
        UpdateTaskStatusSchema().load(data)
    except ValidationError as err:
        return Response(json.dumps(err.messages))
    response = project_board_base.update_task_status(data)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/board/list_boards.yml")
@project_board.route("/list_boards/", methods=["GET"])
def list_boards():
    team_id = request.args.get("id")
    response = project_board_base.list_boards(team_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)


@swag_from("../documentation/board/export_board.yml")
@project_board.route("/export_board/", methods=["GET"])
def export_board():
    board_id = request.args.get("id", "")
    response = project_board_base.export_board(board_id)
    return Response(json.dumps(response), mimetype=APPLICATION_JSON_MIME_TYPE)
