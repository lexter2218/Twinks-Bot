import discord
from discord import Client

from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

import Twinks
from data.core import GuildInitMF

# bot = Bot(command_prefix="//", description="Twinks 2.0", pm_help=True, help_command=None)
bot = Bot(command_prefix=GuildInitMF().botprefix, intents=discord.Intents.all(), description="Twinks 2.0")

@bot.event
async def on_ready():
    print("Twinks bot Status: OPENING")
    await Twinks.Appearance(bot).Set(status=discord.Status.online, activity="Twinkling!!!!")
    print("Twinks bot Status: PREPARING")
    for each_guild in bot.guilds:
        GuildInitMF().datainit(each_guild.id)
        await Twinks.System_Channel(each_guild, "I'm Online!").greetings()
    print(f"{bot.user.name} Status: READY")

@bot.event
async def on_guild_join(guild):
    await Twinks.System_Channel(guild).greetings()
    print(f"I joined {guild.name}!")

@bot.event
async def on_guild_remove(guild):
    print(f"I left {guild.name}!")

@bot.event
async def on_message(msg):
    print(f"{msg.author} sent a message!")
    if msg.author == bot.user:
        return

    if bot.user.mentioned_in(msg):
        await msg.channel.send(f"Greetings, {msg.author}!")

    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    print(error)