import disnake
import tarfile
import requests
import youtube_dl
import asyncio
import platform
import os

from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


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
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="music", description="DJ Discord")
    async def music(self, interaction: Aci):
        pass

    @music.sub_command()
    async def play(self, interaction: Aci, data: str):
        """Chơi bài hát nào đó."""
        try:
            a = interaction.author.voice
        except TypeError:
            await interaction.response.send_message(
                "Vào kênh voice trước đi rồi hãng nói"
            )
            return

        await a.channel.connect()
        if not data.upper().__contains__("YOUTU"):
            await interaction.response.send_message(
                "Đây không phải là link Youtube."
            )

        voice_channel = interaction.guild.voice_client
        r = requests.get(data)
        await interaction.response.send_message(f"")
        async with interaction.channel.typing():
            filename = await YTDLSource.from_url(data, loop=self.bot.loop)
            voice_channel.play(disnake.FFmpegPCMAudio(executable=ensure_ffmpeg(), source=filename))

        interaction.guild.voice_client.cleanup()
        interaction.guild.voice_client.disconnect()

    @music.sub_command()
    async def pause(self, interaction: Aci):
        """Tạm dừng bài nhạc đang phát"""
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            voice_client.cleanup()
            voice_client.disconnect()
        else:
            await interaction.response.send_message("Bot hiện không đang phát bài nào.")

    @music.sub_command()
    async def resume(self, interaction: Aci):
        """Tiếp tục bài nhạc"""
        voice_client = interaction.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await interaction.response.send_message("Bot không đang phát bài nào mà bị dừng.")

    @music.sub_command()
    async def stop(self, interaction: Aci):
        """Dừng bài nhạc"""
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await interaction.response.send_message("Bot hiện không đang phát bài nào.")


def setup(bot: commands.Bot):
    ensure_ffmpeg()
    bot.add_cog(Music(bot))
