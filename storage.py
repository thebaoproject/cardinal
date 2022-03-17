import config_manager as cfg

import pyrebase

CONFIG = {
    "databaseURL": cfg.read("fire-dtb"),
    "apiKey": cfg.read("fire-api-key"),
    "authDomain": "",
    "storageBucket": "",
    "serviceAccount": ""
}


def get_dtb() -> pyrebase.pyrebase.Database:
    return pyrebase.initialize_app(CONFIG).database()
