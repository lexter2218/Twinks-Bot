import discord
from discord.ext import commands

from functions import fetch_prefix

from Games.library.gtn import GuessTheNumber
from Games.models import GameDatabaseConfig

from math import log, exp as euler_exponent, e as euler_num

brief_play = "$command-prefix$play [amount]"
help_play = "Clear previous messages.\n\n$command-prefix$play [amount]\n\nNote:\n\t+ Amount should only be positive integers."

brief_rules = "$command-prefix$rules [amount]"
help_rules = "Clear previous messages.\n\n$command-prefix$rules [amount]\n\nNote:\n\t+ Amount should only be positive integers."

brief_quit = "$command-prefix$quit [amount]"
help_quit = "Clear previous messages.\n\n$command-prefix$quit [amount]\n\nNote:\n\t+ Amount should only be positive integers."

brief_channelpoints = "$command-prefix$channelpoints [amount]"
help_channelpoints = "Clear previous messages.\n\n$command-prefix$channelpoints [amount]\n\nNote:\n\t+ Amount should only be positive integers."

brief_coins = "$command-prefix$coins [amount]"
help_coins = "Clear previous messages.\n\n$command-prefix$coins [amount]\n\nNote:\n\t+ Amount should only be positive integers."

class GameConfig(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.available_games = {"guess-the-number":GuessTheNumber}

	#=========================HIDDEN COMMANDS: SHOULD NOT BE ACCESSIBLE BY DISCORD USERS=========================
	#User Authentication
	async def player_authentication(self, message):
		self.user_config = GameDatabaseConfig(message.guild.id)
		self.user_data = self.user_config.fetch_game_data(message.author.id)

		#=========================Saving to Database=========================
		if not self.user_data:
			self.user_data = self.user_config.create_game_data(message.author.id, 0, 0, "", 0, 0, "")

		return self.user_data

	async def string_from_to_dict(self, from_or_to, var_value, separator=("", ""), returned_as_tuple=False):
		if from_or_to == "to":
			if var_value == "":
				if returned_as_tuple:
					return (("", 0), )
				else:
					return {}
			else:
				splitted_message = var_value.split(separator[0])
				try:
					list_message = [tuple(each_pair.split(separator[1])) for each_pair in splitted_message]
				except:
					list_message = [tuple(each_pair.split(separator[0])) for each_pair in splitted_message]
				if returned_as_tuple:
					return tuple(list_message)

				dict_message = {}
				for key, value in list_message:
					dict_message[key] = int(value)

				return dict_message

		elif from_or_to == "from":
			try:
				list_message = [f"{each_key}{separator[1]}{str(var_value[each_key])}" for each_key in var_value]
			except:
				list_message = [f"{each_key}{separator[0]}{str(var_value[each_key])}" for each_key in var_value]
			string_message = separator[0].join(list_message)

			return string_message

	async def coins_management(self, message, add_coins, add_points, source):
		'''
			channel_message_sent is the amount of messages sent by a user in each channel that is in string form.
			This variable should be in dictionary variable but there is no dictionary field in peewee's SqliteDatabase.

			Structure:
				Each key and value is separated by ':___:'
				Example:
					channel-one:___:27

				Each pair is separated by ',|-|, '
				Example:
					channel-one:___:27,|-|,  channel-three:___:96
		'''

		#user_config, user_data = await self.fetch_user_data(message.guild.id, message.author.id)

		if source == "channel":
			self.user_data.channel_points += add_points

			#Change Value of channel message sent
			#Convert String to Dict
			dict_channel_message = await self.string_from_to_dict("to", self.user_data.channel_message_sent, (",|-|, ", ":___:"))
			try:
				dict_channel_message[message.channel.name] += 1
			except:
				dict_channel_message[message.channel.name] = 1
			#Convert Dict to String
			string_channel_message = await self.string_from_to_dict("from", dict_channel_message, (",|-|, ", ":___:"))

			self.user_data.channel_message_sent = string_channel_message

		elif source == "game":
			self.user_data.coins += add_coins
			self.user_data.overall_points += add_points

		self.user_config.update_game_data(self.user_data.tuple_data())
		#self.user_config.close_data()

	async def response_awaiter(self, func, recipient, author_mention):
		bot_response, instant_response = func

		for each_response in bot_response:
			await recipient.send(f"{author_mention}```\n{each_response}```")

		for each_response in instant_response:
			try:
				await each_response
			except discord.Forbidden:
				pass

	#=========================FIRST DESTINATION OF MESSAGES=========================
	async def analyze_user_response(self, message):
		#==============================Channel Points==============================
		#For every message sent by a user, add a point to a player (Message should be sent at al channels except at game channels)
		if not await self.player_authentication(message):
			#This outcome have zero percent chance to come out yet because cemit legitimate validation systerm is not yet working
			await ctx.channel.send("Sorry, but you are not validated as a member, yet!")
			return

		message_length = len(message.content)
		command_prefix = fetch_prefix(message.guild.id)
		len_cmd_prefix = len(command_prefix)

		#==============================Checks the message if it is a command or not==============================
		if message.content.split()[0][0:len_cmd_prefix] == command_prefix:
			accessible_commands = ("coins", "channelpoints", "game")
			exclusive_game_commands = ("play", "rules", "quit", "leaderboards")
			lobby_commands = ("gameprofile", "bag", "bank")

			invoker = message.content.split()[0][len_cmd_prefix:]
			#==============================Accessible Commands game commands can be invoked at all channels==============================
			if invoker in accessible_commands:
				await getattr(self, invoker)(self, message)

			elif invoker in exclusive_game_commands:
				if message.channel.category.name.title() == "Games" and message.channel.name in self.available_games:
					await getattr(self, invoker)(self, message)
				else:
					await message.channel.send(f"{message.author.mention}```\nThis command is only available at game channels.```")

			elif invoker in lobby_commands:
				if message.channel.category.name.title() == "Games" and message.channel.name == "lobby":
					await getattr(self, invoker)(self, message)
				else:
					await message.channel.send(f"{message.author.mention}```\nThis command is only available at game lobby.```")

			elif invoker == "shop":
				if message.channel.category.name.title() == "Games" and message.channel.name == "shop":
					await getattr(self, invoker)(self, message)
				else:
					await message.channel.send(f"{message.author.mention}```\nThis command is only available at game shop.```")

			else:
				#==============================Commands not under Game Configs can be invoked everywhere except game channels==============================
				if message.channel.category.name == "Games" and message.channel.name in self.available_games:
					await message.channel.purge(limit=1)
				else:
					await self.bot.process_commands(message)
		#==============================If message is not a command, checks if it is sent in game channels==============================
		else:
			if message.channel.category.name.title() == "Games" and message.channel.name in self.available_games:
				result, instant_result, final_coins_points = self.available_games[message.channel.name](message).user_response(message)
				await self.response_awaiter((result, instant_result), message.channel, message.author.mention)

				if final_coins_points[0]:
					await self.coins_management(message, final_coins_points[1], final_coins_points[2], "game")
			else:
				#==============================Channel points can only be gathered on non-game channels and non-commands messages==============================
				await self.coins_management(message, message_length, message_length, "channel")

		self.user_config.close_data()


	#=========================EVERY GAME SHOULD HAVE THE FOLLOWING FUNCTIONS=========================
	@commands.command(brief="placeholder", help="placeholder")
	async def play(self, message):
		await self.response_awaiter(self.available_games[message.channel.name](message).start(message), message.channel, message.author.mention)

	@commands.command(brief="placeholder", help="placeholder")
	async def rules(self, message):
		await self.response_awaiter(self.available_games[message.channel.name](message).help(message), message.channel, message.author.mention)

	@commands.command(brief="placeholder", help="placeholder")
	async def quit(self, message):
		await self.response_awaiter(self.available_games[message.channel.name](message).terminate(message), message.channel, message.author.mention)

	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def leaderboards(self, message):
		pass


	#=========================GAME'S UNIQUE COMMANDS=========================
	#For Game/Server Settings
	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def game(self, message):
		#parameters/actions = refresh, fix [game(optional), default: all], install [game], uninstall [game], setup(accessible in all channel), settings [in game prefix(save at Data/core), ]
		pass

	#For Player Game Data
	@commands.command(brief="placeholder", help="placeholder")
	async def coins(self, message):
		#Shows the player, how many coins does he/she has
		if self.user_data:
			await message.channel.send(f"```\nCoins:\t{self.user_data.coins}```")
		else:
			await message.channel.send(f"```\nCoins:\t0```")

	@commands.command(brief="placeholder", help="placeholder")
	async def channelpoints(self, message):
		#Shows the player, how many channel points does he/she has
		if self.user_data:
			#Convert String to Tuple
			tuple_channel_message = await self.string_from_to_dict("to", self.user_data.channel_message_sent, (",|-|, ", ":___:"), True)
			string_count = ""
			try:
				for channel_key, message_sents in tuple_channel_message:
					string_count += f"\t{channel_key}:\t{message_sents}\n"
			except ValueError:
				string_count += "\n"
			await message.channel.send(f"```\nChannel Points:\t{self.user_data.channel_points}\n\nChannel Message Count:\n{string_count}```")
		else:
			await message.channel.send(f"```\nChannel Points:\t0\n\nChannel Message Count:\n\tNone```")

	#Lobby Accessible Commands
	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def gameprofile(self, message):
		pass

	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def bag(self, message):
		pass

	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def bank(self, message):
		pass

	#Shop Accessible Commands
	@commands.command(brief="placeholder", help="placeholder", hidden=True)
	async def shop(self, message):
		#parameters/actions = buy, sell, refund
		pass


def setup(bot):
	bot.add_cog(GameConfig(bot))