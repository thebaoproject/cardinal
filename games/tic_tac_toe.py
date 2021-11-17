import disnake
import random
import time
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

name = "tictactoe"
des = "Chơi XO không?"
promt = " --- {a} VS {b} ---"
lore = [
    "Ồ, hay này",
    "Lấy bỏng ngô ra đi!",
    "Kịch tính!",
    "Action!",
    "Chơi đi!",
    "Bắt đầu!",
    "Hai kì cùng địch thủ gặp nhau này"
]
controls = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
x = "❎"
o = "🅾"
b = "⬜"


class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name=name, description=des)
    async def tictactoe(self, interaction: Aci, opponent: disnake.Member = None):
        if opponent is None:
            o = "AI"
        else:
            o = opponent.name
        board = [b, b, b, b, b, b, b, b, b]
        await interaction.response.send_message(
            promt.format(a=interaction.author.name, b=o) + "\n*" + random.choice(lore) + "*")
        board_str = ""
        await interaction.channel.send(f"```py\n# DEBUG INFO:\n{board}```")
        for i in range(3):
            for j in range(3):
                board_str += board[i * 3 + j]
            board_str += "\n"

        # Use a seprate message to send the board
        await interaction.channel.send(board_str)
        for reaction in controls:
            await interaction.channel.last_message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: disnake.Reaction, user):
        board = []
        print(1)
        def get_board_from_message():
            print(2)
            for character in reaction.message.content:
                if [x, o, b].__contains__(character):
                    board.append(character)

        # Before placing the move, checking if the opponent won
        rea = []
        if not reaction.me:
            return
        for i in reaction.message.reactions:
            rea.append(i.emoji)
        for emoji in controls:
            if not rea.__contains__(emoji):
                print("gone")
                return
        if user.bot:
            return
        get_board_from_message()
        won = is_win(board)
        print(3)
        board_str = ""
        # Register the player's move
        if board[controls.index(reaction.emoji)] == b:
            board[controls.index(reaction.emoji)] = x
        else:
            board_str =+ "\n Nước đi không hợp lệ!"
        # Place the ai move
        print("AI MOVE: ",ai(board))
        board[ai(board)] = o
        await reaction.message.remove_reaction(reaction.emoji, user)
        for i in range(3):
            for j in range(3):
                board_str += board[i * 3 + j]
            board_str += "\n"

        if won:
            await reaction.message.edit(content=board_str)
        # Checking if after we place the move, we won
        elif is_win(board):
            await reaction.message.channel.send(board_str + "\n AI thắng!")


def log(*args):
    print(args[0:len(args)])
    time.sleep(1)

# Analizes the board with the given depth and play as player specified.
def ai(board: list, depth=2, play_as=o):
    if is_win(board):
        return -1
    if is_full(board):
        return -2
    if play_as == x:
        best = -2
        for i in range(len(board)):
            if board[i] == b:
                board[i] = x
                score = ai(board, depth - 1, o)
                board[i] = b
                if score > best:
                    best = score
        return best
    else:
        best = 2
        for i in range(len(board)):
            if board[i] == b:
                board[i] = o
                score = ai(board, depth - 1, x)
                board[i] = b
                if score < best:
                    best = score
        return best


# Hand crafted (tm)
def is_win(board: list):
    if board[0] == board[1] == board[2] and board[0] != b: return True
    if board[3] == board[4] == board[5] and board[3] != b: return True
    if board[6] == board[7] == board[8] and board[6] != b: return True
    if board[3] == board[5] == board[7] and board[3] != b: return True
    if board[0] == board[4] == board[8] and board[0] != b: return True
    if board[2] == board[4] == board[6] and board[2] != b: return True
    return False


def is_full(board):
    if board.count(b) > 1:
        return False
    else:
        return True


def setup(bot):
    bot.add_cog(TicTacToe(bot))

# Seaky test
if __name__ == "__main__":
    fake_board = [
        b, b, b,
        b, b, b,
        b, b, b
    ]
    # while not (is_full(fake_board) and is_win(fake_board)):
    #     print(f"AI output:", ai(fake_board))
    print(is_win(fake_board))
    while not is_win(fake_board):
        fake_board[ai(fake_board, play_as=x)] = x
        fake_board[ai(fake_board, play_as=o)] = o

        #     fake_board[ai(fake_board)] = x
        #     print("FINAL")
        for i in range(3):
            print("".join(fake_board[i * 3:i * 3 + 3]))
