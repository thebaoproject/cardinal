import disnake
import sympy
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

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
    n = n.replace("(*x", "(x")
    n = n.replace("y", "*y")
    n = n.replace(" *y", "y")
    n = n.replace("+*y", "+y")
    n = n.replace("-*y", "-y")
    n = n.replace("***y", "**y")
    n = n.replace("/*y", "/y")
    n = n.replace("(*y", "(y")
    n = n.replace(")(", ")*(")
    if n[0] == "*":
        n = n[1:]
    return eval(n, {"x": x, "y": y})


class Math(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="math")
    async def math(self, interaction: Aci):
        pass

    @math.sub_command(name="solve", description=disnake.Localized("Giải phương trình.", key="solve"))
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

    @math.sub_command(name="simplify", description=disnake.Localized("Rút gọn đa thức.", key="simplify"))
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
