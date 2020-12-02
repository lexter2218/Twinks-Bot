import discord
from discord import Client
from discord.utils import get

import asyncio
import sqlite3

from discord.ext import commands
from discord.ext.commands import Bot

from CustomCommands import *

bot = Bot(command_prefix=get_prefix, description="Twinks Bot", pm_help=True, help_command=None)

bot_settings = {"main channel":"owner-test-channel", "announce":"announcements", "general":"general"}

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("twink!!"))
	print("Twinks Bot is ready!")
	for each_guild in bot.guilds:
		bot_channel = get(each_guild.channels, name="owner")
		if bot_channel:
			await bot_channel.send("Good day, I'm Online again!")

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
	customize_prefix(guild, "prefixes.json", "add")
	print(f"I joined {guild}!")

#Event when bot is removed from a guild
@bot.event
async def on_guild_remove(guild):
	#Clears a custom prefix
	customize_prefix(guild, "prefixes.json", "clear")
	print(f"I left {guild}!")

@bot.event
async def on_message(message):
	#=========================Handler if a bot tried to send a command=========================
	try:
		#=========================Making Sure that game channels exist=========================
		if not get(message.guild.categories, name="Palaro"):
			await message.guild.create_category("Palaro")

		game_room_category = get(message.guild.categories, name="Palaro")

		if not get(message.guild.channels, name="guess-the-number"):
			from palaro.GuessTheNumber import GuessTheNumber
			game_room_channel = await message.guild.create_text_channel("guess-the-number", category=game_room_category)
			#=========================Send rules at the top of the channel=========================
			bot_response = GuessTheNumber(message).rules
			for response in bot_response:
				await game_room_channel.send(f"```\n{response}```")

		#=========================Checking the message if it is sent in categories palaro=========================
		if message.channel.category == game_room_category:
			#=========================Make sure that the message is not from the bot=========================
			if message.author.id != 773355955587907584:
				#=========================Message sent in palaro category=========================

				#=========================Handler if a bot tried to send a command=========================
				try:
					#=========================Checks if the message is a command=========================
					if message.content.split()[0][0] == fetch_prefix(message.guild.id):
						await message.channel.purge(limit=1)

						#=========================Handler if a user or bot can not be DMed=========================
						try:
							await message.author.send(f"```\nInvoking of commands is {message.channel.name} is prohibited!```")
						except discord.errors.HTTPException():
							pass

						return
				except IndexError:
					await message.channel.purge(limit=1)
					return

				#=========================Message will now be processed by the game=========================
				if message.channel.name == "guess-the-number":
					from palaro.GuessTheNumber import GuessTheNumber
					bot_response, instant_response = GuessTheNumber(message).user_response(message)

				#=========================Bot Responds to user that the game's ready=========================
				for response in instant_response:
					#=========================Handler if a user or bot can not be DMed=========================
					try:
						await response
					except discord.errors.HTTPException():
						pass
				for response in bot_response:
					await message.channel.send(f"{message.author.mention}\n```\n{response}```")

		else:
			#=========================Message not sent in palaro category=========================
			await bot.process_commands(message)
	except AttributeError:
		return

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