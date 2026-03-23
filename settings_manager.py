import json
import os


SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "music_enabled"   : True,
    "sfx_enabled"     : True,
    "show_fps"        : False,
    "enemy_indicators": True,
}

def load_settings():
    # load from file if it exists, otherwise fall back to defaults
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # fill in any keys that weren't in the file (e.g. newly added settings)
        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)
        return data
    return dict(DEFAULT_SETTINGS)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)