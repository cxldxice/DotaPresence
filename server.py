import flask
import json
from flask import Flask, \
    redirect, render_template, request



app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        json_data = json.loads(request.data)

        with open("info.json", "w") as info_file:
            json.dump(json_data, info_file)
        

    return "0"


if __name__ == "__main__":
    print("[+] Server started!")
    app.run(port=6768)