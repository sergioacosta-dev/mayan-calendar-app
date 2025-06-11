
import json, os, random, hashlib

def load_iching_data():
    path = os.path.join("data", "iching_detailed_template.json")
    with open(path, "r") as f:
        return json.load(f)

def get_seed_from_question(text):
    hash_obj = hashlib.md5(text.encode())
    return int(hash_obj.hexdigest(), 16) % 100000

def generate_hexagram_lines(seed):
    random.seed(seed)
    return [random.randint(6, 9) for _ in range(6)]

def get_binary_from_lines(lines):
    return "".join("1" if line in (7, 9) else "0" for line in reversed(lines))

def find_hexagram(binary, data):
    for entry in data:
        if entry["binary"] == binary:
            return entry
    return None

def get_iching_hexagram(question):
    seed = get_seed_from_question(question)
    lines = generate_hexagram_lines(seed)
    binary = get_binary_from_lines(lines)
    data = load_iching_data()
    hexagram = find_hexagram(binary, data)
    return hexagram
