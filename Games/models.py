import sqlite3


class GameDatabaseConfig:
	def __init__(self, fetched_guild_id):
		self.conn = sqlite3.connect(f'Games/data/{fetched_guild_id}.db')
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS PlayerGameDatabase(
			user_id text,
			overall_points int,
			coins int,
			bag text,
			bank int,

			channel_points int,
			channel_message_sent text
			)""")
		self.player_data = None

	class ModelData:
		def __init__(self, user_data):
			self.user_id, self.overall_points, self.coins, self.bag, self.bank, self.channel_points, self.channel_message_sent = user_data

		def tuple_data(self):
			return (self.user_id, self.overall_points, self.coins, self.bag, self.bank, self.channel_points, self.channel_message_sent)

	def create_game_data(self, *user_data):
		self.c.execute("""INSERT INTO PlayerGameDatabase VALUES {}""".format(user_data))
		self.conn.commit()
		return self.ModelData(user_data)

	def fetch_game_data(self, fetched_player_id):
		self.c.execute("""SELECT * FROM PlayerGameDatabase WHERE user_id = '{}'""".format(fetched_player_id))
		self.player_data = self.c.fetchone()
		if self.player_data:
			return self.ModelData(self.player_data)
		else:
			return None

	def update_game_data(self, user_data):
		self.c.execute("""UPDATE PlayerGameDatabase SET overall_points = {}, coins = {}, bag = '{}', bank = {}, channel_points = {}, channel_message_sent = '{}' WHERE user_id = '{}'""".format(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[0]))
		self.conn.commit()

	def delete_game_data(self, fetched_player_id):
		self.c.execute("""DELETE FROM PlayerGameDatabase WHERE user_id = '{}'""".format(fetched_player_id))
		self.conn.commit()

	def close_data(self):
		self.conn.close()