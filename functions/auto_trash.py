import disnake
from disnake.ext import commands
import config_manager as cfg


class AutoTrash(commands.Cog):
    """
    T R A S H
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Tự tạo reaction trash cho tất cả những tin nhắn đã được gửi đi
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.id == self.bot.user.id:
            await message.add_reaction("🚮")

    # Xóa tất cả các tin nhắn do bot gửi mà có quá nhiều emoji trash
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: disnake.Reaction, user: disnake.Member):
        if reaction.emoji == "🚮" and reaction.count >= 3:
            await reaction.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(AutoTrash(bot))
