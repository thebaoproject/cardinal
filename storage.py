import pyrebase

import config_manager as cfg

CONFIG = {
    "databaseURL": cfg.get("backend.fireDtb"),
    "apiKey": cfg.get("backend.fireApiKey"),
    "authDomain": "",
    "storageBucket": "",
    "serviceAccount": ""
}


def get_dtb() -> pyrebase.pyrebase.Database:
    return pyrebase.initialize_app(CONFIG).database()
