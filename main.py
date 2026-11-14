import disnake
from disnake.ext import commands
import os
from l import keep_alive
bot = commands.Bot(command_prefix='!',test_guilds=["YOUR_SERVER_ID"], intents=disnake.Intents.all())
token = '...'

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

keep_alive()
bot.run(token)
