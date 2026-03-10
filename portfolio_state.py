import json
import os

STATE_FILE = "live_state.json"


def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        return json.load(f)
