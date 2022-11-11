import os
import asyncio
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands
from discord import Embed, Client, Guild
from discord.ext.commands import Bot, CommandNotFound

from functions import channel_check, member_check, fetch_prefix

brief_help = "$command-prefix$help [all(default)/category/command] [members/text channels]"
help_help = "Sends a copy of list of commands that a user can use.\n\n$command-prefix$help [all(default)/category/command] [members/text channels]\n\nNote:\n\t+ $command-prefix$help is same as $command-prefix$help all . They both sends a copy of all the commands that can be used by the users.\n\t+ When member/text channels are not specified, the list of commands will be sent to the text channel where this command was invoked.\n\n+ Users can see the commands associated to a category by $command-prefix$help [category]\n\ti.e.$command-prefix$help Member\n\n\tThe list of commands associated with member will be shown.\n\t+ Users can see deeper description about a specific command when they use the command $command-prefix$help [command]\n\ti.e.$command-prefix$help help\n\n\tDeeper description of help command will be shown."

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
			pseudo_recipients = ["--" + str(ctx.message.channel), ]

		#fetches the commmand-prefix
		prefix = fetch_prefix(ctx.guild.id)

		#Recipient Identifier
		known_recipients, unknown_recipient = [], []
		for recipient in pseudo_recipients:
			#If word has "--" prefix or has "<@!" as prefix and ">" as suffix, this means that it might be a channel or member
			if recipient[:2] == "--" or ((recipient[:3] == "<@!" or recipient[:2] == "<#") and recipient[-1] == ">"):
				#Checks if recipient is member or channel of guild
				recipient_is_member = member_check(member_id=recipient, bot=self.bot)
				recipient_is_channel = channel_check(ctx.guild, channel_name_id=recipient)
				if recipient_is_member:
					known_recipients.append((recipient_is_member, "U"))
				elif recipient_is_channel:
					known_recipients.append((recipient_is_channel, "C"))
				else:
					unknown_recipient.append(recipient)
			else:
				unknown_recipient.append(recipient)

		#Sends all the unknown recipients
		if len(unknown_recipient) != 0:
			unknown_recipient = ",\n\t".join(unknown_recipient)
			await ctx.channel.send(f"Unknown Recipients:\n\t{unknown_recipient}\n\nMake sure that your recipients are members or channels of this guild/server.")

		#loads all commands
		cmd_set = self.bot.commands.copy()
		cmd_dict = {}
		cmd_names = []
		for cmd in cmd_set:
			if not cmd.hidden:
				cmd_names.append(cmd.name)
				if cmd.cog_name in ("Member", "Help"):
					cmd_dict.setdefault("Member", []).append(cmd)
				elif cmd.cog_name in ("Admin", "Owner"):
					cmd_dict.setdefault(f"{cmd.cog_name}", []).append(cmd)
				elif cmd.cog_name in ("GameConfig", "ShopConfig"):
					cmd_dict.setdefault("Game", []).append(cmd)

		category_list = [each_category for each_category in cmd_dict]

		def cmd_field_iter(category_name, listed_cmd):
			if category_name == "Owner" and not owner_access:
				return

			listed_brief = [prefix.join(each_cmd.brief.split("$command-prefix$")) for each_cmd in listed_cmd]
			new_value = "\n\t".join(listed_brief)
			return help_embed.add_field(name=category_name + " Commands:", value=new_value, inline=False)
 

		#Help Message Creator
		for each_recipient in known_recipients:
			recipient = each_recipient[0]
			rec_type = each_recipient[1]

			#Checks if the receiver is an owner or an admin
			if rec_type == "U":
				owner_access = int(recipient.id) == int(config('DISCORD_OWNER_ID'))
			else:
				owner_access = False

			#Header of the Help Embed
			help_embed = Embed(colour=discord.Colour.blue(), title="Twinks Bot Help", description="Gives user the allowed commands to do based on user's role.")

			#Adds help infos
			if options == "All":
				for each_cog in cmd_dict:
					cmd_field_iter(each_cog, cmd_dict[each_cog])
			elif options in category_list:
				cmd_field_iter(options, cmd_dict[options])
			elif options.lower() in cmd_names:
				options = options.lower()
				for each_cog in cmd_dict:
					this_cog_cmds = [each_cmd.name for each_cmd in cmd_dict[each_cog]]
					if options in this_cog_cmds:
						if each_cog == "Owner" and not owner_access:
							await ctx.channel.send("Recipient is not my owner!")
							break
						else:
							get_cmd = cmd_dict[each_cog][this_cog_cmds.index(options)]
							new_value = prefix.join(get_cmd.help.split("$command-prefix$"))
							help_embed.add_field(name=options.title() + " Command:", value=new_value, inline=False)
			else:
				raise CommandNotFound()

			help_embed.set_footer(text=f"send {prefix}help [category/command] for more information.")

			try:
				await recipient.send(embed=help_embed)
			except AttributeError:
				await ctx.channel.send("You are not allowed to send this to a bot!")
				print("A user tried sending a bot a help command!")


def setup(bot):
	bot.add_cog(Help(bot))