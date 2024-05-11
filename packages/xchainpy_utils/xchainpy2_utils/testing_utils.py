import json
import pathlib


def load_example_json(base_file, *args):
    """
    Load a JSON file from the same directory as the base file, with the given path components.
    :param base_file: The base file to start from.
    :param args: The path components to append to the base file.
    :return: The loaded JSON data.
    """
    path = pathlib.Path(base_file).parent.resolve()
    for arg in args:
        path = path / arg
    with open(path) as f:
        return json.load(f)
