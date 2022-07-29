import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

import config_manager as cfg

# Tụ tập tất cả mọi thứ liên quan đến troll.
# Không buộc phải có cái này. Để cho gọn thôi.
msg = {
    "rickroll": "Này, Rick Astley tặng quà cho bạn này!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "name": "rickroll",
    "description": "Tự Rick Roll bản thân mình. Tăng sự ức chế, bồi bổ sự nhẫn nhịn.",
    "invalid": "Hiện tại Rick Roll không được bật. Hãy thay đổi cài đặt trong `config.py` hoặc gõ lệnh `/config "
               "change <tên> <giá trị>` "
}

RESPONSES = {
    "rickroll": "Này, Rick Astley tặng quà cho bạn này!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "đảng": "```\n       ⠀⠀⠀⠀ ⠀⢀⣤⣀⣀⣀⠀⠈⠻⣷⣄ \n"
            "       ⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠋⠀⠀⠀⠹⣿⣦⡀   \n"
            "       ⠀⠀⢀⣴⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⢹⣿⣧   \n"
            "       ⠀⠀⠙⢿⣿⡿⠋⠻⣿⣿⣦⡀⠀⠀⠀⢸⣿⣿⡆  \n"
            "       ⠀⠀⠀⠀⠉⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⢸⣿⣿⡇  \n"
            "       ⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠈⠻⣿⣿⣶⣿⣿⣿⠁  \n"
            "       ⠀⠀⠀⣠⣿⣿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⡁   \n"
            "       ⢠⣶⣿⣿⠋⠀⠉⠛⠿⠿⠿⠿⠿⠛⠻⣿⣿⣦⡀  \n"
            "       ⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿ \n"
            "ĐẢNG CỘNG SẢN VIỆT NAM QUANG VINH MUÔN NĂM!```",
    "rat": "https://www.youtube.com/watch?v=0R8CpjAYPcY",
    "chicken attack": "https://www.youtube.com/watch?v=miomuSGoPzI",
    "chicken pig attack": "https://www.youtube.com/watch?v=7dAUADjVzv4",
    "lactroi": "https://www.youtube.com/watch?v=m8Kp_hNcPW4",
    "rat 10h": "https://www.youtube.com/watch?v=2TSaAysdHhk",
    "smash mouth ussr": "https://www.youtube.com/watch?v=no7PSouCN_c"
}


class Reply(commands.Cog):
    """
    Never gonna give you up
    Never gonna let you down
    Never gonna run around and desert you
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        c = message.content.lower()
        if message.author.bot or "shitpost" not in c.lower():
            return
        for k, v in RESPONSES.items():
            if k in c:
                await message.reply(v)
                return

    # Còn nếu chú muốn "tự" rickroll mình thì cũng được thôi.
    @commands.slash_command(name="rickroll", description=disnake.Localized("Quà tặng của Rick Astley", key="rickroll"))
    async def rickroll(self, interaction: Aci):
        if cfg.get("jokes.rickRoll"):
            await interaction.response.send_message(msg["rickroll"])
        else:
            await interaction.response.send_message(msg["invalid"])


def setup(bot):
    bot.add_cog(Reply(bot))
