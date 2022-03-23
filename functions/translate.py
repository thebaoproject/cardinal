import logger
import translations as msg

from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from translations.langlist import LIST


async def language_suggester(interaction: Aci, inp: str):
    lang = []
    for k, v in LIST.items():
        lang.append(f"{k} - {v['name']}")
    result = [i for i in lang if inp.upper() in i.upper()]
    if len(result) <= 10:
        return result
    else:
        return result[:10]


class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="translate", description="Dịch")
    async def translate(
        self,
        interaction: Aci,
        target_language=commands.Param(autocomplete=language_suggester),
        query: str = commands.Param(),
        source_language=None
    ):
        await interaction.response.defer()
        tl = target_language[:2]
        result = await msg.translate(
            query, target_language=tl, source_language=source_language
        )
        if len(result) == 1:
            r = result[0]
        else:
            r = ", ".join(result)
        await interaction.edit_original_message(content=msg.get(interaction.author, "trans.Tcard").format(src=query, r=r))


def setup(bot):
    bot.add_cog(Translate(bot))




