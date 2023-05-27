import time
from datetime import datetime

from pymongo import MongoClient

from constant import MONGO_DB_URL


class TeamBase(object):
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    def __init__(self) -> None:
        self.team_db = MongoClient(MONGO_DB_URL)["factwise"]["team"]
        self.user_db = MongoClient(MONGO_DB_URL)["factwise"]["user"]

    # create a team
    def create_team(self, request: dict) -> dict:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        request["creation_time"] = datetime.now()
        request["team_id"] = f"TEAM{int(time.mktime(datetime.now().timetuple()))}"
        request["users"] = []
        self.team_db.insert_one(request)
        return {"status": True, "message": "Team created Successfully!"}

    # list all teams
    def list_teams(self) -> dict:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        teams_list = self.team_db.find_many({}, {"name": 1, "description": 1, "creation_time": 1, "admin": 1, "_id": 0})
        if len(teams_list) == 0:
            return {"status": False, "message": "Team are not available. Please create a new team"}
        return {"status": True, "team_list": teams_list}

    # describe team
    def describe_team(self, request: str) -> dict:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        response = self.team_db.find({"team_id": request}, {"name": 1, "description": 1, "creation_time": 1, "admin": 1, "_id": 0})
        if response is None:
            return {"status": False, "message": f"team not found for the this team id {request}"}
        return {"status": True, "team_details": response}

    # update team
    def update_team(self, request: dict) -> dict:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        team_id = request.get("team_id", "")
        updated_details = request.get("team", {})
        self.team_db.update({"team_id": team_id}, {"$set": updated_details})
        return {"status": True, "message": "Details updated Successfully!"}

    # add users to team
    def add_users_to_team(self, request: dict):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        team_id = request.get("id", "")
        users_id_list = request.get("users", [])
        available_user_list = []
        unavailable_user_list = []
        for user_id in users_id_list:
            user = self.user_db.find({"user_id": user_id})
            if user:
                data = {"user_name": user.get("name", ""), "user_id": user_id}
                available_user_list.append(data)
            else:
                unavailable_user_list.append(user_id)
        if len(available_user_list) > 0:
            self.team_db.update({"team_id": team_id}, {"$push": available_user_list})
        message = "User added successfully!"
        if len(unavailable_user_list) > 0:
            message = (
                f"{message} but this list of user id's are not available hence this user not updated for this team id {team_id}"
            )
        return {"status": True, "message": message}

    # add users to team
    def remove_users_from_team(self, request: dict):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        self.team_db.update({"team_id": request.get("id")}, {"$unset": {"users.$.user_id": {"$in": request.get("users", [])}}})
        return {"status": True, "message": "User are removed"}

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        team = self.team_db.find({"team_id": request})
        if team:
            return {"status": True, "user_list": team.get("users", [])}
        else:
            return {"status": False, "message": f"Team not found for this team id {request}"}
