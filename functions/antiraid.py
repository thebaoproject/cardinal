import disnake
import translations as msg
import bot_utils as utils
import numpy
import config_manager as cfg

from disnake.ext import commands


class AntiRaid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if not cfg.get("antiRaid.enable"):
            return
        c = message.content
        a = message.author
        ping = "@everyone" in c or "@here" in c
        is_raid = 0
        if ping:
            if a.bot:
                is_raid += 1
            elif not a.top_role.permissions.moderate_members:
                is_raid += 0.2
        if utils.str_in_str(
            [
                ".com",
                ".net",
                ".gift",
                ".gg",
                "http",
                "//"
            ],
            c
        ):
            is_raid += 0.3

        msg_list = message.channel.history(limit=5)
        author_list = []
        times = []
        async for i in msg_list:
            author_list.append(i)
            times.append(i.created_at.timestamp())
        if author_list.count(author_list[0]) == len(author_list):
            is_raid += 0.3
        avg_time = numpy.average(numpy.diff(times))
        if avg_time < 2:
            is_raid += 0.3

        if a.guild.audit_logs(limit=5):
            pass

        is_raid = is_raid >= cfg.get("antiRaid.spamThreshold")
        if is_raid:
            await a.timeout(duration=1*60*60)
            card = disnake.Embed(title=msg.get("vi", "antiRaid.susTitle"))
            card.add_field(
                msg.get("vi", "intel.name"), a.name
            )
            card.add_field(
                msg.get("vi", "antiRaid.action"), msg.get("vi", "antiRaid.isolateMember")
            )
            await message.channel.send(
                embed=card
            )


def setup(bot):
    bot.add_cog(AntiRaid(bot))
