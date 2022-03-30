from __future__ import annotations

import builtins
import datetime
from typing import Coroutine

import disnake
import logger
import bot_utils as utils
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


async def democracy(interaction: Aci, action: str):
    """
    well its real democracy
    """
    # To Be Implemented (tm)
    # await interaction.send()
    ...


async def enough_permission(interaction: Aci):
    if interaction.author.bot:
        return False

    # Check for RAT module
    try:
        from functions import rat
        return rat.eat(interaction.author)
    except ModuleNotFoundError:
        pass

    for role_id in cfg.get("manualConfig.adminRoles"):
        if interaction.author.get_role(role_id) is None:
            await interaction.response.send_message(random.choice(msg.get(interaction.author, "mod.perms.public")))
            logger.info(f"{interaction.author} tried to get access to administrative commands, but access is denied: "
                        f"not enough permission.")
            return False
    return True


async def say_goodbye(
    to: disnake.ApplicationCommandInteraction | disnake.abc.Messageable,
    member: disnake.Member | disnake.User,
    admin: disnake.Member | disnake.User,
    string: str,
    action: Coroutine = None,
    lang: disnake.User = "en",
    reason: str = None,
    duration: str = None,
    dm: bool = True
):
    """
    The Hammer to execute the moderation commands.
    To avoid repetition.

    :param to: The public channel to send the message to
    :param member: The member to send the message to.
    :param admin: The moderator who punished the member.
    :param string: The codename of the string needed.
    :param action: The function to execute after saying goodbye.
    :type action: function
    :param lang: The user from whom the language will be inferred
    :param reason: The reason for the punishment. Defaults to None.
    :param duration: The duration of the punishment. Defaults to None.
    :param dm: Whether will the member be dm-ed. Will check if they had DMing enabled first. Defaults to True.
    """
    if not enough_permission(to):
        return
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
    if action is not None:
        await action
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
        await say_goodbye(
            interaction,
            member,
            interaction.author,
            "mod.ban",
            interaction.author.guild.ban(user=member, reason=reason),
            interaction.author,
            reason,
            duration
        )

    # Một cách viết khác dễ hiểu hơn.
    @commands.slash_command(name=name["tempban"], description=des["tempban"])
    async def tempban(
        self,
        interaction: Aci, 
        member: disnake.Member, 
        reason: str = "không xác định",
        duration: int = 0
    ):
        ...

    @commands.slash_command(name=name["unban"], description=des["unban"])
    async def unban(
        self, interaction: Aci,
        member: disnake.User,
        reason: str = "không xác định",
        duration: str = "mãi mãi"
    ):
        await say_goodbye(
            interaction,
            member,
            interaction.author,
            "mod.unban",
            interaction.author.guild.unban(user=member, reason=reason),
            interaction.author,
            reason,
            duration
        )

    # Get out!
    @commands.slash_command(name=name["kick"], description=des["kick"])
    async def kick(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        reason: str = "không xác định"
    ):
        await say_goodbye(
            interaction,
            member,
            interaction.author,
            "mod.kick",
            member.kick(reason=reason),
            interaction.author,
            reason
        )

    # Warn!
    @commands.slash_command(name=name["warn"], description=des["warn"])
    async def warn(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        content: str = "không gì cả"
    ):
        await say_goodbye(
            interaction,
            member,
            interaction.author,
            "mod.warn",
            None,
            interaction.author,
            content,
            "",
            False
        )

    # Finally, isolate. Your opinion don't matter to us.
    @commands.slash_command(name=name["isolate"], description=des["isolate"])
    async def isolate(
        self, 
        interaction: Aci, 
        member: disnake.Member, 
        duration: str,
        reason: str = "không gì cả"
    ):
        await say_goodbye(
            interaction,
            member,
            interaction.author,
            "mod.isolate",
            member.timeout(until=utils.handle_time(duration)),
            interaction.author,
            reason,
            duration)


def setup(bot):
    bot.add_cog(Moderate(bot))
