import json

def load_sites(path='data/sites-si.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
