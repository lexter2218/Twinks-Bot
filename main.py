import discord
from decouple import config
from client import bot
from peewee import SqliteDatabase

from os import listdir
import asyncio

def startup():
    from data.core import setup as core_startup
    core_startup()

async def extension_loader():
    for filename in listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    startup()
    await extension_loader()

    token = config('BOT_TOKEN', cast=str)
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())