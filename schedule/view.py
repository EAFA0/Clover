import json
from flask import request
from clover import app


@app.route("/schedule/<user_id>", methods=["GET", "POST", "PUT", "DELETE"])
def schedule(user_id):
    if request.method == "GET":
        return json.dumps([
            {"content": "1"},
            {"content": "2"},
            {"content": "3"}
        ])
    elif request.method == "POST":
        return user_id
