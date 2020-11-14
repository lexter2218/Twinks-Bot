#Member Commands
brief_announce = "$command-prefix$announce [--channel] [message]"
help_announce = "Sends announcements to given channels.\n\n$command-prefix$announce [channel-1] [channel-2(optional)] [message]\n\nNote:\n\t+ You could only send announcements to text channels, use message command to send a direct message to members.\n\t+ You could mention members on message part.\n\t+ Always put the desired text channel before starting the message or else it will be a part of your message.\n\t+ Channels should only be in two formats: \"--\" + \"channel-name\" or \"<#channel-id>\"\ni.e.\n\t$command-prefix$announce --general --general-2 <#952952033535491809> Help command, Hello There!\n\n\tThe message \"Help command, Hello There!\" will be sent to text channels general, general-2, and the text-channel that has the given id."

brief_message = "$command-prefix$message [mention member] [message]"
help_message = "Sends a direct message to given members.\n\n$command-prefix$announce [member-1] [member-2(optional)] [message]\n\nNote:\n\t+ You could only send direct messages to members of this guild, use announce command to send a message to text channels.\n\t+ Always put the desired members before starting the message or else it will be a part of your message.\n\t+ Members should only be in two formats: member mention or \"<@!member-id>\"\ni.e.\n\t$command-prefix$message @ProgrammingDoctor @ManOfSteel <@!952952033535491809> Help command, Hello There!\n\n\tThe message \"Help command, Hello There!\" will be sent to members ProgrammingDoctor, ManOfSteel, and the owner of given id."

brief_admincheck = "$command-prefix$admincheck"
help_admincheck = "Checks if you are an admin.\n\n$command-prefix$admincheck"

brief_help = "$command-prefix$help [all(default)/category/command] [members/text channels]"
help_help = "Sends a copy of list of commands that a user can use.\n\n$command-prefix$help [all(default)/category/command] [members/text channels]\n\nNote:\n\t+ $command-prefix$help is same as $command-prefix$help all . They both sends a copy of all the commands that can be used by the users.\n\t+ When member/text channels are not specified, the list of commands will be sent to the text channel where this command was invoked.\n\n+ Users can see the commands associated to a category by $command-prefix$help [category]\n\ti.e.$command-prefix$help Member\n\n\tThe list of commands associated with member will be shown.\n\t+ Users can see deeper description about a specific command when they use the command $command-prefix$help [command]\n\ti.e.$command-prefix$help help\n\n\tDeeper description of help command will be shown."

brief_info = "$command-prefix$info [members/text channels]"
help_info = "Sends the info of a user."



#Admin Commands
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
help_clear ="Clear previous messages.\n\n$command-prefix$clear [amount]\n\nNote:\n\t+ Amount should only be positive integers."




#Owner Commands
brief_close = "$command-prefix$close"
help_close = "closes the bot.\n\n$command-prefix$close"