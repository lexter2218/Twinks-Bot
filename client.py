import discord
from discord import Client
from discord.utils import get

import asyncio
import sqlite3

from discord.ext import commands
from discord.ext.commands import Bot

from CustomCommands import *

from os.path import exists
from os import remove


bot = Bot(command_prefix=get_prefix, description="Class Support Bot", pm_help=True, help_command=None)

bot_settings = {"main channel":"owner-test-channel", "announce":"announcements", "general":"general"}

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("as Support!"))
	print("Class Support Bot is ready!")
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
	user_id = int(message.author.id)
	try:
		channel_category = str(message.channel.category)
	except AttributeError:
		return

	if channel_category == "Games":
		if user_id != 773355955587907584:
			game_folder = "#" + str(message.guild.id)
			game_room_id = str(message.channel.id)
			path = f"Games/{game_folder}/{game_room_id}.json"

			#Checks if the user is the one who is trying to communicate with the bot in the game room
			guild_game_data = sqlite3.connect(f"Games/#{message.guild.id}/guild_game_data.db")
			active_rooms = guild_game_data.cursor()
			active_rooms.execute("SELECT users_id FROM activerooms WHERE channel_id = '{}'".format(message.channel.id))
			fetched_users_id = active_rooms.fetchall()
			guild_game_data.commit()
			guild_game_data.close()
			for each_active_room in fetched_users_id:
				if str(user_id) not in each_active_room:
					await message.channel.purge(limit=1)
					try:
						await message.author.send(f"```Sorry, you are not allowed to send messages in game room {message.channel.name}.```")
					except:
						pass
					else:
						return

			#Sets the game of the user
			game_room_game_index = int(message.channel.name.split('-')[0])
			if game_room_game_index == 1:
				from Games.lib.GuessTheNumber import GuessTheNumber
				game_library = GuessTheNumber()
			#Checks the message if it has game command
			if message.content[:2] == "--":
				#Gets the command of the user
				game_command = message.content.split(" ")[0][2].lower()
				try:
					game_command_params = message.content.lower().split(" ")[1:]
				except:
					game_command_params = []

				#Checks the game command invoked by the user
				if game_command == "p":
					bot_response = game_library.start_game(game_command_params, path, str(user_id))
					for response in bot_response:
						await message.channel.send(response)
				elif game_command == "h":
					await message.channel.send(game_library.game_help)
				elif game_command == "s":
					pass
				elif game_command == "q":
					#Deletes the game room
					await message.channel.send("```\nGoodbye!```")
					await message.channel.category.set_permissions(message.author, read_messages=False, send_messages=False)
					await asyncio.sleep(1)
					await message.channel.delete()

					#Erases the room from list of active rooms
					guild_game_data = sqlite3.connect(f"Games/#{message.guild.id}/guild_game_data.db")
					active_rooms = guild_game_data.cursor()
					active_rooms.execute("DELETE FROM activerooms WHERE users_id = '{}'".format(user_id))
					guild_game_data.commit()
					guild_game_data.close()
					if exists(path):
						remove(path)
				else:
					await message.channel.send(f"```\nSorry, there is no action as {game_command}.```")
			else:
				try:
					if message.content[0] == fetch_prefix(message.guild.id):
						await message.channel.purge(limit=1)
						await message.channel.send("```\nNo invoking of commands except game commands in here!```")
					elif exists(path):
						bot_response = game_library.user_response(message, path, str(user_id))
						if bot_response:
							for response in bot_response:
								await message.channel.send(response)
				except IndexError:
					await message.channel.purge(limit=1)
					await message.channel.send("```\nNo invoking of commands except game commands in here!```")
	else:
		await bot.process_commands(message)

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