import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

name = {
    "intelligence": "intelligence",
    "intel": "intel"
}

des = {
    "intelligence": "Câu lệnh tìn báo, nêu thông tin về một người dùng nào đó. Câu cửa miệng của CIA.",
    "intel": "Cách gõ ngắn hơn, cũng tìm kiếm thông tin."
}

# Cho con người
content = """
Tên thật:            `{name}`
Biệt danh:           `{nick}`
ID:                  `{id}`
Có nitro từ:         `{nitro}` 
Đăng kí Discord lúc: `{res_date}`
Đã vào server lúc:   `{join_date}`
"""
# Cho bot
content_bot = """
Tên thật:            `{name}`
Biệt danh:           `{nick}`
Người tạo ra bot:    `{owner}`
ID người tạo ra bot: `{ownerid}`
ID bot:              `{id}`
Đăng kí Discord lúc: `{res_date}`
Đã vào server lúc:   `{join_date}`

"""

title = "Thông tin tình báo về {name}"


class Intelligence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=name["intelligence"], description=des["intelligence"])
    async def intelligence(self, interaction: Aci, member: disnake.Member):
        response = disnake.Embed(
            title=title.format(name=member.name),
            description=content.format(
                name=member.name,
                nick=member.display_name,
                id=member.id,
                nitro=member.premium_since,
                res_date=member.created_at,
                join_date=member.joined_at
            ),
        )
        if member.avatar is not None:
            response.set_image(member.avatar.url)
        await interaction.response.send_message(embed=response)


def setup(bot: commands.Bot):
    bot.add_cog(Intelligence(bot))
