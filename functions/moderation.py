import datetime

import disnake

import logger
import utils
import random
import translations as msg
import config_manager as cfg
import storage

from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

# Commands description
des = {
    "ban": "Cấm một Thành viên khỏi server. Nêu ra số ngày nếu cần cấm tạm thời.",
    "tempban": "Vẫn là cấm nhưng có hạn. Hiện vẫn chưa hoạt động.",
    "unban": "Hủy lệnh cấm cho một thành viên nào đó.",
    "kick": "Thanh trừ một thành viên khỏi server.",
    "warn": "Cảnh cáo một thành viên vì hành động của họ",
    "isolate": "Khóa mồm một thành viên. VD cho thời gian hợp lệ: 31/11/2011 20:29:43 hay 5h4m3s"
}
name = {
    "ban": "ban",
    "unban": "unban",
    "tempban": "tempban",
    "kick": "kick",
    "warn": "warn",
    "isolate": "isolate"
}
# Messages will be randomized to add "tension"


async def enough_permission(interaction: Aci):
    if interaction.author.bot:
        return False

    # Check for RAT module
    try:
        from functions import rat
        # Tyrrant
        return rat.eat(interaction.author)
    except ModuleNotFoundError:
        pass

    for role_id in cfg.read("admin-roles"):
        if interaction.author.get_role(role_id) is None:
            await interaction.response.send_message(random.choice(msg.get(interaction.author, "mod.perms.public")))
            logger.info(f"{interaction.author} tried to get access to administrative commands, but access is denied: "
                        f"not enough premission.")
            return False
    return True


async def say_goodbye(
    to,
    member,
    admin: disnake.Member,
    string: str,
    lang: disnake.User,
    reason: str = None,
    duration: str = None,
    dm: bool = True
):
    """
    Says goodbye to a member when he is punished by a moderation command.

    Args:
        to (disnake.ApplicationCommandInteraction | disnake.Messagable): The public channel to send the message to
        member (disnake.Member): The member to send the message to.
        admin (disnake.Member): The moderator who punished the member.
        string (str): The codename of the string needed.
        lang (disnake.User): The user from whom the language will be infered
        reason (str, optional): The reason for the punishment. Defaults to None.
        duration (str, optional): The duration of the punishment. Defaults to None.
        dm (bool, optional): Whether will the member be dm-ed. Will check if they had dm enabled first. Defaults to True.
    """
    if reason is None:
        nreason = msg.get(lang, "mod.unspecifiedReason")
    else:
        nreason = reason
    if duration is None:
        nduration = msg.get(lang, "mod.forever")
    else:
        nduration = duration
    await to.send(
        random.choice(msg.get(lang, string + ".public")).format(
            usr=member.mention,
            admin=admin.mention,
            dur=nduration,
            reas=nreason
        )
    )
    if dm and storage.get_dtb().child("users").child(str(member.id)).child("dm").get():
        await member.send(
            random.choice(msg.get(lang, string + ".dm")).format(
                admin=admin.name,
                dur=nduration,
                reas=nreason
            )
        )
    logger.success(f"{to.author} ({to.author.id}) has used {string} on {member} ({member.id})")
    punishments = storage.get_dtb().child("users").child(str(member.id)).child("violations").child(string)
    punishments_list = punishments.get()
    punishments_list.append({
        "time": datetime.datetime.now().timestamp(),
        "type": string,
        "adminID": to.author.id,
        "reason": reason,
        "duration": duration,
    })
    punishments.set(punishments_list)


class Moderate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Búa ban!
    @commands.slash_command(name=name["ban"], description=des["ban"])
    async def ban(
        self, 
        interaction: Aci,
        member: disnake.Member,
        reason: str = None,
        duration: str = None
    ):
        if not enough_permission(interaction):
            return

        await say_goodbye(interaction, member, interaction.author, "mod.ban", interaction.author, reason, duration)
        await interaction.author.guild.ban(user=member, reason=reason)

    # Một cách viết khác dễ hiểu hơn.
    @commands.slash_command(name=name["tempban"], description=des["tempban"])
    async def tempban(
        self,
        interaction: Aci, 
        member: disnake.Member, 
        reason: str = "không xác định",
        duration: int = 0
    ):
        if not enough_permission(interaction):
            return
        # await self.ban(interaction, member, reason, duration)
        # await interaction.response.send_message(mes["tempban"])

    @commands.slash_command(name=name["unban"], description=des["unban"])
    async def unban(
        self, interaction: Aci,
        member: disnake.User,
        reason: str = "không xác định",
        duration: str = "mãi mãi"
    ):
        if not enough_permission(interaction):
            return

        await say_goodbye(interaction, member, interaction.author, "mod.unban", interaction.author, reason, duration)
        await interaction.author.guild.unban(user=member, reason=reason)

    # Get out!
    @commands.slash_command(name=name["kick"], description=des["kick"])
    async def kick(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        reason: str = "không xác định"
    ):
        if not enough_permission(interaction):
            return
        await say_goodbye(interaction, member, interaction.author, "mod.kick", interaction.author, reason)
        await member.kick(reason=reason)

    # Warn!
    @commands.slash_command(name=name["warn"], description=des["warn"])
    async def warn(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        content: str = "không gì cả"
    ):
        if not enough_permission(interaction):
            return
        await say_goodbye(interaction, member, interaction.author, "mod.warn", interaction.author, content, "", False)

    # Finally, isolate. Your opinion don't matter to us.
    @commands.slash_command(name=name["isolate"], description=des["isolate"])
    async def isolate(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        duration: str,
        reason: str = "không gì cả"
    ):
        if not enough_permission(interaction):
            return
        await say_goodbye(interaction, member, interaction.author, "mod.isolate", interaction.author, reason, duration)
        await member.timeout(until=utils.handle_time(duration))


def setup(bot):
    bot.add_cog(Moderate(bot))
