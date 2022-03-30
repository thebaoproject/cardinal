import disnake
import random
import time
from enum import Enum
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

name = "homework"
des = "Tìm cách giải bài tập về nhà cho bạn."


class Subject(Enum):
    MATH = 0
    CHEMISTRY = 1
    ENGLISH = 2


class Homework(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.slash_command(name=name, description=des)
    # async def homework(
    #     self,
    #     interaction: Aci,
    #     homework: Subject,
    #     content: str
    # ):
    #     if homework == Subject.ENGLISH:


def setup(bot: commands.Bot):
    bot.add_cog(Homework(bot))
