from typing import Optional

from disnake.ext import commands
import os
import platform
import tarfile
import requests
from youtubesearchpython.__future__ import *

from functions.msc import control
from disnake import ApplicationCommandInteraction as Aci


class FakeContext:
    """
    Bodging
    """

    def __init__(self, interaction: Aci = None, author=None, bot=True, guild=None):
        self.i = interaction

        try:
            self.author = interaction.author
            self.bot = interaction.bot
            self.guild = interaction.guild
            self.voice_client = interaction.guild.voice_client
        except AttributeError:
            self.author = author
            self.bot = author.bot
            self.guild = guild
            self.voice_client = guild.voice_client

    async def send(self, text="", embed=None):
        pass
        # await self.i.response.send_message(text, embed=embed)


async def find_video(query: str, find: int = 5) -> Optional[dict]:
    link = query
    if not query.upper().__contains__("YOUTU"):
        videos_search = VideosSearch(query, limit=find)
        videos_result = await videos_search.next()
        link = "https://youtube.com/watch?v=" + videos_result["result"][0]["id"]

    info = await Video.getInfo(link, resultMode=ResultMode.json)

    return info


def ensure_ffmpeg():
    if "ffmpeg" not in os.listdir():
        if "LINUX" in platform.platform().upper():
            link = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
            print("DOWNLOADING FFmpeg...")
            r = requests.get(link)
            f_dir = os.path.abspath("ffmpeg.tar.gz")
            with open(f_dir, "wb") as f:
                f.write(r.content)
            tar = tarfile.open(f_dir, "r:xz")
            tar.extractall(path=os.path.abspath("ffmpeg"))
            tar.close()

        else:
            print("No FFmeg lol, no sound. linux only. function/music.py")
    else:
        print("FFmpeg already exists, skipping...")
    f_dir = os.path.abspath(os.path.join("ffmpeg", os.listdir(os.path.join(os.getcwd(), "ffmpeg"))[0], "ffmpeg"))

    return f_dir


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = control.Music(self.bot)

    @commands.slash_command(name="music", description="DJ Discord")
    async def music(self, interaction: Aci):
        pass

    @music.sub_command()
    async def stop(self, interaction):
        """Dừng bài nhạc"""
        await self.controller.leave(FakeContext(interaction))

    @music.sub_command()
    async def pause(self, interaction):
        """Tạm dừng bài nhạc đang phát"""
        await self.controller.pause(FakeContext(interaction))

    @music.sub_command()
    async def play(self, interaction, query):
        """Chơi bài hát nào đó."""
        await self.controller.play(ctx=FakeContext(interaction), url=query)


def setup(bot):
    bot.add_cog(Music(bot))
