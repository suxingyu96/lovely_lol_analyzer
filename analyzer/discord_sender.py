import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


class DiscordSender:

    @staticmethod
    def send_message(message):
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message}
        )

        response.raise_for_status()
