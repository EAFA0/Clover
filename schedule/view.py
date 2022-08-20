from flask import request
from clover import app


@app.route("/schedule/<user_id>", methods=["GET", "POST", "PUT", "DELETE"])
def schedule(user_id):
    if request.method == "GET":
        return "ok"
    elif request.method == "POST":
        return user_id
