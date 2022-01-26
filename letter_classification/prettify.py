import json


with open('test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

