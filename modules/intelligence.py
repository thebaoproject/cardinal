import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

import logger
import translations as msg


class Intelligence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="intelligence",
                            description=disnake.Localized("Liệt kê thông tin tình báo của một thành viên nào đó.",
                                                          key="intelligence"))
    async def intelligence(self, interaction: Aci, member: disnake.Member):
        # user = Profile(interaction.guild, member.id, member.name)
        await interaction.response.defer()
        response = disnake.Embed(
            title=msg.get(interaction.author, "intel.card.title").format(usr=member.name),
            color=disnake.Color.blue()
        )
        time_format = msg.get(interaction.author, "timeFormat")
        time_tags = msg.get(interaction.author, "time")
        response.add_field(msg.get(interaction.author, "intel.card.name"), member.name)
        response.add_field(msg.get(interaction.author, "intel.card.nickname"), member.display_name)
        response.add_field(msg.get(interaction.author, "intel.card.id"), member.id)
        if member.premium_since is None:
            pre_time = msg.get(interaction.author, "no")
        else:
            pre_time = member.premium_since.strftime(time_format)
        response.add_field(msg.get(interaction.author, "intel.card.pre"), pre_time)
        response.add_field(
            msg.get(
                interaction.author, "intel.card.create"
            ),
            member.created_at.strftime(time_format).format(
                h=time_tags["h"],
                m=time_tags["m"],
                s=time_tags["s"],
                d=time_tags["d"],
                mo=time_tags["mo"],
                y=time_tags["y"]
            )
        )
        response.add_field(
            msg.get(
                interaction.author, "intel.card.join"
            ),
            member.joined_at.strftime(time_format).format(
                h=time_tags["h"],
                m=time_tags["m"],
                s=time_tags["s"],
                d=time_tags["d"],
                mo=time_tags["mo"],
                y=time_tags["y"]
            )
        )
        if member.avatar is not None:
            response.set_thumbnail(member.avatar.url)
        await interaction.edit_original_message(embed=response)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        logger.info(
            f"INTELLIGENCE: Message with author {message.author} ({message.author.id}) has been deleted: "
            f"'{message.content}' with ID {message.id} in channel '{message.channel}'"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        logger.info(
            f"INTELLIGENCE: Message with author {before.author} ({before.author.id}) has been edited: old:"
            f"'{before.content}' with ID {before.id} | new: '{after.content}' with ID {after.id} in "
            f"channel '{before.channel}'"
        )


def setup(bot: commands.Bot):
    bot.add_cog(Intelligence(bot))
