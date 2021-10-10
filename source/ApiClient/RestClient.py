import requests
import json

from ShiftCipher import full_encode


class RestClient:

    @staticmethod
    def get_link(state: str) -> str:
        match state:
            case "Dev":
                return "https://localhost:5001/api/Matches/Add"
            case "Prod":
                return "https://123.123.123.123:5001/api/Matches/Add"
            case _:
                return ""

    @staticmethod
    def steam64_to_steam3(steam64: int | str) -> int:
        steam_base = 76561197960265728
        match steam64:
            case str(steam64):
                return int(steam64) - steam_base
            case int(steam64):
                return steam64 - steam_base

    @staticmethod
    def send(data: dict, state: str) -> int:
        try:
            steam_id = RestClient.steam64_to_steam3(data["player"]["steamid"])
            match_id = int(data["map"]["matchid"])
        except requests.RequestException as e:
            print(e)
            return 500

        transfer = {
            'steam3Id': steam_id,
            'matchId': match_id,
            # Шифрование сообщения, чтобы нельзя было подменить по api
            'data': full_encode("(authentic string)->" + str(data).replace("True", "true").replace("False", "false"),
                                str(match_id - steam_id))
        }

        try:
            res = requests.post(RestClient.get_link(state), json=transfer, verify=False)
            if res.status_code != 200:
                print(res.text)
            return res.status_code

        except requests.RequestException as e:
            if len(e.args) > 0:
                print(e.args[0])
            return 500


# Test
f = open('info.json')
data_from_json = json.load(f)
print(RestClient.send(data_from_json, 'Dev'))
