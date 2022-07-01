import disnake
import sympy
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
import translations as msg

def to_expression(expr: str):
    """
    Converts from normal string representation to math expression.

    :param expr: the string representation.
    """
    x = sympy.symbols("x")
    y = sympy.symbols("y")
    n = expr.replace("x", "*x")
    n = n.replace(" *x", "x")
    n = n.replace("+*x", "+x")
    n = n.replace("-*x", "-x")
    n = n.replace("^", "**")
    n = n.replace("***x", "**x")
    n = n.replace("/*x", "/x")
    n = n.replace("y", "*y")
    n = n.replace(" *y", "y")
    n = n.replace("+*y", "+y")
    n = n.replace("-*y", "-y")
    n = n.replace("***y", "**y")
    n = n.replace("/*y", "/y")
    return eval(n, {"x": x, "y": y})


class Math(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="math", description="Liên lạc với Ngô Bảo Châu")
    async def math(self, interaction: Aci):
        pass

    @math.sub_command(name="solve", description="Giải phương trình ez")
    async def solve(self, interaction: Aci, equation: str):
        eq = to_expression(equation)
        try:
            sol_list = sympy.solve(eq)
            await interaction.response.send_message(
                msg.get(interaction.author, "math.solist").format(sol=len(sol_list)) + "```" + "".join(
                    # No, this is not obfuscated;
                    # but we leave understanding this list comprehension as an excerise for the reader.
                    [j[0] for j in [[" = ".join([str(z) for z in list(s.items())[0]]) + "\n"] for s in sol_list]]
                ) + "```"
            )
        except NameError:
            await interaction.response.send_message(msg.get(interaction.author, "math.error"))

    @math.sub_command(name="simplify", description="Ông thần rút gọn")
    async def simplify(self, interaction: Aci, equation: str):
        ex = to_expression(equation)
        try:
            sol_list = sympy.simplify(ex)
            await interaction.response.send_message(
                msg.get(interaction.author, "math.simplify") + "```" + sympy.pretty(sol_list) + "```"
            )
        except NameError:
            await interaction.response.send_message(msg.get(interaction.author, "math.error"))


def setup(bot: commands.Bot):
    bot.add_cog(Math(bot))
