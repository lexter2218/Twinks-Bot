from discord.utils import get

def member_check(ctx, member_name_id):
	if member_name_id[:3] == "<@!" and member_name_id[-1] == ">":
		return ctx.guild.get_member(int(member_name_id[3:-1]))
	else:
		return None

def channel_check(ctx, channel_name_id):
	if channel_name_id[:2] == "--":
		return get(ctx.guild.channels, name=channel_name_id[2:])
	elif channel_name_id[:2] == "<#" and channel_name_id[-1] == ">":
		return ctx.guild.get_channel(int(channel_name_id[2:-1]))
	else:
		return None