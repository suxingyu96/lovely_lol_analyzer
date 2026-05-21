import os

from riot_client import RiotClient
from rules import MatchAnalyzer
from discord_sender import DiscordSender
from storage import MatchStorage


PUUID = os.getenv("RIOT_PUUID")


def build_report(results):
    if not results:
        return (
            "🎮 Daily Riot Report\n\n"
            "No losses detected yesterday. Nice work."
        )

    lines = []
    lines.append("🎮 Daily Riot Loss Report\n")

    for idx, result in enumerate(results, start=1):
        lines.append(
            f"❌ Loss {idx} — {result['champion']}"
        )

        lines.append(f"KDA: {result['kda']}")
        lines.append(f"CS/min: {result['cs_per_min']}")
        lines.append(f"Vision Score: {result['vision_score']}")

        lines.append("\nKey Findings:")

        if result["findings"]:
            for finding in result["findings"]:
                lines.append(f"- {finding}")
        else:
            lines.append("- No major issues detected.")

        lines.append("\n---------------------\n")

    return "\n".join(lines)

def main():
    riot_client = RiotClient()
    analyzer = MatchAnalyzer(PUUID)

    processed_matches = MatchStorage.load_processed_matches()

    match_ids = riot_client.get_match_ids(PUUID)

    analyzed_results = []

    for match_id in match_ids:

        if match_id in processed_matches:
            continue

        match_json = riot_client.get_match(match_id)

        if not analyzer.is_yesterday_match(match_json):
            continue

        result = analyzer.analyze_match(match_json)

        processed_matches.append(match_id)
    
	if result:
            analyzed_results.append(result)

    report = build_report(analyzed_results)

    DiscordSender.send_message(report)

    MatchStorage.save_processed_matches(processed_matches)


if __name__ == "__main__":
    main()
