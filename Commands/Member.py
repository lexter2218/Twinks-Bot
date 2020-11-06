import json
import asyncio
import discord
from discord.utils import get
from discord.ext import commands

class Member(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Announcement
	@commands.command()
	async def announce(self, ctx, *, message):
		#Checks if did input a channel
		if message == "":
			await ctx.channel.purge(limit=1)
			return
		else:		
			chan = message.split()
			chosen_channel = []
			#Checks where to send
			for msg in chan:
				if msg[:2] == "--":
					chosen_channel.append(msg[2:])
				elif msg[0:3] == "<@!" and msg[-1] == ">":
					if self.bot.get_channel(int(msg[3:-1])):
						msg = self.bot.get_channel(int(msg[3:-1]))
						chosen_channel.append(msg)
					else:
						await ctx.channel.send(f"{msg[3:-1]} id is not a channel in this server!")
						print("A user tried to announce to a non-existent channel!")
				else:
					break

			print(chosen_channel)

			if len(chosen_channel) == 0:
				chosen_channel.append("announcements")
			else:
				for cha in chosen_channel:
					chan.remove("--" + cha)
			message = " ".join(chan)

			#Checks if announcement has message
			if message == "":
				await ctx.channel.send(f"Announcement has no message!")
				print(f"An announcement has no message!")
				return

			#try/except if channel does not exist
			for cha in chosen_channel:
				bot_channel = get(self.bot.get_all_channels(), name=cha)
				if bot_channel:
					await bot_channel.send(f"{message}")
					print(f"An announcement has been sent by {ctx.message.author}!")
				else:
					await ctx.channel.send(f"{cha} Channel does not exist!")
					print("A user tried to announce to a non-existent channel!")

	#Sends private message to a user in a group, deletes/purges the recent message which is the command that executes this code
	@commands.command()
	async def message(self, ctx, member : discord.Member, *, message=""):
		await ctx.channel.purge(limit=1)
		anon = message.split()
		if anon[0][:2] == "--":
			if anon[0].upper() in ("--A", "--ANONYMOUS"):
				from_msg = "Anonymous"
			anon.remove(anon[0])
			message = " ".join(anon)
		else:
			from_msg = ctx.message.author
		if message == "":
			await ctx.channel.purge(limit=1)
			return
		try:
			await member.send(f"{from_msg} said: {message}")
			print(f"{from_msg} to {member}: {message}")
		except:
			await ctx.message.author.send(f"Hello {ctx.message.author}, you are not allowed to message {member}, try sending a friend request first.")
			print("A message failed to send due to no permissions!")

	#Checks if the user is an admin or not
	@commands.command()
	async def admincheck(self, ctx):
		if ctx.message.author.top_role.permissions.administrator:
			await ctx.channel.send(f"You're an admin, {ctx.message.author.mention}!")
			print(f"{ctx.message.author} is an admin!")
		else:
			await ctx.channel.send(f"You're not an admin, {ctx.message.author.mention}!")
			print(f"{ctx.message.author} is not an admin!")

	#Checks if the user is an admin or not
	@commands.command()
	async def info(self, ctx, member):
		user_id = member
		print(len(user_id))


def setup(bot):
	bot.add_cog(Member(bot))