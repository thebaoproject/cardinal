import os
import logger
import disnake
import datetime

from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands, tasks


async def log_autocompleter(interaction: Aci, inp: str):
    return [log_file for log_file in os.listdir("logs") if inp in log_file]


class LogManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="log", description="Log của bot")
    async def log(
            self,
            interaction: Aci,
            logfile=commands.Param(autocomplete=log_autocompleter)
    ):
        await self.auto_save_logs()
        await interaction.response.defer()
        await interaction.send(file=disnake.File(os.path.join("logs", logfile)))

    @tasks.loop(minutes=1)
    async def auto_save_logs(self):
        with open(os.path.join("logs", datetime.datetime.now().strftime("latest.log")), "w", encoding="utf8") as f:
            for i in logger.LOG:
                f.write(i + "\n")

    @commands.Cog.listener()
    async def on_ready(self):
        with open(os.path.join("logs", datetime.datetime.now().strftime("latest.log")), "w", encoding="utf8") as f:
            f.write("\n")

    @commands.Cog.listener()
    async def on_disconnect(self):
        os.system(f"mv latest.log {datetime.datetime.now().strftime('%y-%m-%d-%H:%M%:%S.log')}")


def setup(bot: commands.Bot):
    bot.add_cog(LogManager(bot))
