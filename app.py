#               DotaPresence
#         by @clxdxice & @Xorsiphus
#             rewrite version

#DEBUG: GET > http://127.0.0.1:6768/?mode=debug
#UPTIME: GET > http://127.0.0.1:6768/
#RECIVE DATA: POST > http://127.0.0.1:6768/

import json
import time
import flask
import psutil
import logging
import threading

from flask import Flask, \
    request, jsonify

start = time.time()
server = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR) #disable logs from flask

data = {"dota": {}, "update": start, "game": False} 


@server.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data["dota"] = json.loads(request.data)
        data["update"] = time.time()

        return "0"
    
    else:
        if request.args.get("mode") == "debug":
            return json.dumps(data, indent=4, sort_keys=True)

        else:
            return f"<h1>Uptime</h1> <h4>{time.time()-start}</h4>"

def is_open(process):
    return process in (p.name() for p in psutil.process_iter())

def in_match():
    if time.time() < data["update"] + 5:
        try:
            data["dota"]["hero"]

            return True
        except:
            pass

    return False


def main():
    threading.Thread(target=server.run, args=("127.0.0.1", 6768), daemon=True).start() #run server in 2nd thread

    while True:
        if is_open("dota2.exe"):
            if in_match(): data["game"] = True
            else: data["game"] = False
   
            time.sleep(1)

        else:
            time.sleep(60)


if __name__ == "__main__": 
    main()