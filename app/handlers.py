import discord
import logging
from config import Config
from command_handler import CommandHandler

# Pass the `cmds` argument when creating the `CommandHandler` instance
def create_command_handler(cmds):
    return CommandHandler(cmds)

async def handle_help(message, args, help_embeds):
    for embed in help_embeds:
        await message.channel.send(embed=embed)

async def handle_hi(message, args):
    embed = discord.Embed(description="Hello! I'm Archon the Minecraft RCON bot!")
    await message.channel.send(embed=embed)

async def handle_admin(message, args, auth_level, command_handler):
    if auth_level >= 4:
        await command_handler.send_rcon(args, '', message)
    else:
        await message.channel.send(f'Sorry, you need the {Config.ADMIN_ROLE} role to use that command.')

async def handle_rcon_command(message, cmd, args, auth_level, required_level, command_handler):
    if auth_level >= required_level:
        await command_handler.send_rcon(cmd, args, message)
    else:
        role_name = Config.USER_ROLE if required_level == 1 else Config.MOD_ROLE if required_level == 2 else Config.ADMIN_ROLE
        await message.channel.send(f'Sorry, you need the {role_name} role to use that command.')
