import disnake
import random
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
from enum import Enum
import datetime

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
        t = "Trả lời" if option == Choice.answer else "Lựa chọn"
        embed = disnake.Embed(
                title=f"Quả cầu Pha lê: {t}",
                description="Quả cầu kì diệu sẽ giúp bạn trả lời thắc mắc. *tHậT 100%:tm:*",
                timestamp=datetime.datetime.now()
            )

        embed.footer.icon_url = interaction.author.avatar.url
        embed.footer.text = f"Được yêu cầu bởi {interaction.author}"
        embed.add_field("Câu hỏi", data, inline=False)

        if option == Choice.answer:
            embed.add_field("Trả lời", random.choice(response), inline=False)
        elif option == Choice.choice:
            choices = data.split(",")
            embed.add_field("Trả lời", random.choice(choices), inline=False)
        else:
            await interaction.response.send_message("Lựa chọn không rõ.")

        await interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(MagicBall(bot))
