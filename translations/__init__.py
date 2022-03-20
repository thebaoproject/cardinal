import json
import os
import logger
import disnake
from typing import Union

import storage

LANG_LIST = {
    "Tiếng Việt (Việt Nam)": "vi",
    "English (United States/United Kingdom)": "en",
    "LOLCAT TiếG VịT (Vịt Nem)": "lolvi",
    "EngLisH LOLCAT (UNiTed Steaks/UNited KiNdam)": "lolen",
    "Tiếq Việt Kải Kác (Bùi Hiền Việt Nam)": "vicc",
    "(ɯopɓuᴉʞ pǝʇᴉu∩/sǝʇɐʇs pǝʇᴉu∩) ɥsᴉlɓuǝ uʍopǝpᴉsd∩": "uen",
}


def get(target_language: Union[disnake.User, str], identifier: str) -> any:
    path = identifier.split(".")
    logger.debug(f"path to read: {path}")
    if type(target_language) == str:
        n_lan = "en" if target_language in ["en-UK", "en-US"] else target_language
        n_lan = "vi" if n_lan == "vi-VN" else n_lan
    else:
        n_lan = storage.get_dtb().child("users").child(str(target_language.id)).child("language").get().val()
    try:
        with open(os.path.join("translations", f"{n_lan}.json"), "r", encoding="utf-8") as f:
            strings = json.loads(f.read())
    except FileNotFoundError:
        logger.warning(f"Language {n_lan} not found. Defaulting to English.")
        with open(os.path.join("translations", f"en.json"), "r", encoding="utf-8") as f:
            strings = json.loads(f.read())
    dest = strings
    for i in path:
        dest = dest[i]
    return dest
