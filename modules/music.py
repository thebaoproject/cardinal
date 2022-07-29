from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

from modules.music_engine import *
from modules.music_engine.widgets import *


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="music")
    async def music(self, interaction):
        pass

    @music.sub_command(name="play", description="Chơi một bài hát.")
    async def play(self, interaction: Aci, query: str):
        await interaction.response.defer()
        voice = interaction.author.voice
        results = search(query)
        if interaction.guild.id not in QUEUE.keys():
            QUEUE[interaction.guild.id] = {"q": [], "vc": None}
        if not bool(voice):
            await interaction.send(msg.get(interaction.author, "music.error.notInVoice"))
            return
        v = disnake.ui.View()
        song_chooser = SongChooser(results, interaction.author)
        song_chooser.placeholder = results[0].title
        v.add_item(song_chooser)
        v.add_item(SongPlayButton(interaction.author, results[0]))
        await interaction.send(view=v, embed=make_card(results[0], interaction.author))

    @music.sub_command(name="pause", description="Tạm dừng bài hát đang chơi.")
    async def pause(self, interaction: Aci):
        if (QUEUE[interaction.guild.id]["vc"]) is None:
            await interaction.send(msg.get(interaction.author, "music.error.notInVoice"))
            return
        await pause(QUEUE[interaction.guild]["vc"])
        await interaction.send(msg.get(interaction.author, "music.success.pause"))

    @music.sub_command(name="stop", description="Dừng chơi bài hát.")
    async def stop(self, interaction: Aci):
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect(force=False)
        await interaction.send(msg.get(interaction.author, "music.success.stop"))
        QUEUE[interaction.guild.id]["q"] = []

    @music.sub_command(name="skip", description="Bỏ qua bài hát.")
    async def skip(self, interaction: Aci):
        QUEUE[interaction.guild.id]["vc"].stop()
        await interaction.send(msg.get(interaction.author, "music.success.skip"))

    @music.sub_command(name="queue", description="Liệt kê danh sách phát.")
    async def queue(self, interaction: Aci):
        await interaction.response.defer()
        await interaction.edit_original_message(
            msg.get(interaction.author, "music.success.list"),
            embeds=[make_card(i, interaction.author) for i in QUEUE[interaction.guild.id]["q"]]
        )


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
