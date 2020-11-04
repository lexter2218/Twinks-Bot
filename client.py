import os
import asyncio
import discord
import json
from discord import Client, Intents
from discord.utils import get
from decouple import config

from discord.ext import commands, tasks
from discord.ext.commands import is_owner, Bot, has_permissions, CheckFailure, Context

def get_prefix(bot, message):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	try:
		return prefixes[str(message.guild.id)]
	except:
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)

		prefixes[str(message.guild.id)] = "."

		with open("prefixes.json", "w") as f:
			json.dump(prefixes, f, indent=4)

bot = Bot(command_prefix=get_prefix, description="BSCoE Class Support Bot", pm_help=True)

bot_settings = {"main channel":"owner-test-channel", "announce":"announcements"}

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Supporting!"))
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	print("BSCoE Class Support Bot is ready!")
	await bot_channel.send("Good day, I'm online again!")
	await "general".send("Good day, I'm Online again!")

@bot.event
async def on_member_join(member):
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	print(f"{member} has joined a server.")
	await bot_channel.send(f"Hello {member}!")

@bot.event
async def on_member_remove(member):
	bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	print(f"{member} has left a server.")
	await bot_channel.send(f"Goodbye {member}!")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.channel.send(f"Command not found!")
		print(error)

#Event when bot is joing guild
@bot.event
async def on_guild_join(guild):
	#Sets a default prefix that can be changed later
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "."

	with open("prefixes.json", "w") as f:
		json.dump(prefixes, f, indent=4)
	print(f"I joined {guild}!")

#Event when bot is removed from a guild
@bot.event
async def on_guild_remove(guild):
	#Clears a custom prefix
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open("prefixes.json", "w") as f:
		json.dump(prefixes, f, indent=4)
	print(f"I left {guild}!")

#Closes the Bot, Only owners can do it
@bot.command()
@is_owner()
async def close(ctx):
	await ctx.channel.send(f"Goodbye for the meantime guys! BSCoE Class Support Bot is closing!")
	print(f"BSCoE Class Support Bot is closing!")

	os._exit(1)

#When a non-owner tries to execute a close command
@close.error
async def close_error(error, ctx):
	await ctx.channel.send(f"Only the owners are allowed to close me!")
	print(f"A non-owner tried to close me!")

#Announcement
@bot.command()
async def announce(ctx, *, message):
	#Checks if did input a channel
	if message == "":
		await ctx.channel.purge(limit=1)
		return
	else:		
		chan = message.split()
		if chan[0][:2] == "--":
			chosen_channel = chan[0][2:]
			chan.remove(chan[0])
			message = " ".join(chan)
		else:
			chosen_channel = "announcements" 
		bot_channel = get(bot.get_all_channels(), name=chosen_channel)
		await bot_channel.send(f"{message}")
		print(f"An announcement has been sent by {ctx.message.author}!")

#Sends private message to a user in a group, deletes/purges the recent message which is the command that executes this code
@bot.command(description="Send message to a user thru BSCoE Support Bot that is also in this server.\n\n\tFor anonymous Message: .message [recipient's username#discriminator] --a(or --anonymous) [Message]\n\tFor Named Message: .message [recipient's username#discriminator] [Message]\n\nMentioning recipients also works.")
async def message(ctx, member : discord.Member, *, message=""):
	await ctx.channel.purge(limit=2)
	anon = message.split()
	if anon[0][:2] == "--":
		if anon[0].upper() in ("--A", "--ANONYMOUS"):
			from_msg = "Anonymous"
		anon.remove(anon[0])
		message = " ".join(anon)
	else:
		from_msg = ctx.message.author
	if message == "":
		await ctx.channel.purge(limit=1)
		return
	await member.send(f"{from_msg} said: {message}")
	print(f"{from_msg} to {member}: {message}")

#Checks if the user is an admin or not
@bot.command(description="Shows if user is an admin.")
async def admin(ctx):
	if ctx.message.author.top_role.permissions.administrator:
		await ctx.channel.send(f"You're an admin, {ctx.message.author.mention}!")
		print(f"{ctx.message.author.mention} is an admin!")
	else:
		await ctx.channel.send(f"You're not an admin, {ctx.message.author.mention}!")
		print(f"{ctx.message.author.mention} is not an admin!")