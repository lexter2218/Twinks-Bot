import os
import discord
from discord import Client, Intents
from discord.utils import get
from decouple import config

from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, is_owner, errors as d_errors

# Permissions bot
default_command_prefix = ">"
bot = commands.Bot(command_prefix=default_command_prefix)

CHANNEL_MAP = {
    'bot': '🤖cemit-discord-bot',
    'valid': '✅validation'
}

@bot.event
async def on_message(message):
    #==============================Checks if user is not a bot==============================
    if not message.author.bot:
        from palaro.cog import GameConfig
        #await GameConfig(bot).analyze_user_response(GameConfig(bot), message, default_command_prefix)
        await GameConfig(bot).analyze_user_response(message, default_command_prefix)
           
@bot.command()
async def hello(ctx):
    member = f"<@{ctx.author.id}>"
    await ctx.channel.send(f"Hello {member} :)")

@bot.command()
@is_owner()
async def close(ctx):
    bot_channel = get(bot.get_all_channels(), name="owner")
    await bot_channel.send(f"Force closing BOT, bye bye")

    os._exit(1)

@bot.event
async def on_ready():
    print(f"DISCORD {bot.user.name}(BOT) Ready!")
    bot_channel = get(bot.get_all_channels(), name="owner")
    await bot_channel.send("Test bot is online")

@bot.event
async def on_member_join(member):
    print(member.name, "joined!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        #Checks if user invoke any command from cog officers
        if ctx.invoked_with in [str(each_command) for each_command in bot.commands if str(each_command.cog_name) == "Officers"]:
            ctx.channel.send("Only officers can invoke this command!")
    elif isinstance(error, commands.MissingPermissions):
        #Checks if the command is in cog Admin
        if ctx.invoked_with in [str(each_command.name) for each_command in bot.commands if str(each_command.cog_name) == "Admin"]:
            if ctx.invoked_with == "clear":
                await ctx.channel.purge(limit=1)
            await ctx.channel.send(f"You are not an admin!")