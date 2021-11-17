import disnake
import random
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
from enum import Enum
import config_manager as cfg

name = "quacauphale"
des = "Trả lời một câu hỏi cho bạn. Đừng tin vào nó quá."
response = [
    "Đúng", "Ừ", "Có", "Chuẩn luôn", "Không", "Còn lâu", "",
    "Không biết", "HỎI KHÓ THẾ AI MÀ BIẾT???", "Tất nhiên rồi, thế mà cũng hỏi",
    "Không thèm trả lời", "Có thể đúng, mà cũng có thể sai", "????",
    "AAAAAAAAAA", "...", "à, cái đó thì tôi không biết."
]


class Choice(str, Enum):
    answer = "answer"
    choice = "choices"


class MagicBall(commands.Cog):
    """
    Quả cầu thần kì
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name=name, description=des)
    async def qua_cau_pha_le(self, interaction: Aci, option: Choice, data: str):
        if option == Choice.answer:
            await interaction.response.send_message(random.choice(response))
        elif option == Choice.choice:
            # Splits the data into a list of choices seprated with comma
            choices = data.split(",")
            # Randomly chooses one of the choices
            await interaction.response.send_message(random.choice(choices))
        else:
            await interaction.response.send_message("Lựa chọn không rõ.")


def setup(bot: commands.Bot):
    bot.add_cog(MagicBall(bot))
