import disnake
import translations as msg
import storage

from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from functions.moderation import enough_permission


LANGUAGE = "en"

name = {
    "jointask": "jointask",
}

description = {
    "jointask": "Làm việc với người dùng mới vào server",
}


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
        await interaction.send(msg.get(self.values[0], "setup.languageSuccess"))


class DontSpamMeButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            label=msg.get(LANGUAGE, "setup.noDM"),
            style=disnake.ButtonStyle.red,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.send(
            msg.get(interaction.locale, "setup.noDMok")
        )
        storage.get_dtb().child("users").child(str(interaction.user.id)).child("dm").set(False)


class Setup(commands.Cog):
    """
    Task that runs when player joins
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name=name["jointask"], description=description["jointask"])
    async def jointask(self, interaction: Aci, debug=True):
        global LANGUAGE
        LANGUAGE = interaction.locale
        if not enough_permission(interaction):
            return
        ui = disnake.ui.View()
        ui.add_item(LanguageChooser())
        ui.add_item(DontSpamMeButton())
        if debug:
            await interaction.send(msg.get(interaction.locale, "setup.card"), view=ui)
            dtb = storage.get_dtb()
            data = {
                "name": interaction.user.name,
                "language": interaction.locale,
                "dm": True,
                "description": None,
            }
            dtb.child("users").child(str(interaction.user.id)).set(data)


def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))
