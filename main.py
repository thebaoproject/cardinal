import os

import disnake
from disnake.ext import commands
import config_manager as cfg

# Sẽ bị bỏ qua, vì dùng /.
bot = commands.Bot(command_prefix=cfg.read("prefix"))


@bot.event
async def on_ready():
    print("Bot đã khởi động thành công và đã kết nối với Discord.")


if __name__ == "__main__":
    print("Bắt đầu thuật toán khởi động bot.")
    print(
        f"""
     --- THÔNG TIN ---

Token:                  '{cfg.read("token")}';
ID server đăng kí lệnh:  {cfg.read("guild-ids")};
Ngôn ngữ:               '{cfg.read("language")}'.
""")

    func_dir = cfg.read("functions-dir")
    # Code này ăn trộm từ Stack Overflow (tm)
    # Load các phần quan trọng
    for file in os.listdir(func_dir):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"{func_dir}.{file[:-3]}")
                print(f"OK: Đã load chức năng: {file}")
            except disnake.ext.commands.errors.NoEntryPointError:
                print(f"LỖI: Không thể load được chức năng: {file}")

    # Load trò đùa
    try:
        for file in os.listdir("jokes"):
            if file.endswith(".py"):
                try:
                    bot.load_extension(f"jokes.{file[:-3]}")
                    print(f"OK: Đã load trò đùa: {file}")
                except disnake.ext.commands.errors.NoEntryPointError:
                    print(f"LỖI: Không thể load được trò đùa: {file}")
    except FileNotFoundError:
        print("Không có thư mục cho trò đùa. Không load trò đùa.")

    bot.run(cfg.read("token"))
