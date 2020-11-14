import json
import asyncio
import discord
from discord.ext import commands

from Commands.GuildDataCheck import channel_check, member_check
from Commands.DefaultCommandsInfo import *

class Member(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Announcement
	@commands.command(brief=brief_announce, help=help_announce)
	async def announce(self, ctx, *, message):
		#Recipients - Message Separator
		recipient_with_message = message.split()
		recipient_channels = []
		prepared_message = ""
		for each_channel in recipient_with_message:
			#If word has "--" prefix or has "<@!" as prefix and ">" as suffix, this means that it might be a channel
			if each_channel[:2] == "--" or (each_channel[:2] == "<#" and each_channel[-1] == ">"):
				#Checks if the name(word excluded the "--" prefix) or id(word excluded the "<@!" as prefix and ">" as suffix) is true
				found_channel = channel_check(ctx, channel_name_id=each_channel)
				if found_channel:
					recipient_channels.append(found_channel)
				else:
					await ctx.channel.send(str([each_channel[2:-1] + " id", each_channel[2:]][each_channel[:2] == "--"]) + f" is not a channel in this server!")
					print(f"A user tried to announce to a non-existent channel in {ctx.guild.name}!")
			else:
				#Separates the message from the recipient channels
				prepared_message = recipient_with_message[recipient_with_message.index(each_channel):]
				#Stops the iteration because this word is now the first word of the message
				break

		#Checks if there are any channels collected
		if len(recipient_channels) == 0:
			await ctx.channel.send(f"Please input at least one channel!")
			print(f"An announcement has no recipient!")
			return

		#Checks if announcement has message
		if prepared_message == "":
			await ctx.channel.send(f"Announcement has no message!")
			print(f"An announcement has no message!")
			return
		else:
			prepared_message = " ".join(prepared_message)

		#Sends the announcement for each channel
		for each_channel in recipient_channels:
			await each_channel.send(f"{prepared_message}")
			print(f"An announcement has been sent by {ctx.message.author}!")

	#Sends private message to a user in a group, deletes/purges the recent message which is the command that executes this code
	@commands.command(brief=brief_message, help=help_message)
	async def message(self, ctx, *, message):
		sender = ctx.message.author
		await ctx.channel.purge(limit=1)
		#Recipients - Message Separator
		recipient_with_message = message.split()
		recipient_members = []
		prepared_message = ""
		for each_member in recipient_with_message:
			#If word has "<@!" as prefix and ">" as suffix, this means that it might be a member
			if each_member[:3] == "<@!" and each_member[-1] == ">":
				#Checks if the id(word excluded the "<@!" as prefix and ">" as suffix) is true
				found_member = member_check(ctx, member_name_id=each_member)
				if found_member:
					recipient_members.append(found_member)
				else:
					await sender.send(str([each_member[3:-1] + " id", each_member[2:]][each_member[:2] == "--"]) + f" is not a member of {ctx.guild.name}!")
					print(f"A user tried to message a non-member of {ctx.guild.name}!")
			else:
				#Separates the message from the recipient members
				prepared_message = recipient_with_message[recipient_with_message.index(each_member):]
				#Stops the iteration because this word is now the first word of the message
				break

		#Checks if there are any members collected
		if len(recipient_members) == 0:
			await sender.send(f"Please input at least one member!")
			print(f"A message has no recipient!")
			return

		#Checks if announcement has message
		if prepared_message == "":
			await sender.send(f"Announcement has no message!")
			print(f"A message has no message!")
			return
		else:
			prepared_message = " ".join(prepared_message)

		#Sends the announcement for each member
		for each_member in recipient_members:
			await each_member.send(f"{prepared_message}")
			print(f"A message has been sent by {sender}!")

	#Checks if the user is an admin or not
	@commands.command(brief=brief_admincheck, help=help_admincheck)
	async def admincheck(self, ctx):
		if ctx.message.author.top_role.permissions.administrator:
			await ctx.channel.send(f"You're an admin, {ctx.message.author.mention}!")
			print(f"{ctx.message.author} is an admin!")
		else:
			await ctx.channel.send(f"You're not an admin, {ctx.message.author.mention}!")
			print(f"{ctx.message.author} is not an admin!")

	#Checks if the user is an admin or not
	@commands.command(brief=brief_info, help=help_info)
	@commands.has_role("Moderator")
	async def info(self, ctx):
		for com in self.bot.commands:
			print(com.cog_name)


def setup(bot):
	bot.add_cog(Member(bot))