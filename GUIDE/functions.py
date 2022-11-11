from discord.utils import get

from Data.core import db, GuildInitialization as GUILDINIT


def join_or_leave_guild(fetched_guild_id, action):
	if action == "join":
		guild_data = GUILDINIT(guild_id=fetched_guild_id, command_prefix=".")
		guild_data.save()
	elif action == "leave":
		guild_data = GUILDINIT.get(GUILDINIT.guild_id == fetched_guild_id)
		guild_data.delete_instance()
	db.close()

	return guild_data

def fetch_prefix(fetched_guild_id):
	try:
		guild_data = GUILDINIT.get(GUILDINIT.guild_id == fetched_guild_id)
	except:
		guild_data = join_or_leave_guild(fetched_guild_id, "join")

	result = guild_data.command_prefix
	db.close()

	return result

def get_prefix(bot, message):
	return fetch_prefix(message.guild.id)


def member_check(member_id, bot):
	if member_id[:3] == "<@!" and member_id[-1] == ">":
		return bot.get_user(int(member_id[3:-1]))
	else:
		return None

def channel_check(guild, channel_name_id):
	if channel_name_id[:2] == "--":
		return get(guild.channels, name=channel_name_id[2:])
	elif channel_name_id[:2] == "<#" and channel_name_id[-1] == ">":
		return guild.get_channel(int(channel_name_id[2:-1]))
	else:
		return None