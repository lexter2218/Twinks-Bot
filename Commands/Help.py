import os
import asyncio
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands
from discord import Embed, Client, Guild
from discord.ext.commands import Bot, CommandNotFound

from CustomCommands import channel_check, member_check, fetch_prefix
from Commands.DefaultCommandsInfo import brief_help, help_help

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief=brief_help, help=help_help)
	async def help(self, ctx, options="All", *, send_to=None):
		options = options.title()
		#Collecting all recipients
		if send_to != None:
			pseudo_recipients = send_to.split()
		else:
			pseudo_recipients = ["--" + str(ctx.message.channel)]

		#fetches the commmand-prefix
		prefix = fetch_prefix(ctx.guild.id)

		#Recipient Identifier
		recipients, recipient_type, unknown_recipient = [], [], []
		for recipient in pseudo_recipients:
			#If word has "--" prefix or has "<@!" as prefix and ">" as suffix, this means that it might be a channel or member
			if recipient[:2] == "--" or ((recipient[:3] == "<@!" or recipient[:2] == "<#") and recipient[-1] == ">"):
				#Checks if recipient is member or channel of guild
				recipient_is_member = member_check(member_id=recipient, bot=self.bot)
				recipient_is_channel = channel_check(ctx.guild, channel_name_id=recipient)
				if recipient_is_member:
					recipients.append(recipient_is_member)
					recipient_type.append("U")
				elif recipient_is_channel:
					recipients.append(recipient_is_channel)
					recipient_type.append("C")
				else:
					await ctx.channel.send(str([[recipient[3:-1], recipient[2:-1]][recipient[:2] == "<#"] + " id", recipient[2:]][recipient[:2] == "--"]) + f" is not a channel in this server!")
					print("A user tried to send help commands to a non-existent " + str(["id", "name"][recipient[:2] == "--"]) + f" in {ctx.guild.name}!")
			else:
				unknown_recipient.append(recipient)
				continue

		if len(unknown_recipient) == 1:
			unknown_recipient = unknown_recipient[0]
			await ctx.channel.send(f"{unknown_recipient} is not in correct format.\n\tFor channel name:\t{prefix}help --a --recipient_name\n\tFor member id:\t{prefix}help --a <@!recipient_id>\n\tFor channel id:\t{prefix}help --a <#recipient_id>.")
		elif len(unknown_recipient) > 1:
			unknown_recipient = ", ".join(unknown_recipient)
			await ctx.channel.send(f"Recipients ({unknown_recipient}) are not in correct format.\n\tFor channel name:\t{prefix}help --a --recipient_name\n\tFor member id:\t{prefix}help --a <@!recipient_id>\n\tFor channel id:\t{prefix}help --a <#recipient_id>.")

		#Copies the list of all the commands loaded
		all_commands_list = self.bot.commands.copy()
		all_commands_list_names = [each_command.name for each_command in all_commands_list]
		member_commands, admin_commands, owner_commands = [], [], []
		member_commands_names, admin_commands_names, owner_commands_names = [], [], []
		for each_command in all_commands_list:
			if not each_command.hidden:
				if each_command.cog_name in ("Member", "Help"):
					member_commands.append(each_command)
					member_commands_names.append(each_command.name)
				elif each_command.cog_name == "Admin":
					admin_commands.append(each_command)
					admin_commands_names.append(each_command.name)
				elif each_command.cog_name == "Owner":
					owner_commands.append(each_command)
					owner_commands_names.append(each_command.name)

		def commands_interator(each_name, categories):
			if categories[each_name] in (member_commands, admin_commands) or (owner_access and categories[each_name] == owner_commands):
				new_name = categories[each_name][0].cog_name
				each_name = categories[each_name]
				new_value = []
				for each_value in each_name:
					pseudo_value = prefix.join(each_value.brief.split("$command-prefix$"))
					new_value.append(pseudo_value)
				new_value = "\n".join(new_value)
				return help_embed.add_field(name=new_name + " Commands:", value=new_value, inline=False)
			else:
				return 
		#Help Message Creator
		categories = {"Member":member_commands, "Admin":admin_commands, "Owner":owner_commands}
		index = 0
		for recipient in recipients:
			#Checks if the receiver is an owner or an admin
			if recipient_type[index] == "U":
				owner_access = int(recipient.id) == int(config('DISCORD_OWNER_ID'))
			else:
				owner_access = False

			#Header of the Help Embed
			help_embed = Embed(colour=discord.Colour.blue(), title="BSCoE Class Support Bot Help", description="Gives user the allowed commands to do based on user's role.")

			#Adds help infos
			if options == "All":
				for each_name in categories:
					commands_interator(each_name, categories)
			elif options in categories:
				if categories[options] != owner_commands or (owner_access and categories[options] == owner_commands):
					commands_interator(options, categories)
				else:
					await ctx.channel.send("Recipient is not my owner!")
					continue
			elif options.lower() in all_commands_list_names:
				options = options.lower()
				if options in member_commands_names or options in admin_commands_names or (owner_access and options in owner_commands_names):
					if options in member_commands_names:
						new_value = member_commands[member_commands_names.index(options)]
					elif options in admin_commands_names:
						new_value = admin_commands[admin_commands_names.index(options)]
					elif owner_access and options in owner_commands_names:
						new_value = owner_commands[owner_commands_names.index(options)]
					pseudo_value = prefix.join(new_value.help.split("$command-prefix$"))
					help_embed.add_field(name=options.title() + " Command:", value=pseudo_value, inline=False)
				else:
					await ctx.channel.send("Recipient is not my owner!")
					continue
			else:
				raise CommandNotFound()

			help_embed.set_footer(text=f"send {prefix}help [category/command] for more information.")

			try:
				await recipient.send(embed=help_embed)
			except AttributeError:
				await ctx.channel.send("You are not allowed to send this to a bot!")
				print("A user tried sending a bot a help command!")

			index += 1



def setup(bot):
	bot.add_cog(Help(bot))