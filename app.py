from flask import Flask
from pymongo import MongoClient

from blueprint.team import team
from blueprint.user import user
from constant import MONGO_DB_URL

app = Flask(__name__)
# app.config["DB_CONN"] = MongoClient(MONGO_DB_URL)
# app.config["FACTWISE"] = app.config["DB_CONN"]["factwise"]


@app.route("/")
def home():
    return "Welcome!"


# register blueprints
app.register_blueprint(user)
app.register_blueprint(team)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
