import youtubesearchpython.__future__ as yt

import os
import json
import disnake
import logger
import translations as msg
import youtube_dl as ytdl

from disnake.ext import commands
from enum import Enum
from disnake import ApplicationCommandInteraction as Aci

FFMPEG_OPTIONS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
YDL_OPTIONS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}
PLAYING = {}
QUEUE = []
CHOICES = []
CHOSEN = -1
BOT: commands.Bot = None
VOICE_CLIENT: disnake.VoiceClient = None
SKIPPING = False


class MusicStatus(Enum):
    SUCCESS = 200
    AWAIT = 201
    PAUSED = 202
    USER_NOT_IN_VOICE = 400
    VIDEO_NOT_FOUND = 401
    INVALID_ID = 402
    NOT_PLAYING_ANYTHING = 403
    INVALID_JSON = 404
    ERROR = 500
    VIDEO_PLAYBACK_ERROR = 501


class SongSelect(disnake.ui.Button):
    def __init__(self, lang: disnake.User, supposed_choice: dict):
        super().__init__(
            style=disnake.ButtonStyle.green,
            label=msg.get(lang, "music.buttonChooseLabel")
        )
        self.supposed_choice = supposed_choice

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        global QUEUE
        global CHOICES
        global CHOSEN
        global VOICE_CLIENT
        QUEUE.append(self.supposed_choice)
        if _is_in_voice(interaction.author):
            channel = interaction.author.voice.channel
            if VOICE_CLIENT is None:
                VOICE_CLIENT = await channel.connect()
            try:
                await interaction.send(embed=infobox(self.supposed_choice, interaction.author))
                await _play(VOICE_CLIENT, QUEUE[0]["rawurl"])
            except IndexError:
                pass
            except disnake.ClientException as e:
                logger.warning(f"ClientException received: {e}")
                pass
        else:
            await interaction.send(msg.get(interaction.author, "music.error.notInVoice"))


class SongChooser(disnake.ui.Select):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang

    def add_song(self, title: str, channel: str, return_val: any):
        super().add_option(
            label=msg.get(self.lang, "music.chooseCard")
            .format(channel=channel, title=title[:30] + "..."),
            value=str(return_val)
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        global CHOSEN
        global CHOICES
        CHOSEN = int(self.values[0])
        chosen_info = CHOICES[CHOSEN]
        ok = SongSelect(interaction.author, chosen_info)
        ui = disnake.ui.View()
        ui.add_item(self)
        ui.add_item(ok)
        embed = infobox(chosen_info, interaction.author)
        # embed.set_image(chosen_info["thumbnail"])
        self.placeholder = self.options[CHOSEN].label
        await interaction.send(
            embed=embed,
            view=ui
        )
        logger.debug(f"User has chosen {self.values[0]}")


async def find_video(query: str, find: int = 5) -> list[dict]:
    """
    Find the video with the specified query/link.

    Parameters
    ----------
    query: str
        The query to find. Can be a link or a search query.
    find: int = 5
        The amount of videos to find. Default to 5.

    Returns
    -------
    info: list[dict]
        The info of the video found.
    """
    logger.debug(f"Video search request initiated: '{query}', finding {find} videos.")
    info = []
    # Checks if this is a derect YouTube link
    if not query.upper().__contains__("YOUTU"):
        videos_search = yt.VideosSearch(query, limit=find)
        videos_result = await videos_search.next()
        logger.debug(f"Found videos: {videos_result}")
        for i in range(len(videos_result["result"])):
            info.append(videos_result["result"][i])
    # Else, it is a search query.
    else:
        a = await yt.Video.getInfo(query, resultMode=yt.ResultMode.json)
        info.append(a)

    return info


def _is_playing():
    """Checks that audio is currently playing before continuing."""
    return VOICE_CLIENT.is_playing()


def extract_juice(video_url: str):
    with ytdl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info["formats"][0]["url"]


def infobox(video: dict, lang):
    embed = disnake.Embed(title=video["title"], color=disnake.Color.red())
    embed.add_field(msg.get(lang, "music.songDescription.title"), video["title"])
    embed.add_field(msg.get(lang, "music.songDescription.length"), video["length"])
    embed.add_field(msg.get(lang, "music.songDescription.channel"), video["channel"])
    embed.set_thumbnail(video["thumbnail"])
    embed.url = video["url"]
    return embed


def _is_in_voice(member: disnake.Member) -> bool:
    voice = member.voice
    return bool(voice) and bool(voice.channel)


async def _play(client: disnake.VoiceClient, url: str):
    """
    Plays the video with the url above.

    Parameters
    ----------
    client: disnake.VoiceClient
        The client the bot is connected to
    url: str
        The URL of the video.
    """
    msc = disnake.PCMVolumeTransformer(
        disnake.FFmpegPCMAudio(
            url,
            before_options=FFMPEG_OPTIONS,
            executable=ensure_ffmpeg()
        ),
        volume=1.0
    )

    def _after(err):
        if err is not None:
            logger.error(err)
        else:
            global QUEUE
            global SKIPPING
            if not SKIPPING:
                logger.warning(f"Trying to pop a song out of the queue... {QUEUE}")
                QUEUE.pop(0)
            else:
                SKIPPING = False
            if len(QUEUE) == 0:
                return
            _play(client, QUEUE[0]["url"])
    logger.debug(f"Đang chơi... {url}")
    client.play(msc, after=_after)


def _pause():
    """Pauses the sound"""
    global VOICE_CLIENT
    if VOICE_CLIENT.is_paused():
        VOICE_CLIENT.resume()
    else:
        VOICE_CLIENT.pause()


async def _stop():
    global VOICE_CLIENT
    if VOICE_CLIENT and VOICE_CLIENT.channel:
        await VOICE_CLIENT.disconnect()
        VOICE_CLIENT = None
    else:
        logger.warning("The bot isn't in a voice channel, cannot leave.")
        return MusicStatus.NOT_PLAYING_ANYTHING


def ensure_ffmpeg() -> str:
    """
    Ensures that ffmpeg is installed on the system.

    Returns
    -------
    f_dir: str
        The directory where the ffmpeg executable lives.
    """
    if "ffmpeg" not in os.listdir():
        # if "LINUX" in platform.platform().upper():
        #     link = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
        #     logger.info(
        #         "FFmpeg not found. It is required to do sound functions. Downloading binary for Linux AMD64...")
        #     r = requests.get(link)
        #     f_dir = os.path.abspath("ffmpeg.tar.gz")
        #     with open(f_dir, "wb") as f:
        #         f.write(r.content)
        #     tar = tarfile.open(f_dir, "r:xz")
        #     tar.extractall(path=os.path.abspath("ffmpeg"))
        #     tar.close()
        #
        # else:
        logger.error(
            "Please download FFmpeg and extract it to ./ffmpeg/. It is needed for music to function correctly."
        )
    else:
        logger.info("Found FFmpeg installed on your system. Getting its path...")
    ffmpeg_executable = "ffmpeg"
    ffmpeg_executable += ".exe" if os.name == "nt" else ""
    f_dir = os.path.abspath(os.path.join("ffmpeg", ffmpeg_executable))
    logger.info(f"FFmpeg found at {f_dir}")
    return f_dir


async def _song_choose(interaction: Aci, songs: list[dict[str, str, disnake.User]]):
    """
    Displays a graphical UI to choose the song.
    """
    choices = SongChooser(interaction.author)
    for i, v in enumerate(songs):
        choices.add_song(
            title=v["title"][:20] + "...",
            channel=v["channel"],
            return_val=i
        )
    ui = disnake.ui.View()
    ui.add_item(choices)
    await interaction.send(view=ui)


def _scrap_result(result, lang):
    """Extract juice"""
    videos = result
    output = []
    for i in videos:
        logger.debug(f"parsing video: {i}")
        try:
            description = i["descriptionSnippet"][0]["text"]
        except TypeError:
            description = msg.get(lang, "music.noDescription")
        output.append({
            "title": i["title"],
            "length": i["duration"],
            "channel": i["channel"]["name"],
            "description": description,
            "thumbnail": i["thumbnails"][0]["url"],
            "url": i["link"],
            "rawurl": extract_juice(i["link"])
        })
    return output


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    @commands.slash_command(name="music", description="DJ Discord")
    async def music(self, interaction: Aci):
        pass

    @music.sub_command()
    async def stop(self, interaction: Aci):
        """Dừng bài nhạc"""
        await _stop()
        await interaction.send(msg.get(interaction.author, "music.success.stop"))

    @music.sub_command()
    async def pause(self, interaction: Aci):
        """Tạm dừng bài nhạc đang phát"""
        _pause()
        await interaction.send(msg.get(interaction.author, "music.success.pause"))

    @music.sub_command()
    async def play(self, interaction: Aci, query: str):
        """Chơi bài hát nào đó."""
        if not _is_in_voice(interaction.author):
            await interaction.send(msg.get(interaction.author, "music.error.notInVoice"))

            logger.info(f"User {interaction.author.name} requested without joining a voice channel.")
            return
        await interaction.response.defer()
        logger.debug("Received play request.")
        songs = await find_video(query)
        songs = _scrap_result(songs, interaction.author)
        logger.debug(json.dumps(songs, ensure_ascii=False))
        global CHOICES
        CHOICES = songs
        await _song_choose(interaction, songs)
        # if not _is_playing():
        #     self.voice_client = VOICE_CLIENT
        #     try:
        #         await interaction.send(embed=infobox(CHOICES[CHOSEN], interaction.author))
        #         try:
        #             await _play(self.voice_client, QUEUE[0]["rawurl"])
        #         except disnake.ClientException:
        #             pass
        #     except IndexError:
        #         pass

    @music.sub_command()
    async def skip(self, interaction: Aci, song_number: int = 0):
        """Bỏ qua bài nhạc có số thứ tự được nêu. Mặc định là bài tiếp theo."""
        await interaction.response.defer()
        global QUEUE
        global VOICE_CLIENT
        logger.debug(f"Trying to pop a song out of the queue... {QUEUE}")
        QUEUE.pop(song_number)
        if song_number == 0:
            global SKIPPING
            SKIPPING = True
            await _stop()
        if len(QUEUE) != 0:
            VOICE_CLIENT = await interaction.author.voice.channel.connect()
            logger.debug("Trying to play the next song")
            await _play(VOICE_CLIENT, QUEUE[0]["rawurl"])
        await interaction.edit_original_message(content=msg.get(interaction.author, "music.success.skip"))

    @music.sub_command()
    async def listqueue(self, interaction: Aci):
        """Hiện danh sách phát bài nhạc"""
        await interaction.response.defer()
        embeds = []
        global QUEUE
        for i in QUEUE:
            embeds.append(infobox(i, interaction.author))
        await interaction.edit_original_message(
            content=msg.get(interaction.author, "music.success.list") +
            msg.get(interaction.author, "music.noSongInQueue") if len(QUEUE) == 0 else "",
            embeds=embeds
        )


def setup(bot):
    bot.add_cog(Music(bot))
    global BOT
    BOT = bot
