# E hèm. Nghiêm túc này.
import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
import random
import config_manager as cfg

# Commands description
des = {
    "ban": "Cấm một Thành viên khỏi server. Nêu ra số ngày nếu cần cấm tạm thời.",
    "tempban": "Vẫn là cấm nhưng có hạn. Hiện vẫn chưa hoạt động.",
    "unban": "Hủy lệnh cấm cho một thành viên nào đó.",
    "kick": "Thanh trừ một thành viên khỏi server.",
    "warn": "Cảnh cáo một thành viên vì hành động của họ"
}
name = {
    "ban": "ban",
    "unban": "unban",
    "tempban": "tempban",
    "kick": "kick",
    "warn": "warn"
}
# Messages will be randomized to add "tension"
mes = {
    "ban": {
        "public": [
            "Người dùng {usr} đã bị cấm khỏi server, với lí do: {reas} bởi {admin} với thời hạn {dur}",
            "Ủy ban Kiểm Tra Trung Ương, Bộ Chính Trị, Ủy Ban Mặt Trận Spike's Kingdom đại tá {admin} xử đồng chí {"
            "usr} với hình phạt thanh trừ mãi mãi, với tội {reas} với thời hạn {dur}",
            "{admin} xử {usr} án PAY ACC, với lí do là {reas} với thời hạn {dur}",
            "Tòa tuyên phạt bị cáo {usr} với tội CẤM KHỎI SERVER, với lí do đưa ra trong bản cáo trạng của viện "
            "trưởng Viện Kiểm Sát Nhân Dân {admin}: {reas} với thời hạn {dur} "
        ],
        "dm": "Xin lỗi, bạn đã bị cấm khỏi server bởi {admin}, với lí do {reas}",
    },
    "tempban": "Xin lỗi, câu lệnh này chưa được hoàn thành, trong quá trình thử nghiệm.",
    "kick": {
        "public": [
            "Người dùng {usr} bị đuổi khỏi server, vì: {reas} bởi {admin}",
            "Bí thư {admin} của Spike's Kingdom quyết định kỉ luật thành viên {usr}bằng hình thức:\n    - Thanh trừ "
            "vì tội {reas}",
            "PAY ACC {usr}, vì {admin} đã kick với lí do: {reas}"
        ],
        "dm": "Xin lỗi, bạn đã bị đuổi khỏi server bởi {admin} với lí do: {reas}"
    },
    "warn": {
        "public": [
            "Này {usr}, bạn đã bị cảnh cáo về: {content} bởi {admin}",
            "Người dùng {usr} đã bị cảnh cáo bởi {admin} về: {content}"
        ]
    },
    "unban": {
        "public": [
            "Chủ tọa {admin} quyên bố: tha cho bị cáo {usr} vì {reas}",
            "Người dùng {usr} đã được gỡ lệnh cấm bởi {admin} với lí do: {reas}",
            "Thượng Thư Hình Bộ {admin} đã tha chết cho {usr} vì đã được giải oan: {reas}"
        ],
        "dm": "Bạn đã được gỡ lệnh cấm bởi @{admin}, với lí do là: {reas}"
    },
    "perms": {
        "public": [
            "Bạn không có quyền",
            "Định lên mặt à? Bạn không thể thực hiện hành động này đâu!",
            "Đừng có mơ",
            "Còn lâu",
            "Người dùng... À mà thôi."
            "Ai cho bạn dùng câu lệnh này?"
        ]
    }
}


def enough_permission(interaction: Aci):
    if interaction.author.bot:
        return False
    for role_id in cfg.read("admin-roles"):
        if interaction.author.get_role(role_id) is None:
            return False
    return True


class Moderate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Búa ban!
    @commands.slash_command(name=name["ban"], description=des["ban"])
    async def ban(
            self, interaction: Aci,
            member: disnake.Member,
            reason: str = "không xác định",
            duration: str = "mãi mãi"
    ):
        if not enough_permission(interaction):
            interaction.response.send_message(random.choice(mes["perms"]["public"]))
            return
        await interaction.response.send_message(
            random.choice(mes["ban"]["public"]).format(admin=interaction.author.mention, usr=member.mention,
                                                       reas=reason, dur=duration))
        await interaction.author.guild.ban(user=member, reason=reason)
        await member.send(mes["ban"]["dm"].format(admin=interaction.author.mention, reas=reason, dur=duration))

    # Một cách viết khác dễ hiểu hơn.
    @commands.slash_command(name=name["tempban"], description=des["tempban"])
    async def tempban(self, interaction: Aci, member: disnake.Member, reason: str = "không xác định",
                      duration: int = 0):
        if not enough_permission(interaction):
            interaction.response.send_message(random.choice(mes["perms"]["public"]))
            return
        # await self.ban(interaction, member, reason, duration)
        interaction.response.send_message(mes["tempban"])

    @commands.slash_command(name=name["unban"], description=des["unban"])
    async def unban(
            self, interaction: Aci,
            member: disnake.User,
            reason: str = "không xác định",
            duration: str = "mãi mãi"
    ):
        if not enough_permission(interaction):
            interaction.response.send_message(random.choice(mes["perms"]["public"]))
            return
        await interaction.response.send_message(

            random.choice(mes["unban"]["public"]).format(admin=interaction.author.mention, usr=member.mention,
                                                         reas=reason, dur=duration))
        await interaction.author.guild.unban(user=member, reason=reason)
        await member.send(mes["unban"]["dm"].format(admin=interaction.author.mention, reas=reason, dur=duration))

    # Get out!
    @commands.slash_command(name=name["kick"], description=des["kick"])
    async def kick(self, interaction: Aci, member: disnake.Member, reason: str = "không xác định"):
        if not enough_permission(interaction):
            interaction.response.send_message(random.choice(mes["perms"]["public"]))
            return
        await interaction.response.send_message(
            random.choice(mes["kick"]["public"]).format(admin=interaction.author.mention, usr=member.mention,
                                                        reas=reason))
        await member.kick(reason=reason)
        await member.send(mes["kick"]["dm"].format(admin=interaction.author.mention, reas=reason))

    # Warn!
    @commands.slash_command(name=name["warn"], description=des["warn"])
    async def warn(self, interaction: Aci, member: disnake.Member, content: str = "không gì cả"):
        if not enough_permission(interaction):
            interaction.response.send_message(random.choice(mes["perms"]["public"]))
            return
        await interaction.response.send_message(
            random.choice(mes["warn"]["public"]).format(usr=member.mention, admin=interaction.author.mention,
                                                        content=content)
        )


def setup(bot):
    bot.add_cog(Moderate(bot))
