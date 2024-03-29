import disnake
from disnake.ext import commands

import bot_utils as utils
import logger
import storage
import translations as msg
from modules.moderation import enough_permission

LANGUAGE = "en"


class LanguageChooser(disnake.ui.Select):
    def __init__(self):
        super().__init__()

        for lan, lanid in msg.LANG_LIST.items():
            self.add_option(label=lan, value=lanid)

    async def callback(self, interaction: disnake.MessageInteraction):
        dtb = storage.get_dtb()
        data = {
            "name": interaction.user.name,
            "language": self.values[0],
            "dm": True,
            "description": None,
        }
        dtb.child("users").child(str(interaction.user.id)).set(data)
        await interaction.send(msg.get(self.values[0], "setup.languageSuccess")
                               .format(lang=utils.get_key(msg.LANG_LIST, self.values[0])))


class DontSpamMeButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            label=msg.get(LANGUAGE, "setup.noDM"),
            style=disnake.ButtonStyle.red,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.send(
            msg.get(str(interaction.locale), "setup.noDMok")
        )
        storage.get_dtb().child("users").child(
            str(interaction.user.id)).child("dm").set(False)


class Setup(commands.Cog):
    """
    Task that runs when player joins
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="jointask", description=disnake.Localized("Xử lí newbie.", key="jointask"))
    async def jointask(self, interaction, debug=True):
        global LANGUAGE
        LANGUAGE = interaction.locale
        if not await enough_permission(interaction):
            return
        ui = disnake.ui.View()
        ui.add_item(LanguageChooser())
        ui.add_item(DontSpamMeButton())
        if debug:
            await interaction.send(msg.get(interaction.locale.name, "setup.card"), view=ui)
            dtb = storage.get_dtb()
            data = {
                "name": interaction.user.name,
                "language": str(interaction.locale),
                "dm": True,
                "description": None,
                "violations": []
            }
            dtb.child("users").child(str(interaction.user.id)).set(data)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        global LANGUAGE
        LANGUAGE = "em"
        if member.bot:
            return
        logger.info(f"{member} ({member.id}) has joined the server. Executing jointask...")
        ui = disnake.ui.View()
        ui.add_item(LanguageChooser())
        ui.add_item(DontSpamMeButton())
        await member.send(msg.get("en", "setup.card"), view=ui)
        dtb = storage.get_dtb()
        data = {
            "name": member.name,
            "language": "en",
            "dm": True,
            "description": None,
            "violations": []
        }
        dtb.child("users").child(str(member.id)).set(data)


def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))
