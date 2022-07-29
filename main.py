import logging
import os
import sys

import disnake
from disnake.ext import commands

import config_manager as cfg
import logger

# Omitted, because we use / here
bot = commands.Bot(
    command_prefix=cfg.get("general.prefix"),
    intents=disnake.Intents.all()
)
status = cfg.get("general.status")


@bot.event
async def on_ready():
    logger.info("Bot has connected to Discord successfully")
    logger.info(f"Logged in as {bot.user.name} with ID {bot.user.id}")
    logger.info("Applying Rich Presence...")
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=status))
    logger.info("Done!")


if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(level=logging.INFO)
    log_level = logger.DEBUG if "--debug" in sys.argv else logger.INFO
    logger.set_min_level(log_level)
    logger.info("Bot staring algorithm is initiated")
    logger.info(f"Using token '***************************************'")
    logger.info(f"Loading locales")
    bot.i18n.load("translations/comm/")
    logger.info(f"Starting Cogs initiation")
    # Copied from Stack Overflow (tm)
    # Loads important cogs
    for file in os.listdir("modules"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"modules.{file[:-3]}")
                logger.info(f"Successfully loaded function cog {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                logger.warning(f"Cannot load function cog {file}: no setup() method found")

    # Loads jokes
    for file in os.listdir("jokes"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"jokes.{file[:-3]}")
                logger.info(f"Successfully loaded joke cog {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                logger.warning(f"Cannot load joke cog {file}: no setup() method found")

    logger.info("Running bot with token...")
    bot.run(cfg.get("general.botToken"))
