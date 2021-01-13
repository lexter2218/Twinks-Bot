import discord
from peewee import SqliteDatabase
from decouple import config
from client import bot


def startup():
    from Data.core import setup as core_models
    core_models()

if __name__ == "__main__":
    startup()
    token = config('BOT_TOKEN')
    
    bot.load_extension("Commands.Admin")
    bot.load_extension("Commands.Member")
    bot.load_extension("Commands.Owner")
    bot.load_extension("Commands.Help")

    #Games
    bot.load_extension("Games.cog")
    bot.run(token)