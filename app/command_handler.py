import discord
from rcon import Rcon
from config import Config
import logging

logging.basicConfig(level=logging.INFO)

class CommandHandler:
    def __init__(self, cmds):
        self.cmds = cmds

    def create_help_embeds(self):
        embeds = []
        embed = discord.Embed(description="A bot to interact with your Minecraft server - from Discord!")

        def add_field(embed, name, value):
            embed.add_field(name=name, value=value, inline=False)

        self._add_role_commands(embed, 'user_commands', Config.USER_ROLE)
        self._add_role_commands(embed, 'mod_commands', Config.MOD_ROLE)
        self._add_role_commands(embed, 'admin_commands', Config.ADMIN_ROLE)
        embed.add_field(name='admin', value='Runs a custom command', inline=False)

        embeds.append(embed)
        return embeds

    def _add_role_commands(self, embed, command_type, role):
        embed.add_field(name='\u200b', value=f'-------------------------{role}-------------------------')
        for command, description in self.cmds[command_type].items():
            embed.add_field(name=command, value=description)

    async def send_rcon(self, cmd, args, message):
        try:
            with Rcon(Config.IP, Config.PASS, Config.PORT) as mcr:
                resp = mcr.command(f"{cmd} {args}" if args else cmd)
        except Exception as e:
            resp = 'Connection from the bot to the server failed.'
            logging.error(f"RCON connection error: {e}")

        logging.info(f"[{message.author}]: {cmd} {args}")
        if resp:
            await message.channel.send(resp)
            logging.info(resp)
