import asyncio
from typing import Union

import disnake

import logger
import translations as msg
from . import Song, QUEUE, play


def make_card(song: Song, lang: Union[str, disnake.Locale]) -> disnake.Embed:
    """
    Generates an infobox for the song.

    :param song: The video information. Supposed to come from _scrap_result()
    :param lang: The user from whom the language will be infered
    :return: The embed which contains the infobox.
    """
    embed = disnake.Embed(title=song.title, color=disnake.Color.red())
    embed.add_field(msg.get(lang, "music.songDescription.prop"), f"{song.like}👍")
    embed.add_field(msg.get(lang, "music.songDescription.length"), str(song.duration))
    embed.add_field(msg.get(lang, "music.songDescription.channel"), song.channel)
    embed.add_field(msg.get(lang, "music.songDescription.description"), song.description[:30] + "...")
    embed.add_field(msg.get(lang, "music.songDescription.channel"), song.publish_date)

    embed.set_thumbnail(song.thumbnail)
    embed.url = song.url
    return embed


class SongChooser(disnake.ui.Select):
    def __init__(self, songs: list[Song], lang):
        super().__init__()
        for i, v in enumerate(songs):
            super().add_option(
                label=msg.get(
                    lang, "music.chooseCard"
                ).format(channel=v.channel, title=v.title[:30] + "..."),
                value=str(i)
            )
        self.song_list = songs

    async def callback(self, interaction: disnake.MessageInteraction):
        song = self.song_list[int(self.values[0])]
        v = disnake.ui.View()
        ok = SongPlayButton(interaction.author, song)
        self.placeholder = song.title
        v.add_item(self)
        v.add_item(ok)

        await interaction.edit_original_message(
            embed=make_card(song, interaction.author),
            view=v
        )


class SongPlayButton(disnake.ui.Button):
    def __init__(self, lang: disnake.User, choice: Song = None):
        super().__init__(
            style=disnake.ButtonStyle.green,
            label=msg.get(lang, "music.buttonChooseLabel")
        )
        self.choice = choice

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        QUEUE[interaction.guild.id]["q"].append(self.choice)

        def continue_queue(exc: Exception):
            QUEUE[interaction.guild.id]["q"].pop(0)
            if exc is not None:
                logger.error(str(exc))
            if len(QUEUE[interaction.guild.id]["q"]) > 0:
                asyncio.run_coroutine_threadsafe(
                    interaction.message.channel.send(
                        msg.get(interaction.author, "music.success.play"),
                        embed=make_card(QUEUE[interaction.guild.id]["q"][0], interaction.author)
                    ),
                    interaction.guild.voice_client.client.loop
                )
                asyncio.run_coroutine_threadsafe(
                    play(
                        QUEUE[interaction.guild.id]["q"][0],
                        interaction.guild.voice_client
                    ),
                    interaction.guild.voice_client.client.loop)
            else:
                asyncio.run_coroutine_threadsafe(
                    interaction.guild.voice_client.disconnect(force=False),
                    interaction.guild.voice_client.client.loop
                )

        self.disabled = True
        await interaction.send(
            msg.get(interaction.author, "music.success.addQueue"),
            embed=make_card(self.choice, interaction.author)
        )
        logger.debug(QUEUE)
        if QUEUE[interaction.guild.id]["vc"] is None:
            QUEUE[interaction.guild.id]["vc"] = await interaction.author.voice.channel.connect()
        if not QUEUE[interaction.guild.id]["vc"].is_playing():
            await play(self.choice, interaction.guild.voice_client, done=continue_queue)
