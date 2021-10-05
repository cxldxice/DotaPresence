import flask
import json
from flask import Flask, request

app = Flask(__name__)
data = {"dota": {}}


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        print("[+] Data recived")
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
