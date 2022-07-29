import os

from config import CONFIG


def get(entry: str):
    path = entry.split(".")
    a = CONFIG.copy()
    for i in path:
        a = a[i]
    if a is not None:
        return a
    else:
        return os.environ[entry]
