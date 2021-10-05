import time

import flask
import json
from flask import Flask, request

app = Flask(__name__)

data = {"dota": {}}
timer = time.time()


@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        global timer
        timer = time.time()
        data["dota"] = json.loads(request.data)

        return flask.jsonify({"code": 200, "response": 1})

    else:
        return flask.jsonify({"code": 405, "error": "method not allowed"})


@app.route("/debug")
def debug():
    return flask.jsonify(data["dota"])


@app.route("/debug/<column>")
def debug_(column):
    return flask.jsonify(data["dota"][column])


def polling():
    print("[+] Server started")
    app.run(port=6768)


def get_connection_status():
    global timer
    if time.time() - timer < 60:
        return False
    else:
        return True


def get_data():
    return data["dota"]
