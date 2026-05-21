from datetime import datetime, timezone, timedelta


YESTERDAY = datetime.now(timezone.utc).date() - timedelta(days=1)


class MatchAnalyzer:

    def __init__(self, puuid):
        self.puuid = puuid

    def is_yesterday_match(self, match_json):
        game_end = match_json["info"]["gameEndTimestamp"] / 1000
        game_date = datetime.fromtimestamp(game_end, tz=timezone.utc).date()

        return game_date == YESTERDAY

    def get_player_data(self, match_json):
        for participant in match_json["info"]["participants"]:
            if participant["puuid"] == self.puuid:
                return participant

        return None

    def analyze_match(self, match_json):
        player = self.get_player_data(match_json)

        if not player:
            return None

        if player["win"]:
            return None

        findings = []

        champion = player["championName"]
        kills = player["kills"]
        deaths = player["deaths"]
        assists = player["assists"]
        cs = (
            player["totalMinionsKilled"]
            + player.get("neutralMinionsKilled", 0)
        )

        game_duration = match_json["info"]["gameDuration"] / 60
        cs_per_min = round(cs / game_duration, 1)

        vision_score = player.get("visionScore", 0)

        # Rule: high deaths
        if deaths >= 8:
            findings.append(
                "High death count reduced mid-game consistency."
            )

        # Rule: low CS
        if cs_per_min < 5:
            findings.append(
                "Low CS/min caused weaker gold scaling."
            )
	# Rule: low vision
        if vision_score < 20:
            findings.append(
                "Vision score was low for overall game duration."
            )

        # Rule: low kill participation
        team_kills = sum(
            p["kills"]
            for p in match_json["info"]["participants"]
            if p["teamId"] == player["teamId"]
        )

        kp = 0
        if team_kills > 0:
            kp = (kills + assists) / team_kills

        if kp < 0.35:
            findings.append(
                "Low kill participation suggests weak teamfight involvement."
            )
	
	# Rule: anti-heal detection
        enemy_team = [
            p for p in match_json["info"]["participants"]
            if p["teamId"] != player["teamId"]
        ]

        healing_champions = {
            "Aatrox",
            "Soraka",
            "Vladimir",
            "Sylas",
            "Warwick",
            "Briar",
            "DrMundo",
            "Yuumi"
        }

        enemy_healing = any(
            enemy["championName"] in healing_champions
            for enemy in enemy_team
        )

	antiheal_items = {
            3123,
            3035,
            3165
        }

        built_antiheal = any(
            player.get(f"item{i}") in antiheal_items
            for i in range(7)
        )

        if enemy_healing and not built_antiheal:
            findings.append(
                "No anti-heal item built against heavy sustain composition."
            )

        return {
            "champion": champion,
            "kda": f"{kills}/{deaths}/{assists}",
            "cs_per_min": cs_per_min,
            "vision_score": vision_score,
            "findings": findings
        }
