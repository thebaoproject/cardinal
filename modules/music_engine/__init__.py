import datetime
from dataclasses import dataclass
from typing import Callable, Optional, Any

import disnake
import youtube_dl as ytdl

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }]
}

QUEUE = {}


@dataclass
class Song:
    url: str = None
    title: str = None
    channel: str = None
    channel_link: str = None
    publish_date: datetime.date = None
    description: str = None
    thumbnail: str = None
    audio: str = None
    like: int = None
    # display this
    dislike: int = None
    duration: datetime.timedelta = None
    views: str = None


def to_date(d: str) -> datetime.date:
    """
    Turns YouTube dates into date objects.

    :param d: the date string.
    :return: the date object.
    """
    return datetime.datetime.strptime(f"{d[:4]}-{d[4:6]}-{d[6:]}", "%Y-%m-%d").date()


def timelize(t: str) -> datetime.timedelta:
    return datetime.timedelta(seconds=int(t))


def search(query: str, n: int = 5) -> list[Song]:
    with ytdl.YoutubeDL(YTDL_OPTIONS) as ydl:
        videos = ydl.extract_info(f"ytsearch{n}:{query}", download=False)['entries']
        return [_clean_result(i) for i in videos]


def _clean_result(data: dict) -> Song:
    return Song(
        url=data.get("webpage_url"),
        title=data.get("title"),
        channel=data.get("uploader"),
        channel_link=data.get("uploader_url"),
        description=data.get("description"),
        thumbnail=data.get("thumbnail"),
        audio=data.get("formats")[0]["url"],
        views=data.get("view_count"),
        like=data.get("like_count"),
        dislike=data.get("dislike_count"),
        duration=timelize(data.get("duration")),
        publish_date=to_date(data.get("upload_date"))
    )


def song_to_dict(s: Song) -> dict:
    return {
        "url": s.url,
        "title": s.title,
        "channel": s.channel,
        "channel_link": s.channel_link,
        "description": s.description,
        "thumbnail": s.thumbnail,
        "audio": s.audio,
        "views": s.views,
        "like": s.like,
        "dislike": s.dislike,
        "duration": s.duration.seconds,
        "publish_date": s.publish_date.isoformat(),
    }


def dict_to_song(d: dict) -> Song:
    return Song(
        url=d.get("url"),
        title=d.get("title"),
        channel=d.get("channel"),
        channel_link=d.get("channel_link"),
        description=d.get("description"),
        thumbnail=d.get("thumbnail"),
        audio=d.get("audio"),
        views=d.get("views"),
        like=d.get("like"),
        dislike=d.get("dislike"),
        duration=timelize(d.get("duration")),
        publish_date=datetime.date.fromisoformat(d.get("publish_date"))
    )


async def connect(member: disnake.Member, voice_client: disnake.VoiceClient = None) -> disnake.VoiceClient:
    """
    Connects to the same channel as a user. Moves channel if alreadly connected
    to one.

    :param member: the member whose channel the bot will join.
    :param voice_client: the bot's voice client.
    """
    channel = member.voice.channel
    if voice_client:
        if voice_client.is_connected():
            await voice_client.move_to(channel)
            return voice_client
    else:
        return await channel.connect()


async def play(song: Song, voice_client: disnake.VoiceClient | disnake.VoiceProtocol,
               done: Callable[[Optional[Exception]], Any] = None):
    """
    Plays a song.

    :param done: the function to be called when playing stops or when encoutered an exception,
                 with the parameter of that exception if it ever occured.
    :param song: the song to play.
    :param voice_client: the bot's current voice client.
    """
    voice_client.play(
        disnake.FFmpegPCMAudio(song.audio, **FFMPEG_OPTS), after=done
    )


async def pause(voice_client: disnake.VoiceClient):
    """
    Pauses the song currently playing, or resume it if it's alreadly paused.

    :param voice_client: the guild's voice client.
    """
    if voice_client.is_paused():
        voice_client.pause()
    else:
        voice_client.resume()
