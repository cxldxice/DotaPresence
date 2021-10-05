config_data = \
""""DotaPresence  Configuration"
{
    "uri"               "http://localhost:6768/"
    "timeout"           "15.0"
    "buffer"            "15.0"
    "throttle"          "15.0"
    "heartbeat"         "15.0"
    "data"
    {
        "provider"      "1"
        "map"           "1"
        "player"        "1"
        "hero"          "1"
    }
}"""


def main():
    print("[+] Dota path")
    path = str(input("[>] ")) #deafoult > C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta

    try:
        with open(
            f"{path}/game/dota/cfg/gamestate_integration/gamestate_integration_rpc.cfg", "w"
        ) as config:
            config.write(config_data)

        print("[+] Success")

    except FileNotFoundError:
        print("[-] Path not found")


if __name__ == "__main__":
    main()
