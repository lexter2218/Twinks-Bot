import json
from os.path import exists
from discord.utils import get

def get_prefix(bot, message):
	if not exists("prefixes.json"):
		with open("prefixes.json", "w+") as f:
			json.dump({}, f)
			prefixes = {}
	else:
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)
		
	if str(message.guild.id) not in prefixes:
		with open("prefixes.json", "w+") as f:
			prefixes[str(message.guild.id)] = "."
			json.dump(prefixes, f, indent=4)

	return prefixes[str(message.guild.id)]

def customize_prefix(guild, target_file, action):
	with open(target_file, "r+") as f:
		prefixes = json.load(f)

	if action == "add":
		prefixes[str(guild.id)] = "."
	elif action == "clear":
		prefixes.pop(str(guild.id))

	with open("prefixes.json", "w+") as f:
		json.dump(prefixes, f, indent=4)

def fetch_prefix(guild_id):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)
	return prefixes[str(guild_id)]

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