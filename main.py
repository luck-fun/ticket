import disnake
from disnake.ext import commands
import os
from l import keep_alive
bot = commands.Bot(command_prefix='!',test_guilds=[1157921979643465820], intents=disnake.Intents.all())
token = '...'

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

keep_alive()
bot.run(token)
