import json
import pathlib


def load_example_json(base_file, *args):
    path = pathlib.Path(base_file).parent.resolve()
    for arg in args:
        path = path / arg
    with open(path) as f:
        return json.load(f)
