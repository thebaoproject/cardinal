import sympy


def magic(expr: str):
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
    n = n.replace("(*", "(")
    n = n.replace(")(", ")*(")
    if n[0] == "*":
        n = n[1:]
    print(n)
    return eval(n, {"x": x, "y": y})


sols = sympy.solve(magic("(x+3)(x-2)"), dict=True)
output = ""
# for s in sols:
#     i = [str(z) for z in list(s.items())[0]]
#     output += " = ".join(i) + "\n"
#
a = "".join([j[0] for j in [[" = ".join([str(z) for z in list(s.items())[0]]) + "\n"] for s in sols]])
print(sols)

