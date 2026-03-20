import json
import os


def get_state_file(bot_name="default_bot"):
    return f"portfolio_state_{bot_name}.json"


def save_state(state, bot_name="default_bot"):

    state_file = get_state_file(bot_name)

    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def load_state(bot_name="default_bot"):

    state_file = get_state_file(bot_name)

    if not os.path.exists(state_file):

        return {
            "cash": 30000,
            "positions": {},
            "history": []
        }

    with open(state_file, "r") as f:
        return json.load(f)