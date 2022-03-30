# This is the bot configuration options.
# We use .py file here so that we can use comments.
# If any of the options is None, it will be searched for as environment variables.
# pLs dOnT pUt aNyCoDe hErE iT wIlL eXeCuTe oN rUnTiMe

CONFIG = {
    # Bot general options.
    # This is used to set up its core functions.
    "general": {
        # The token of the bot. For production environment, you
        # should put it in the environment variables.
        "botToken": None,
        # The prefix of the bot.
        # This will be omitted, as the bot uses slash commands.
        "prefix": ".c",
        # This option will decide whether the bot will mind other bot actions.
        # This won't affect the anti-raid function. You have to toggle it separately.
        "affectOtherBots": False,
        # Sets the default language for the bot.
        # If the bot can't find the language for the user or the bot can't speak
        # it yet, the below language will be used instead.
        "language": "en",
        # The functions place where function cogs is put.
        "functionsDir": "functions",
        # The bot Rich Presence.
        "status": None
    },
    # This is the manual configuration options.
    "manualConfig": {
        # The bot guilds for the bot to register the slash command locally.
        "guildIds": [],
        # The roles if anyone has can execute admin commands.
        "adminRoles": [754928367115174010],
        # The channel that the bot will listen to "prevent bad knowledge"
        "socialCreditChannelIds": [929628750344249344],
        # The role members will be given when they join the server
        "standardRoleIds": [867313373980393482],
        # Well enables this and the author can always use admin commands :)
        # See functions/rat.py for details
        "tyrant": True,
        # If you want your server to have D E M O C R A C Y
        "democracy": True
    },
    # Bot backend options.
    "backend": {
        # The Firebase database URL
        "fireDtb": None,
        # Firebase API key
        "fireApiKey": None,
        # Rapid API key
        "rapidApiKey": None,
    },
    # The Anti Raid feature settings
    "antiRaid": {
        "enable": False,
        # The point needed for the user to be flagged as "raider"
        "spamThreshold": 0.6,
        # How many messages have the user send in a row to be counted as spam
        "messageSpamAmount": 5,
        # How many admin actions the user have to made
        "adminActionAmount": 5,
    },
    "jokes": {
        "rickRoll": True,
    },
    "autoTrash": {
        "enabled": True,
        "trashEmoji": "🚮"
    }
}

# hey some (complicated) code here
pass
...
pass
