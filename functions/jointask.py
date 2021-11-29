import disnake
import config_manager as cfg
from disnake.ext import commands


class JoinTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    def on_member_join(self, member: disnake.Member):
        initialize(member)


def initialize(member: disnake.Member):
    """
    Initializes an member's profile.
    Fancy stuff will be used.

    :param member:
    :return:
    """
    # Roles necessary.
    guild = member.guild
    for role_id in cfg.read("standard-role-ids"):
        for role in guild.roles:
            if role.id == role_id:
                member.add_roles(role)


def setup(bot: commands.Bot):
    bot.add_cog(JoinTasks(bot))
