import time
from datetime import datetime

from pymongo import MongoClient

from constant import MONGO_DB_URL


class UserBase(object):
    """
    Base interface implementation for API's to manage users.
    """

    def __init__(self) -> None:
        self.team_db = MongoClient(MONGO_DB_URL)["factwise"]["team"]
        self.user_db = MongoClient(MONGO_DB_URL)["factwise"]["user"]

    # create a user
    def create_user(self, request: dict) -> dict:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        request["user_id"] = f"USER{int(time.mktime(datetime.now().timetuple()))}"
        request["creation_time"] = datetime.now()
        self.user_db.insert(request)
        return {"status": True, "message": "User created!", "id": request["user_id"]}

    # list all users
    def list_users(self) -> dict:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        user_list = self.user_db.find({}, {"_id": 0, "name": 1, "display_name": 1, "creation_time": 1})
        if len(user_list) > 0:
            return {"status": True, "users": user_list}
        return {"status": False, "message": "User not found. Please create a users"}

    # describe user
    def describe_user(self, request: str) -> dict:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        user = self.user_db.find({"user_id": request}, {"_id": 0, "name": 1, "description": 1, "creation_time": 1})
        if user:
            return {"status": True, "user": user}
        return {"status": False, "message": f"User not found for this user id{request}"}

    # update user
    def update_user(self, request: dict) -> dict:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        user_id = request.get("id", "")
        updated_details = request.get("user", {})
        self.user_db.update({"user_id": user_id}, {"$set": updated_details})
        return {"status": True, "message": "Details updated!"}

    def get_user_teams(self, request: str) -> dict:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        team = self.team_db.find({"user.[].use_id": request}, {"name": 1, "description": 1, "creation_time": 1, "_id": 0})
        if team:
            return {"status": True, "team_details": team}
        return {"status": True, "message": f"Team not found for this user id {request}"}
