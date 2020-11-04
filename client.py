import os
import asyncio
import discord
from discord import Client, Intents
from discord.utils import get
from decouple import config

from discord.ext import commands, tasks
from discord.ext.commands import is_owner, Bot, has_permissions, CheckFailure, Context

import git
r = git.Repo.init('')
reader = r.config_reader()
dev = reader.get_value("user","name")

bot = Bot(command_prefix=".", description="BSCoE Class Support Bot", pm_help=True)

bot_settings = {"main channel":"owner-test-channel"}

@bot.event
async def on_ready():
	print("BSCoE Class Support Bot is ready!")
	await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Supporting!"))
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	await bot_channel.send("Good day!")

@bot.event
async def on_member_join(member):
	print(f"{member} has joined a server.")
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	await bot_channel.send(f"Hello {member}!")

@bot.event
async def on_member_remove(member):
	print(f"{member} has left a server.")
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	await bot_channel.send(f"Goodbye {member}!")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.channel.send(f"Command not found!")

#Closes the Bot, Only owners can do it
@bot.command()
@is_owner()
async def close(ctx):
	print(f"BSCoE Class Support Bot is closing!")
	await ctx.channel.send(f"Goodbye for the meantime guys! BSCoE Class Support Bot is closing!")

	os._exit(1)

#When a non-owner tries to execute a close command
@close.error
async def close_error(error, ctx):
	await ctx.channel.send(f"Only the owners are allowed to close me!")

#Sends private message to a user in a group, deletes/purges the recent message which is the command that executes this code
'''@bot.command()
async def message(ctx, *args):
	bot_channel = get(bot.get_all_channels(), name="practice-channel")
	if ctx.message.author.top_role.permissions.administrator:
		await bot_channel.send(f"{arg}, admin")
	else:
		await bot_channel.send(f"{arg}, not admin")'''

#Checks if the user is an admin or not
@bot.command(description="Shows if user is an admin.")
async def admin(ctx):
	if ctx.message.author.top_role.permissions.administrator:
		await ctx.channel.send(f"You're an admin, {ctx.message.author.mention}!")
	else:
		await ctx.channel.send(f"You're not an admin, {ctx.message.author.mention}!")