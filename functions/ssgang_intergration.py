import json
import disnake

from disnake.ext import commands
from functions.music import FakeContext, find_video
from functions.msc import control

YT_VID_MODEL = {
    "title": "",
    "url": "",
    "description": "",
    "uploadChannel": "",
    "uploadDate": ""
}


class SSGIntegration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music_controller = control.Music(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        code = 200
        r = "Success"
        if message.channel.id != 945985193934737438:
            return
        if not message.content.startswith("```json"):
            return
        if message.author.id == self.bot.user.id:
            return

        # Process message
        content = json.loads(message.content[7:len(message.content) - 3])
        for g in self.bot.guilds:
            if g.id == 686814591069585448:
                break
        else:
            return

        for m in g.members:
            if m.id == int(content["payload"]["discordID"]):
                break
        else:
            code = 402
            r = "Invalid discordID"

        ctx = FakeContext(
            author=m,
            guild=g
        )

        if (200, 201).__contains__(code):
            if content.get("from", "") == "server":
                if content["payload"]["command"] == "music.play":
                    try:

                        # this is a choice request.
                        vids = await find_video(content["payload"]["query"])
                        vl = []
                        if len(vids) > 1 and type(vids) == list:
                            for v in vids:
                                a = YT_VID_MODEL.copy()
                                a["url"] = v["link"]
                                a["description"] = v["description"].split("\n")[0] + "..."
                                a["title"] = v["title"]
                                a["uploadChannel"] = v["channel"]["name"]
                                a["uploadDate"] = v["uploadDate"]
                                vl.append(a)
                            r = vl
                            code = 201
                        elif type(vids) == dict:
                            v = vids
                            a = YT_VID_MODEL.copy()
                            a["url"] = v["link"]
                            a["description"] = v["description"].split("\n")[0] + "..."
                            a["title"] = v["title"]
                            a["uploadChannel"] = v["channel"]["name"]
                            a["uploadDate"] = v["uploadDate"]
                            r = a
                            code = 200
                        elif len(vids) == 0:
                            code = 401
                            r = "Requested video not found"

                        if code == 200:
                            await self.music_controller.play(ctx, url=r["url"])

                    except KeyError:
                        try:
                            c = message.to_reference(fail_if_not_exists=True)
                            if type(c.resolved) == disnake.Message:
                                url = c.resolved.content["response"][content["payload"]["choice"]]["url"]
                                await self.music_controller.play(ctx, url=url)
                            else:
                                code = 500
                                r = "Original JSON request deleted by the database."

                        except KeyError:
                            code = 402
                            r = "Invalid JSON request"
                        except commands.CommandError:
                            code = 400
                            r = "You need to be in a voice channel to do that"
                    except commands.CommandError:
                        code = 400
                        r = "You need to be in a voice channel to do that"

                elif content["payload"]["command"] == "music.pause":
                    await self.music_controller.pause(ctx)
                elif content["payload"]["command"] == "music.stop":
                    await self.music_controller.leave(ctx)
                else:
                    code = 404
                    r = "Command not found"

        await message.reply(
            "```json\n" + json.dumps({
                "code": code,
                "response": r
            }, indent=2) + "```"
        )


def setup(bot):
    bot.add_cog(SSGIntegration(bot))
