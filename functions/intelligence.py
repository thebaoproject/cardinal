import disnake
import translations as msg

from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

name = {
    "intelligence": "intelligence",
    "intel": "intel",
    "refreshdtb": "refreshdtb"
}

des = {
    "intelligence": "Câu lệnh tìn báo, nêu thông tin về một người dùng nào đó. Câu cửa miệng của CIA.",
    "intel": "Cách gõ ngắn hơn, cũng tìm kiếm thông tin.",
    "refrestdtb": "Làm mới cơ sở dữ liệu toàn server."
}


class Intelligence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=name["intelligence"], description=des["intelligence"])
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


def setup(bot: commands.Bot):
    bot.add_cog(Intelligence(bot))
