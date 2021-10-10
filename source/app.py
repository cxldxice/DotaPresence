#               DotaPresence
#         by @clxdxice & @Xorsiphus
#             rewrite version

# DEBUG: GET > http://127.0.0.1:6768/?mode=debug
# UPTIME: GET > http://127.0.0.1:6768/
# RECIVE DATA: POST > http://127.0.0.1:6768/

import json
import time
import psutil
import logging
import threading
import pypresence

from flask import Flask, \
    request

from ApiClient.RestClient import RestClient

start = time.time()
server = Flask(__name__)
rich_presence = pypresence.Presence(client_id="894510564817121301", pipe=0)
rich_presence.connect()

logging.getLogger('werkzeug').setLevel(logging.ERROR)  # disable logs from flask

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
            return f"<h1>Uptime</h1> <h4>{time.time() - start}</h4>"


def start_listening():
    try:
        threading.Thread(target=server.run, args=("127.0.0.1", 6768), daemon=True).start()  # run server in 2nd thread

        return True
    except:
        return False


def is_open(process):
    return process in (p.name() for p in psutil.process_iter())


def get_name(dota_name):
    name = dota_name.replace("npc_dota_hero_", "").replace("_", " ")
    name = name[0].upper() + name[1:]

    return name


def check_pause(map_obj):
    return map_obj["paused"]


def get_kda(player_obj):
    return f'{player_obj["kills"]}/{player_obj["deaths"]}/{player_obj["assists"]}'


def in_match():
    if time.time() < data["update"] + 10:
        try:
            data["dota"]["hero"]

            return True
        except:
            pass

    return False


def main():
    start_listening()
    counter = 0

    while True:
        if is_open("dota2.exe"):
            if in_match():
                if check_pause(data["dota"]["map"]):
                    while True:
                        try:
                            if not check_pause(data["dota"]["map"]):
                                break

                            time.sleep(15)
                        except:
                            break

                    continue

                data["game"] = True

                try:
                    image = data["dota"]["hero"]["name"]
                    clock = time.time() - data["dota"]["map"]["clock_time"]
                    name = get_name(data["dota"]["hero"]["name"])
                    kda = get_kda(data["dota"]["player"])
                    level = data["dota"]["hero"]["level"]
                    profile_id = int(data["dota"]["player"]["steamid"]) - 76561197960265728

                except:
                    continue

                rich_presence.update(
                    details=f"Playing on {name}",
                    state=kda,
                    large_image=image,
                    small_image=str(level),
                    small_text="level:  " + str(level),
                    large_text="hero: " + name,
                    start=clock,
                    buttons=[
                        {"label": "View profile", "url": f"https://stratz.com/players/{profile_id}"},
                        {"label": "Download DotaPresence", "url": "https://github.com/cxldxice/DotaPresence"}
                    ]
                )

            else:
                data["game"] = False

                rich_presence.update(
                    details=f"with DotaPresence",
                    large_image="dota2icon",
                    buttons=[
                        {"label": "Download DotaPresence", "url": "https://github.com/cxldxice/DotaPresence"}
                    ]
                )

            # Где то тут будет проверка на сорев матч и отправка на сервер раз в минуту
            # if counter == 3:
            #     RestClient.send(data["dota"], "Dev")
            #     counter = (counter + 1) % 4

            time.sleep(15)
        else:
            rich_presence.clear()
            time.sleep(60)


if __name__ == "__main__":
    main()
