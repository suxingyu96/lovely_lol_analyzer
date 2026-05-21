import os
import requests
import time

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REGION = "europe"
PLATFORM_REGION = "euw1"

HEADERS = {
    "X-Riot-Token": RIOT_API_KEY
}

class RiotClient:

    def __init__(self):
        self.base_match_url = f"https://{REGION}.api.riotgames.com"
        self.base_platform_url = f"https://{PLATFORM_REGION}.api.riotgames.com"

    def get_match_ids(self, puuid, count=20):
        url = (
            f"{self.base_match_url}"
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            params={"start": 0, "count": count}
        )

        response.raise_for_status()
        return response.json()

    def get_match(self, match_id):
        url = f"{self.base_match_url}/lol/match/v5/matches/{match_id}"

        response = requests.get(url, headers=HEADERS)

        response.raise_for_status()

        time.sleep(1)

        return response.json()
