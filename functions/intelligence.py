import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from storage import Profile

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

msg = {
    "intelligence": """```
-------------- CƠ BẢN -------------
Tên thật:            {name}
Biệt danh:           {nick}
ID:                  {id}
Có nitro từ:         {nitro}
Đăng kí Discord lúc: {res_date}
Đã vào server lúc:   {join_date}
Người mời:           {inviter}
Link mời:            {ilink}
Người tạo link mời   {ulink}
--------------- HÌNH PHẠT ----------------
Bị ban:               {banned}
Người ban:            
```""",
    "refreshdtb": "Đã làm mới cơ sở dữ liệu thành công."
}

# Cho con người

title = "Thông tin tình báo về {name}"


class Intelligence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=name["intelligence"], description=des["intelligence"])
    async def intelligence(self, interaction: Aci, member: disnake.Member):
        user = Profile(interaction.guild, member.id, member.name)
        response = disnake.Embed(
            title=title.format(name=member.name),
            description=msg["intelligence"].format(
                name=member.name,
                nick=member.display_name,
                id=member.id,
                nitro=member.premium_since,
                res_date=member.created_at,
                join_date=member.joined_at,
                inviter=user.inviter.name,
                ilink=user.invite_link,
                ulink=user.invite_creator
            ),
        )
        if member.avatar is not None:
            response.set_image(member.avatar.url)
        await interaction.response.send_message(embed=response)

    @commands.slash_command(name=name["refreshdtb"], description=des["refrestdtb"])
    async def refresh(self, interaction: Aci):
        guild = interaction.guild
        for user in guild.members:
            prof = Profile(guild, user.id, user.name).user
            if prof.name is None:
                prof.user = user
                prof.description = None
                prof.banned = False
                prof.ban_due = None
                prof.inviter = None
                prof.invite_link = None
                prof.invite_creator = None
                prof.commit()

        interaction.response.send_message(msg["refreshdtb"])


def setup(bot: commands.Bot):
    bot.add_cog(Intelligence(bot))
