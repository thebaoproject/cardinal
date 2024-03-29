import datetime
import os

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

import logger
import translations as msg


async def log_autocompleter(interaction: Aci, inp: str):
    return [log_file for log_file in os.listdir("logs") if inp in log_file]


async def save_logs():
    with open(os.path.join("logs", datetime.datetime.now().strftime("latest.log")), "w", encoding="utf8") as f:
        for i in logger.LOG:
            f.write(i + "\n")


class LogManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="log", description=disnake.Localized("Nhật kí của bot.", key="logs"))
    async def log(
            self,
            interaction: Aci,
            logfile=commands.Param(autocomplete=log_autocompleter)
    ):
        await save_logs()
        await interaction.response.defer()
        await interaction.send(file=disnake.File(os.path.join("logs", logfile)))

    @commands.Cog.listener()
    async def on_ready(self):
        with open(os.path.join("logs", datetime.datetime.now().strftime("latest.log")), "w", encoding="utf8") as f:
            f.write("\n")

    @commands.slash_command(name="savelog", description=disnake.Localized("Lưu file log.", key="savelogs"))
    async def sls(self, interaction: Aci):
        os.rename(os.path.join("bin", "latest.log"),
                  os.path.join("bin", datetime.datetime.now().strftime("%y-%m-%d-%H:%M%:%S.log")))
        await interaction.send(msg.get(interaction.author, "ok"))


def setup(bot: commands.Bot):
    bot.add_cog(LogManager(bot))
