import disnake
import random
import time
from enum import Enum
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

name = "btvn"
des = "Tìm cách giải bài tập về nhà cho bạn."


class Subjects(Enum):
    Math = 0
    Chem = 1


class Homework(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.slash_command(name=name, description=des)
#    async def index(self, interaction: Aci, subject: Subjects):


def setup(bot: commands.Bot):
    bot.add_cog(Homework(bot))
