import json
import os


def get_state_file(BOT_NAME="default_bot"):
    return f"portfolio_state_{BOT_NAME}.json"


def save_state(state, BOT_NAME="default_bot"):

    state_file = get_state_file(BOT_NAME)

    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def load_state(BOT_NAME="default_bot"):

    state_file = get_state_file(BOT_NAME)

    if not os.path.exists(state_file):

        return {
            "cash": 80000,
            "positions": {},
            "history": []
        }

    with open(state_file, "r") as f:
        return json.load(f)