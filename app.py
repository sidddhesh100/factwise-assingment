from flasgger import Swagger
from flask import Flask, redirect, request
from pymongo import MongoClient

from blueprint.project_board import project_board
from blueprint.team import team
from blueprint.user import user

app = Flask(__name__)
app.config["DB_CONN"] = MongoClient("mongodb://localhost:27017")


@app.route("/")
def home():
    return redirect(f"{request.url}apidocs")


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Factwise Assingment",
        "description": "This service provides APIs for Team, User, Board and Task Managements",
        "contact": {
            "email": "siddheshangane142000@gmail.com",
        },
    },
    # "host": "http://localhost:5008",
    "schemes": ["http", "https"],
}

swagger = Swagger(app, template=SWAGGER_TEMPLATE)

# register blueprints
app.register_blueprint(user)
app.register_blueprint(team)
app.register_blueprint(project_board)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
