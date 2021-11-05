import disnake
from disnake.ext import commands
import config_manager as cfg

# Tụ tập tất cả mọi thứ liên quan đến troll.
# Không buộc phải có cái này. Để cho gọn thôi.
msg_rickroll = {
    "rickroll": "Này, Rick Astley tặng quà cho bạn này!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "name": "rickroll",
    "description": "Tự Rick Roll bản thân mình. Tăng sự ức chế, bồi bổ sự nhẫn nhịn.",
    "invalid": "Hiện tại Rick Roll không được bật. Hãy thay đổi cài đặt trong `config.json` hoặc gõ lệnh `/config "
               "change <tên> <giá trị>` "
}


class RickRoll(commands.Cog):
    """
    Negver gonna give you up
    Never gonna let you down
    Never gonna run around and desert you
    """

    def __init__(self, bot):
        self.bot = bot

    # Nếu người đồng chí muốn "bắt tin" chữ rickroll.
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if (not message.author.bot) and ("rick" in message.content) and cfg.read("rick-rolling"):
            await message.reply(msg_rickroll["rickroll"])
            # Nếu không được bật thì im lặng.
            # else:
            #     await message.reply(
            #         "Hiện tại Rick Roll không được bật. Hãy thay đổi cài đặt trong `config.json` hoặc gõ "
            #         "lệnh `/config change <tên> <giá trị>`")

    # Còn nếu chú muốn "tự" rickroll mình thì cũng được thôi.
    @commands.slash_command(name=msg_rickroll["name"], description=msg_rickroll["description"])
    async def rickroll(self, interaction: disnake.Interaction):
        if cfg.read("rick-rolling"):
            await interaction.response.send_message(msg_rickroll["rickroll"])
        else:
            await interaction.response.send_message(msg_rickroll["invalid"])


def setup(bot):
    bot.add_cog(RickRoll(bot))
