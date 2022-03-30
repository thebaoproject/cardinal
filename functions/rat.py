import disnake
import config_manager as cfg

# This file ensures that SpikeBonjour#9179 remains to be the Supreme Leader.
# Isn't meant to be used in production (tyrant/corrupt)


def eat(m: disnake.Member):
    # Always allows if the member ID is SpikeBonjour ID.
    return (m.id == 603577134535147524) and cfg.get("manualConfig.tyrant")
