import requests

from ShiftCipher import full_encode


class RestClient:

    @staticmethod
    def get_link(state: str) -> str:
        match state:
            case "Dev":
                return "https://localhost:5001/api/Auth"
            case "Prod":
                return "https://123.123.123.123:5001/api/Auth"
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
            'steamId': steam_id,
            'matchId': match_id,
            'data': full_encode(str(data), str(match_id - steam_id))
        }

        try:
            res = requests.post(RestClient.get_link(state), json=transfer, verify=False)
            return res.status_code

        except requests.RequestException as e:
            print(e.args[0])
            return 500


# Test
print(RestClient.send({"player": {"steamid": 76561197965742086}, "map": {"matchid": 123412341212}}, 'Dev'))
