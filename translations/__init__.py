import json
import os
import urllib.parse
import logger
import disnake
import aiohttp
import config_manager as cfg
import storage
import translations.langlist

from typing import Union


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


async def translate(*source: str, target_language: str, source_language: str = None) -> list:
    """
    Translates the given text to the target language.
    """
    payload = [f"q={urllib.parse.quote(i)}" for i in source]
    payload = "".join(payload)
    payload += f"&target={urllib.parse.quote(target_language)}"
    payload += f"&source={urllib.parse.quote(source_language)}" if source_language is not None else ""
    # payload = "q=Hello%2C%20%20world!&target=vi"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
        "X-RapidAPI-Key": cfg.read("rapidapi-key")
    }
    logger.debug(f"Completed translation payload: {payload}")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://google-translate1.p.rapidapi.com/language/translate/v2",
            data=payload,
            headers=headers
        ) as r:
            data = await r.json()
            if r.status == 200:
                data = data["data"]["translations"]
                output = [i["translatedText"] for i in data]
                return output
            else:
                a = await r.text("utf8")
                logger.error(f"API translation request error: code {r.status}: {a}")
                return []


async def find_lang(name: str):
    for k, v in langlist.LIST.items():
        if v["name"] in name or v["nativeName"] in name:
            return k
