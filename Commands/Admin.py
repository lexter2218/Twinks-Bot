import json
import asyncio
import discord
from discord.ext import commands

from Commands.DefaultCommandsInfo import *

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Change Command Prefix
	@commands.command(brief=brief_changeprefix, help=help_changeprefix)
	@commands.has_permissions(administrator=True)
	async def changeprefix(self, ctx, prefix):
		#Add prefix limiter
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)

		prefixes[str(ctx.guild.id)] = prefix

		with open("prefixes.json", "w") as f:
			json.dump(prefixes, f, indent=4)
		await ctx.channel.send(f"Commands prefix has been changed to {prefix}")
		print(f"Commands prefix has been changed to {prefix}!")

	#Kick command
	@commands.command(brief=brief_kick, help=help_kick)
	@commands.has_permissions(administrator=True)
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		await member.kick(reason=reason)
		await ctx.channel.send(f"Kicked {member.mention}\n\tReason: {reason}")
		print(f"Kicked {member}\n\tReason: {reason}!")

	#Ban command
	@commands.command(brief=brief_ban, help=help_ban)
	@commands.has_permissions(administrator=True)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason)
		await ctx.channel.send(f"Banned {member.mention}\n\tReason: {reason}")
		print(f"Banned {member}\n\tReason: {reason}!")

	#Unban command
	@commands.command(brief=brief_unban, help=help_unban)
	@commands.has_permissions(administrator=True)
	async def unban(self, ctx, *, member):
		banned_list = await ctx.guild.bans()

		if len(banned_list) != 0:
			if "#" not in member:
				await ctx.channel.send("Member name not in correct format. Should be in name#discriminator format!")
				print(f"Member name format incorrect!")
			else:
				for banned_member in banned_list:
					user = banned_member.user

					if (user.name + "#" + user.discriminator) == member:
						await ctx.guild.unban(user)
						await ctx.channel.send(f"Unbanned {user.mention}")
						print(f"Unbanned {user}!")
						return
		else:
			await ctx.channel.send(f"Nothing to unban!")
			print(f"Banned list is empty!")

	#Show list of banned members
	@commands.command(brief=brief_banlist, help=help_banlist)
	@commands.has_permissions(administrator=True)
	async def banlist(self, ctx):
		banned_list = await ctx.guild.bans()

		if len(banned_list) != 0:
			return_list = ""
			for banned_member in banned_list:
				user = banned_member.user
				return_list += f"\n{user.name}#{user.discriminator}"

			await ctx.channel.send(f"Banned Members:{return_list}")
			print(f"Banned Members:{return_list}")
		else:
			await ctx.channel.send(f"No Banned Members!")
			print(f"Banned List is empty!")

	#Purge command
	@commands.command(brief=brief_clear, help=help_clear)
	@commands.has_permissions(administrator=True)
	async def clear(self, ctx, amount=0):
		amount += 1
		await ctx.channel.purge(limit=amount)
		if amount == 2:
			print(f"{amount} message has been cleared in {ctx.channel}")
		elif amount > 2:
			print(f"{amount} messages have been cleared in {ctx.channel}")

def setup(bot):
	bot.add_cog(Admin(bot))