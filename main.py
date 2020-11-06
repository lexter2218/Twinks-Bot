import discord, pkgutil
from decouple import config
from client import bot

if __name__ == "__main__":
    token = config('BOT_TOKEN')
    
    bot.load_extension("Commands.Admin")
    bot.load_extension("Commands.Member")
    bot.load_extension("Commands.Owner")
    bot.load_extension("Commands.Help")
    bot.run(token)