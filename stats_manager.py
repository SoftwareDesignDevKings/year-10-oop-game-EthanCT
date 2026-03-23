import json
import os


STATS_FILE = "stats.json"

DEFAULT_STATS = {
    "games_played"  : 0,
    "total_kills"   : 0,
    "total_coins"   : 0,
    "highest_level" : 1,
    "total_xp"      : 0,
}

def load_stats():
    # load from file if it exists, otherwise start fresh with all zeros
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
        # fill in any keys missing from the file in case new stats were added
        for key, value in DEFAULT_STATS.items():
            data.setdefault(key, value)
        return data
    return dict(DEFAULT_STATS)

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)