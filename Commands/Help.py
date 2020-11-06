import os
import json
import asyncio
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands
from discord import Embed, Client, Guild
from discord.ext.commands import Bot, CommandNotFound

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, options="all", *, send_to=None):
		#Collecting all recipients
		if send_to != None:
			#Clearing unnecessary
			pseudo_recipients = send_to.split()
			while "" in pseudo_recipients:
				pseudo_recipients.remove("")
			if len(pseudo_recipients) == 0:
				await ctx.channel.send("Please complete the argument!")
				print("Argument not complete!")
				return
		else:
			pseudo_recipients = ["<@!" + str(ctx.message.author.id) + ">"]

		#Recipient Identifier
		recipients = []
		recipient_type = []
		for recipient in pseudo_recipients:
			#Given is id (could be user's id or channel's id)
			if recipient[0:3] == "<@!" and recipient[-1] == ">":
				if self.bot.get_user(int(recipient[3:-1])):
					recipient = self.bot.get_user(int(recipient[3:-1]))
					recipients.append(recipient.id)
					recipient_type.append("U")
				elif self.bot.get_channel(int(recipient[3:-1])):
					recipient = self.bot.get_channel(int(recipient[3:-1]))
					recipients.append(recipient.id)
					recipient_type.append("C")
				else:
					await ctx.channel.send(f"{recipient} Id not found. Given Id is not a member or channel in this server.")
					continue
			#Given is channel name ("--" + channel name)
			elif recipient[:2] == "--" and get(self.bot.get_all_channels(), name=recipient[2:]):
				recipient = get(self.bot.get_all_channels(), name=recipient[2:])
				recipients.append(recipient.id)
				recipient_type.append("C")
			#Given is user's name (username#discriminator)
			elif get(self.bot.get_all_members(), name=recipient):
				recipient = get(self.bot.get_all_members(), name=recipient)
				recipients.append(recipient.id)
				recipient_type.append("U")
			else:
				await ctx.channel.send(f"{recipient} Id not found. Given Id is not a member or channel in this server.")
				continue

		#fetches the commmand-prefix
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)

		prefix = prefixes[str(ctx.guild.id)]

		#loads all commands
		with open("Commands/help_commands.json", "r") as f:
			all_commands_list = json.load(f)

		help_command_list = []
		for saved_commands in all_commands_list:
			processed_commands = all_commands_list[saved_commands]
			processed_commands = processed_commands[1]
			processed_commands = processed_commands.split("$command-prefix$")
			processed_commands = prefix.join(processed_commands)
			help_command_list.append(processed_commands)

		def command_info_fetcher(num_range):
			new_value = ""
			for saved_commands in help_command_list[num_range[0]:num_range[1]]:
				new_value += saved_commands + "\n"
			return new_value[:-1]

		def member_commands():
			new_value = command_info_fetcher((0,4))
			return help_embed.add_field(name="Member Commands:", value=new_value, inline=False)

		def admin_commands():
			new_value = command_info_fetcher((4,10))
			return help_embed.add_field(name="Admin Commands:", value=new_value, inline=False)

		def owner_commands():
			new_value = command_info_fetcher((10,11))
			return help_embed.add_field(name="Owner Commands:", value=new_value, inline=False)

		#loading all categories
		help_functions_list = {"MEMBER":member_commands, "MEMBERCOMMANDS":member_commands,
								"ADMIN":admin_commands, "ADMINCOMMANDS":admin_commands,
								"OWNER":owner_commands, "OWNERCOMMANDS":owner_commands}

		#Help Message Creator
		index = 0
		for recipient in recipients:
			#Checks if the receiver is an owner or not
			if recipient_type[index] == "U":
				owner_access = int(recipient) == int(config('DISCORD_OWNER_ID'))
				#Converts the id to user's info
				recipient = self.bot.get_user(int(recipient))
			else:
				owner_access = False
				#Converts the id to user's info
				recipient = self.bot.get_channel(int(recipient))

			#Header of the Help Embed
			help_embed = Embed(colour=discord.Colour.blue(), title="Help Command", description="Gives user the alloweed commands to do based on user's role.")
			help_embed.set_author(name="BSCoE Class Support Bot Help")

			#Adds help infos
			if options == "all":
				member_commands()
				admin_commands()
				if owner_access:
					owner_commands()
			elif options.upper() in help_functions_list:
				caller = options.upper()
				if caller in ("OWNER", "OWNERCOMMANDS"):
					if owner_access:
						owner_commands()
					else:
						await ctx.message.author.send(f"{recipient} have no permission to see this {options} help category!")
						continue
			elif options.lower() in all_commands_list:
				caller = options.lower()
				new_value = all_commands_list[caller]
				if new_value == "close" and not owner_access:
					await ctx.message.author.send(f"{recipient} have no permission to see this {options} help category!")
					continue
				if len(new_value) == 2:
					first_value, second_value = new_value[0], new_value[1]
				elif len(new_value) == 3:
					first_value, second_value, third_value = new_value[0], new_value[1], new_value[2]
				second_value = second_value.split("$command-prefix$")
				second_value = prefix.join(second_value)
				new_value = first_value + "\n\n" + second_value + "\n\n" + third_value
				help_embed.add_field(name=caller.upper() + " Command:", value=new_value)
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