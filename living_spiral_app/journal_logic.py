import os
import json
from datetime import datetime

def save_journal_entry(text):
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("data", "journal_entries.json")

    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[date_str] = text

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_journal_entry(date_str=None):
    path = os.path.join("data", "journal_entries.json")
    if not os.path.exists(path):
        return ""

    with open(path, "r") as f:
        data = json.load(f)

    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return data.get(date_str, "")
    
def list_journal_dates():
    path = os.path.join("data", "journal_entries.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = json.load(f)
    return sorted(data.keys())
    
def delete_journal_entry(date_str):
    path = os.path.join("data", "journal_entries.json")
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        data = json.load(f)
    if date_str in data:
        del data[date_str]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)