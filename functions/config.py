import disnake
import config_manager as cfg
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

name = "config"
des = "Chỉnh sửa thiết lập bot."

mes = {
    "cfg": {
        "read": "Giá trị của mục `{tag}` là `{value}`",
        "write": "Đã ghi giá trị `{value}` vào `{tag}`, đè lên giá trị cũ là `{old_value}`"
    }
}


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=name, description=des)
    async def config(self, interaction: Aci, option: str, entry: str, value: str = None):
        if option == "read":
            interaction.response.send_message(mes["cfg"]["read"].format(tag=entry, value=cfg.read(entry)))
        if option == "write":
            old = cfg.read(entry)
            cfg.write(entry, value)
            interaction.response.send_message(mes["cfg"]["write"].format(tag=entry))
