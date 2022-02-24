import os
import disnake
import config_manager as cfg

from disnake.ext import commands

# Omitted, because we use / here
bot = commands.Bot(
    command_prefix=cfg.read("prefix"),
    intents=disnake.Intents.all()
)
status = cfg.read("status")

@bot.event
async def on_ready():
    print("Bot đã khởi động thành công và đã kết nối với Discord.")
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name=status))


if __name__ == "__main__":
    print("Bắt đầu thuật toán khởi động bot.")
    print(
        f"""
     --- THÔNG TIN ---

Token:                  '{cfg.read("token")}';
ID server đăng kí lệnh:  {cfg.read("guild-ids")};
Ngôn ngữ:               '{cfg.read("language")}'.
""")

    # Copied from Stack Overflow (tm)
    # Loads important cogs
    for file in os.listdir("functions"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"functions.{file[:-3]}")
                print(f"OK: Đã load chức năng: {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                print(f"LỖI: Không thể load được chức năng: {file}")

    # Loads jokes
    for file in os.listdir("jokes"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"jokes.{file[:-3]}")
                print(f"OK: Đã load trò đùa: {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                print(f"LỖI: Không thể load được trò đùa: {file}")

    # Loads games
    for file in os.listdir("games"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"games.{file[:-3]}")
                print(f"OK: Đã load game: {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                print(f"LỖI: Không thể load được game: {file}")

    bot.run(cfg.read("token"))
