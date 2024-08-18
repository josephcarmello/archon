import discord
import json
from config import Config
from command_dispatcher import dispatch_command
from handlers import create_command_handler

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

with open('commands.json') as cmd_file:
    cmds = json.load(cmd_file)

command_handler = create_command_handler(cmds)
help_embeds = command_handler.create_help_embeds()

@client.event
async def on_message(message):
    if message.channel.id != Config.ADMIN_CHANNEL_ID or not message.content.startswith('>') or message.author == client.user:
        return

    try:
        cmd, args = message.content[1:].split(None, 1)
    except ValueError:
        cmd, args = message.content[1:], ''

    auth_level = sum(
        1 if role.name == Config.USER_ROLE else
        2 if role.name == Config.MOD_ROLE else
        4 if role.name == Config.ADMIN_ROLE else 0
        for role in message.author.roles
    )

    await dispatch_command(cmd, message, args, auth_level, cmds, help_embeds, command_handler)

client.run(Config.TOKEN)
