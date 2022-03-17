import json
import logger

import disnake

from disnake.ext import commands

YT_VID_MODEL = {
    "title": "",
    "url": "",
    "description": "",
}


CODE = {
    200: "Success",
    202: "Paused/resumed successfully",
    400: "You need to be in a voice channel to do that",
    401: "Video not found",
    402: "Invalid discordID",
    403: "Not playing anything",
    404: "Invalid JSON request",
    501: "Unable to play video"
}


class SSGIntergration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.Cog.listeners():




#
# def setup(bot):
#     bot.add_cog(SSGIntegration(bot))
