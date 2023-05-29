import json
import time
from datetime import datetime

from pymongo import MongoClient

from constant.constant import CLOSED, IN_PROGRESS, MONGO_DB_URL, OPEN


class ProjectBoardBase(object):
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    def __init__(self) -> None:
        self.team_db = MongoClient(MONGO_DB_URL)["factwise"]["team"]
        self.user_db = MongoClient(MONGO_DB_URL)["factwise"]["user"]
        self.board_db = MongoClient(MONGO_DB_URL)["factwise"]["board"]

    # create a board
    def create_board(self, request: dict):
        """
        :param request: A json string with the board details.
        {
                "name" : "<board_name>",
                "description" : "<description>",
                "team_id" : "<team id>"
                "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
            * board name must be unique for a team
            * board name can be max 64 characters
            * description can be max 128 characters
        """
        request["creation_time"] = datetime.now()
        request["board_id"] = f"BOARD{int(time.mktime(datetime.now().timetuple()))}"
        request["status"] = OPEN
        request["tasks"] = []
        self.board_db.insert_one(request)
        return {"status": True, "message": "Board created Successfully!", "board_id":request["board_id"]}

    # close a board
    def close_board(self, request: str) -> dict:
        """
        :param request: A json string with the user details
        {
            "id" : "<board_id>"
        }

        :return:

        Constraint:
            * Set the board status to CLOSED and record the end_time date:time
            * You can only close boards with all tasks marked as COMPLETE
        """
        board = self.board_db.find_one({"board_id": request})
        if not board:
            return {"status": False, "message": f"{request} This board dosen't exist"}
        is_any_task_in_complete = False
        if len(board.get("tasks", [])) > 0:
            for task in board.get("tasks", []):
                if task.get("status", "") == [IN_PROGRESS, OPEN]:
                    is_any_task_in_complete = True
            if is_any_task_in_complete:
                return {
                    "status": False,
                    "message": f"Task is not complted yet please complete the task and then close this board {request}",
                }
            self.board_db.update_many({"board_id": request}, {"$set": {"status": CLOSED}})
            return {"status": True, "message": f"Task is close {request}"}
        self.board_db.update_many({"board_id": request}, {"$set": {"status": CLOSED}})
        return {"status": True, "message": "This board don't have any task; Closed this board"}

    # add task to board
    def add_task(self, request: dict) -> dict:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
                "title" : "<board_name>",
                "description" : "<description>",
                "user_id" : "<team id>"
                "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
            * task title must be unique for a board
            * title name can be max 64 characters
            * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        board_name = request.get("title", "")
        del request["title"]
        request["task_id"] = f"TASK{int(time.mktime(datetime.now().timetuple()))}"
        request["creation_time"] = datetime.now()
        request["status"] = OPEN
        self.board_db.update_one({"name": board_name}, {"$addToSet": {"tasks": request}})
        return {"status": True, "message": "Task created", "id": request["task_id"]}

    # update the status of a task
    def update_task_status(self, request: dict):
        """
        :param request: A json string with the user details
        {
                "id" : "<task_id>",
                "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        self.board_db.update_many(
            {"tasks.$.task_id": request.get("id", "")}, {"$set": {"tasks.$.status": request.get("status", "")}}
        )
        return {"status": True, "message": "Updated task status!"}

    # list all open boards for a team
    def list_boards(self, request: str) -> dict:
        """
        :param request: A json string with the team identifier
        {
            "id" : "<team_id>"
        }

        :return:
        [
            {
                "id" : "<board_id>",
                "name" : "<board_name>"
            }
        ]
        """
        board_details = list(self.board_db.find({"team_id": request}, {"board_id": 1, "_id": 0, "name": 1}))
        if len(board_details) > 0:
            return {"status": True, "boards": board_details}
        return {"status": False, "message": f"Board not found fot his team id {request}"}

    def export_board(self, request: str) -> dict:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
            "id" : "<board_id>"
        }
        :return:
        {
            "out_file" : "<name of the file created>"
        }
        """
        board = self.board_db.find_one({"board_id": request}, {"_id": 0})
        if board:
            board["creation_time"] = datetime.strftime(board["creation_time"], "%c")
            for task in board.get("tasks", []):
                task["creation_time"] = datetime.strftime(task["creation_time"], "%c")
            json_object = json.dumps(board, indent=4)
            file_name = f"{request}.txt"
            with open(f"out/{file_name}", "w") as outfile:
                outfile.write(json_object)
            return {"out_file": file_name}
        return {"status": False, "message": "Board not found please try with different board id"}
