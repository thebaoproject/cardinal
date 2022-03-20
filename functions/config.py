import config_manager as cfg
import translations as msg
import utils

from functions.moderation import enough_permission
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

name = "config"
des = "Chỉnh sửa thiết lập bot."


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=name, description=des)
    async def config(
            self,
            interaction: Aci,
            option: str = commands.option_enum(["read", "write"]),
            entry: str = commands.option_enum([
                "rick-rolling",
                "social-credit-channel-ids"
            ]),
            value: str = None
    ):
        if not await enough_permission(interaction):
            return
        if option == "read":
            interaction.response.send_message(msg.get(interaction.author, "config.read")
                                              .format(tag=entry, value=cfg.read(entry)))
        if option == "write":
            arg = utils.normalize_argument(value)
            old = cfg.read(entry)
            cfg.write(entry, arg)
            interaction.response.send_message(msg.get(interaction.author, "config.write")
                                              .format(tag=entry, value=arg, old_value=old))


def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))
