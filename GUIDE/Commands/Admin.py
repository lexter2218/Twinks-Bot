import json
import asyncio
import discord
from discord.ext import commands

brief_changeprefix = "$command-prefix$changeprefix [new prefix]"
help_changeprefix = "Customize the prefix of your commands in this server.\n\n$command-prefix$changeprefix [new prefix(special characters)]\n\nNote:\n\t+ Only special characters of non-letter or non-number characters could be used as new prefix.\n\t+ Make sure that this is the only bot that will be using that command prefix or it will trigger both if they have same commands."

brief_kick = "$command-prefix$kick [mention member] [reason(optional)]"
help_kick = "Kick members.\n\n$command-prefix$kick [member] [reason(optional)]\n\nNote:\n\t+ If the reason is not stated, it will be automatically set to None.\n\t+ Members should only be in two formats: member mention or \"<@!member-id>\"\ni.e.\n\t$command-prefix$kick @ProgrammingDoctor @ManOfSteel <@!952952033535491809> Negative Attitude\n\n\tAll of the members will be kicked out of the server with the reason of Negative Attitude."

brief_ban = "$command-prefix$ban [mention member] [reason(optional)]"
help_ban = "Ban members.\n\n$command-prefix$ban [member] [reason(optional)]\n\nNote:\n\t+ If the reason is not stated, it will be automatically set to None.\n\t+ Members should only be in two formats: member mention or \"<@!member-id>\"\ni.e.\n\t$command-prefix$ban @ProgrammingDoctor @ManOfSteel <@!952952033535491809> Negative Attitude\n\n\tAll of the members will be banned from entering the server and from receiving working invitations with the reason of Negative Attitude."

brief_banlist = "$command-prefix$banlist"
help_banlist = "Sends the list of the banned members with reasons.\n\n$command-prefix$banlist"

brief_unban = "$command-prefix$unban [members]"
help_unban = "Unban members.\n\n$command-prefix$unban [members]\n\nNote:\n\t+ Members should only be in two formats: \"name\" + \"#\" + \"discriminator (four numbers after # sign)\" or \"<@!member-id>\"\ni.e.\n\t$command-prefix$ban ProgrammingDoctor#6969 ManOfSteel#7171 <@!952952033535491809>\n\n\tAll of the members will be unbanned from the server and can now receive working invitations."

brief_clear = "$command-prefix$clear [amount]"
help_clear = "Clear previous messages.\n\n$command-prefix$clear [amount]\n\nNote:\n\t+ Amount should only be positive integers."

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Change Command Prefix
	@commands.command(brief=brief_changeprefix, help=help_changeprefix)
	@commands.has_permissions(administrator=True)
	async def changeprefix(self, ctx, prefix):
		if len(prefix) == 1:
			from Data.core import db, GuildInitialization as GUILDINIT

			guild_data = GUILDINIT.get(GUILDINIT.guild_id == ctx.guild.id)
			guild_data.command_prefix = prefix
			guild_data.save()

			await ctx.channel.send(f"Commands prefix has been changed to {prefix}")
		else:
			await ctx.channel.send(f"Command Prefix should only have one character.")

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

	#Create Channel command
	@commands.command(hidden=True)
	@commands.has_permissions(administrator=True)
	async def create(self, ctx, channel_name, text_voice="t", category=None):
		if category:
			  category = await ctx.guild.create_category_channel(category)
		if text_voice.lower() == "t":
			await ctx.guild.create_text_channel("-".join(channel_name.split("_")), category=category)
		elif text_voice.lower() == "v":
			await ctx.guild.create_voice_channel("-".join(channel_name.split("_")), category=category)



def setup(bot):
	bot.add_cog(Admin(bot))