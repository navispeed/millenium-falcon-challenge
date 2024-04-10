import os


def resolve_path(path, json_location):
    if os.path.isabs(path):
        return path
    return os.path.join(os.path.dirname(json_location), path)
