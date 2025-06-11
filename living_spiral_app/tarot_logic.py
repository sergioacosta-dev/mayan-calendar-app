
import json
import os
import random

def load_tarot_cards():
    path = os.path.join("data", "tarot_cards.json")
    with open(path, "r") as f:
        return json.load(f)

def draw_card():
    cards = load_tarot_cards()
    card = random.choice(cards)
    orientation = random.choice(["upright", "reversed"])
    return {
        "name": card["name"],
        "suit": card["suit"],
        "orientation": orientation,
        "meaning": card[orientation]
    }

def draw_three_cards():
    cards = load_tarot_cards()
    spread = random.sample(cards, 3)
    return [
        {
            "position": "Past",
            "name": spread[0]["name"],
            "suit": spread[0]["suit"],
            "orientation": (ori := random.choice(["upright", "reversed"])),
            "meaning": spread[0][ori]
        },
        {
            "position": "Present",
            "name": spread[1]["name"],
            "suit": spread[1]["suit"],
            "orientation": (ori := random.choice(["upright", "reversed"])),
            "meaning": spread[1][ori]
        },
        {
            "position": "Future",
            "name": spread[2]["name"],
            "suit": spread[2]["suit"],
            "orientation": (ori := random.choice(["upright", "reversed"])),
            "meaning": spread[2][ori]
        }
    ]
