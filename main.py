import discord, pkgutil
from decouple import config
from client import bot

if __name__ == "__main__":
    token = config('BOT_TOKEN')
    
    bot.load_extension("Services.AdminCommands")
    bot.run(token)