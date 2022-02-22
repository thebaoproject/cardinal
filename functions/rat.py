import disnake

# This file ensures that SpikeBonjour#9179 remains to be the Superme Leader.
# Isn't meant to be used in production (tyrrant/corrupt)

def eat(m: disnake.Member):
    print(m.id == 603577134535147524)
    return m.id == 603577134535147524