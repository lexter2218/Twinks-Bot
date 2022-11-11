import sqlite3
from os.path import exists
from random import randint
from math import cos, log


#=========================EVERY GAME SHOULD HAVE THE FOLLOWING CLASS=========================
class GameDatabaseConfig:
	def __init__(self, fetched_guild_id):
		self.conn = sqlite3.connect(f'Games/data/{fetched_guild_id}.db')
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS GuessTheNumber(
			player_id text,
			secret_number int,
			range_low_number int,
			range_high_number int,
			difficulty text,
			guesses int
			)""")
		self.player_data = None

	class ModelData:
		def __init__(self, game_data):
			self.player_id, self.secret_number, self.range_low_number, self.range_high_number, self.difficulty, self.guesses = game_data

		def tuple_data(self):
			return (self.player_id, self.secret_number, self.range_low_number, self.range_high_number, self.difficulty, self.guesses)

	def create_game_data(self, *game_data):
		self.c.execute("""INSERT INTO GuessTheNumber VALUES {}""".format(game_data))
		self.conn.commit()
		return self.ModelData(game_data)

	def fetch_game_data(self, fetched_player_id):
		self.c.execute("""SELECT * FROM GuessTheNumber WHERE player_id = '{}'""".format(fetched_player_id))
		self.player_data = self.c.fetchone()
		if self.player_data:
			return self.ModelData(self.player_data)
		else:
			return None

	def update_game_data(self, game_data):
		self.c.execute("""UPDATE GuessTheNumber SET secret_number = {}, range_low_number = {}, range_high_number = {}, difficulty = '{}', guesses = {} WHERE player_id = '{}'""".format(game_data[1], game_data[2], game_data[3], game_data[4], game_data[5], game_data[0]))
		self.conn.commit()

	def delete_game_data(self, fetched_player_id):
		self.c.execute("""DELETE FROM GuessTheNumber WHERE player_id = '{}'""".format(fetched_player_id))
		self.conn.commit()

	def close_data(self):
		self.conn.close()


#=========================CLASS THAT IS UNIQUE TO EVERY GAME=========================
class GuessTheNumber:
	def __init__(self, message_or_ctx):
		self.result, self.instant_result = [], []
		self.game_channel = "guess-the-number"
		self.rules = ("Welcome to GUESS THE NUMBER.\nGoal: Guess what number am I thinking.\nTo play:\n\tEasy:\t'play' or 'play e'\n\tHard:\t'play h'\n\tInsane:\t'play i'\nTo quit:\n\t'quit'\nRules:\n\tThe purpose of this channel is to entertain every player.\n\tAll commands invoked in here except game commands are prohibited.\n\tRespect each player.",)
		#=========================Fetching User's Data=========================
		self.fetched_player_id = int(message_or_ctx.author.id)
		self.fetched_guild_id = message_or_ctx.guild.id

		self.player_config = GameDatabaseConfig(self.fetched_guild_id)
		self.player_data = self.player_config.fetch_game_data(self.fetched_player_id)


	#=========================THIS GAME'S UNIQUE FUNCTIONS=========================
	def get_number(self, difficulty):
		if difficulty == "e":
			range_low_number, range_high_number = (0,100)
		elif difficulty == "h":
			range_low_number, range_high_number = (-50,250)
		elif difficulty == "i":
			range_low_number, range_high_number = (-500,500)

		return randint(range_low_number, range_high_number + 1), range_low_number, range_high_number

	def pointing_system(self, guesses, range_low_number, range_high_number):
		total_range = range_high_number - range_low_number + 1
		return int((((total_range / 2) * (1 / cos((guesses / 10) - 1)) - (total_range / 2)) * (log(total_range) + 1 - guesses)) / log(total_range))
		

	#=========================EVERY GAME SHOULD HAVE THE FOLLOWING FUNCTIONS=========================
	def user_response(self, message):
		#Tells if the returned value is the finals points of the player
		final_coins_points = (False, 0)
		#=========================Checking the message if it is a guess or a command=========================
		try:
			user_guess = int(message.content)
		except:
			from CustomCommands import fetch_prefix
			self.instant_result = (message.channel.purge(limit=1), message.author.send(f"```\nOnly game commands or guesses are allowed to be sent in {message.channel.name}.\nIf it was a game command, make sure that the command prefix that you used is {fetch_prefix(message.guild.id)}.```"))
		else:
			#=========================Message is a guess=========================
			if self.player_data:
				#=========================Player has data=========================
				self.player_data.guesses += 1

				if user_guess == self.player_data.secret_number:
					score = self.pointing_system(self.player_data.guesses, self.player_data.range_low_number, self.player_data.range_high_number)
					self.result = (f"Congratulations!\nYou got it in {self.player_data.guesses} {['guess', 'guesses'][self.player_data.guesses == 1]}!\nAcquired: {score} Coins","Do you want to play again?\nTo play:\n\tEasy:\t'play' or 'play e'\n\tHard:\t'play h'\n\tInsane:\t'play i'")
					self.player_config.delete_game_data(self.fetched_player_id)
					final_coins_points = (True, int(score), int(score))
				else:
					number_range = (self.player_data.range_low_number, self.player_data.range_high_number)
					self.result = (f"Sorry, your answer is wrong. Your answer is {['lower', 'higher'][user_guess > self.player_data.secret_number]} than the hidden number.\nMode: {[['Insane', 'Hard'][self.player_data.difficulty == 'h'], 'Easy'][self.player_data.difficulty == 'e']}\nRange: {number_range} both included\nGuesses: {self.player_data.guesses}",)
					self.player_config.update_game_data(self.player_data.tuple_data())
			else:
				#=========================Player has no data=========================
				self.instant_result = (message.channel.purge(limit=1),)
				self.result = ("You are not in a game, yet.\nTo play:\n\tEasy:\t'play' or 'play e'\n\tHard:\t'play h'\n\tInsane:\t'play i'",)

		self.player_config.close_data()
		return self.result, self.instant_result, final_coins_points

	def start(self, message):
		#=========================Checking if player is still in game=========================
		if not self.player_data:
			#=========================Setting up the values=========================
			try:
				difficulty = message.content.split()[1].lower()
				if difficulty not in ("e", "h", "i"):
					self.result = ("Please specify what difficulty do you want to play:\n\n\tEasy:\t'play e'\n\tHard:\t'play h'\n\tInsane:\t'play i'",)
			except IndexError:
				difficulty = "e"

			secret_number, range_low_number, range_high_number = self.get_number(difficulty)
			print(secret_number)
			guesses = 0

			#=========================Saving to Database=========================
			self.player_data = self.player_config.create_game_data(self.fetched_player_id, secret_number, range_low_number, range_high_number, difficulty, guesses)

			self.result = (f"You are now playing Random Number in {[['Insane', 'Hard'][difficulty == 'h'], 'Easy'][difficulty == 'e']} Mode.\n\nGuess the random number which is in between ({range_low_number}, {range_high_number}), both included.",)
		else:
			self.result = ("Please finish your current game first or quit it.\n\nTo quit:\t'quit'",)

		self.player_config.close_data()
		return self.result, self.instant_result

	def help(self, message):
		self.result = self.rules
		self.player_config.close_data()
		return self.result, self.instant_result

	def terminate(self, message):
		if not self.player_data:
			self.result = ("You are not in a game, yet.\nTo play:\n\tEasy:\t'play' or 'play e'\n\tHard:\t'play h'\n\tInsane:\t'play i'",)
		else:
			self.player_config.delete_game_data(self.fetched_player_id)
			self.result = ("Game terminated, you can now play another game.",)
		self.player_config.close_data()
		return self.result, self.instant_result