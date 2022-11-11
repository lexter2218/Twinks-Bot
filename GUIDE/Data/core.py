from peewee import *

db = SqliteDatabase('Data/twinks.db')
db.connect()

# TODO: UserDB

class GuildInitialization(Model):
	guild_id = TextField()
	command_prefix = TextField()

	class Meta:
		database = db


def setup():
	db.create_tables([GuildInitialization])