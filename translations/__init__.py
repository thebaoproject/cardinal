import json
import os
import urllib.parse
from typing import Union

import aiohttp
import disnake

import config_manager as cfg
import logger
import storage
import translations.langlist

LANG_LIST = {
    "Tiếng Việt (Việt Nam)": "vi",
    "English (United States/United Kingdom)": "en",
    "LOLCAT TiếG VịT (Vịt Nem)": "lolvi",
    "EngLisH LOLCAT (UNiTed Steaks/UNited KiNdam)": "lolen",
    "Tiếq Việt Kải Kác (Bùi Hiền Việt Nam)": "vicc",
    "(ɯopɓuᴉʞ pǝʇᴉu∩/sǝʇɐʇs pǝʇᴉu∩) ɥsᴉlɓuǝ uʍopǝpᴉsd∩": "uen",
}


def get(target_language: Union[disnake.User, str, disnake.Locale], identifier: str) -> any:
    path = identifier.split(".")
    if isinstance(target_language, (str, disnake.Locale)):
        if target_language in ("vi", disnake.Locale.vi):
            n_lan = "vi"
        elif target_language in ("en", disnake.Locale.en_GB, disnake.Locale.en_US):
            n_lan = "en"
        else:
            n_lan = str(target_language)
    elif isinstance(target_language, (disnake.Member, disnake.User)):
        n_lan = storage.get_dtb().child("users").child(str(target_language.id)).child("language").get().val()
    else:
        n_lan = "en"
    try:
        with open(os.path.join("translations", f"{n_lan}.json"), "r", encoding="utf-8") as f:
            strings = json.loads(f.read())
    except FileNotFoundError:
        logger.warning(f"Language {n_lan} not found. Defaulting to English.")
        with open(os.path.join("translations", f"en.json"), "r", encoding="utf-8") as f:
            strings = json.loads(f.read())
    d = strings
    for i in path:
        d = d[i]
    return d


async def translate(*source: str, target_language: str, source_language: str = None) -> list:
    """
    Translates given text to target language using Google's API.

    :param source: the source strings.
    :param target_language: the language to translate to.
    :param source_language: the language of the source.
    :return: the translated string.
    """
    payload = [f"q={urllib.parse.quote(i)}" for i in source]
    payload = "".join(payload)
    payload += f"&target={urllib.parse.quote(target_language)}"
    payload += f"&source={urllib.parse.quote(source_language)}" if source_language is not None else ""
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
        "X-RapidAPI-Key": cfg.get("backend.rapidApiKey")
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
