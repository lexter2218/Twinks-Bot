import json
import discord
from discord.utils import get

from discord.ext import commands
from discord.ext.commands import Bot

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

bot = Bot(command_prefix=get_prefix, description="BSCoE Class Support Bot", pm_help=True, help_command=None)

bot_settings = {"main channel":"owner-test-channel", "announce":"announcements", "general":"general"}

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.offline)
	#await bot.change_presence(status=discord.Status.offline, activity=discord.Game("Supporting!"))
	#bot_channel = get(bot.get_all_channels(), name=bot_settings["main channel"])
	#await bot_channel.send("Good day, I'm online again!")
	#bot_channel = get(bot.get_all_channels(), name=bot_settings["general"])
	#await bot_channel.send("Good day, I'm Online again!")
	print("BSCoE Class Support Bot is ready!")

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

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.channel.send(f"{ctx.message.content} Command not found!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.channel.send(f"Argument not complete!")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.channel.send(f"Member not found!")
	elif isinstance(error, commands.MissingPermissions):
		#Checks if the command is in cog Admin
		if ctx.invoked_with in [str(each_command.name) for each_command in bot.commands if str(each_command.cog_name) == "Admin"]:
			if ctx.invoked_with == "clear":
				await ctx.channel.purge(limit=1)
			await ctx.channel.send(f"You are not an admin!")
	elif isinstance(error, commands.MissingRole):
		await ctx.channel.send(f"You are not a Moderator!")

	print(error)