import discord
from peewee import SqliteDatabase
from decouple import config
from client import bot


db = SqliteDatabase('cemit.db')

def startup():
    db.connect()    

    from services.core.models import setup as core_models
    #TODO: AUTOMATIC TABLE DETECTION
    #TODO: Migrations
    core_models()

if __name__ == "__main__":
    startup()
    token = config('BOT_TOKEN')
    
    bot.load_extension("Commands.Admin")
    bot.load_extension("Commands.Member")
    bot.load_extension("Commands.Owner")
    bot.load_extension("Commands.Help")

    #PALARO
    bot.load_extension("Games.cog")
    bot.run(token)