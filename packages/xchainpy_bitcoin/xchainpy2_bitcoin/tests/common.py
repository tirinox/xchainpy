import json


def load_json(file_name):
    if not file_name.endswith('.json'):
        file_name = f'{file_name}.json'
    with open(f'./mock/{file_name}') as f:
        return json.load(f)
