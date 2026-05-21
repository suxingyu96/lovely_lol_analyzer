import json
import os

STORAGE_FILE = "storage/processed_matches.json"


class MatchStorage:

    @staticmethod
    def load_processed_matches():
        if not os.path.exists(STORAGE_FILE):
            return []

        with open(STORAGE_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_processed_matches(matches):
        with open(STORAGE_FILE, "w") as f:
            json.dump(matches, f)
