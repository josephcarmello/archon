import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('DISCORD_TOKEN')
    USER_ROLE = os.getenv('DISCORD_USER_ROLE')
    MOD_ROLE = os.getenv('DISCORD_MOD_ROLE')
    ADMIN_ROLE = os.getenv('DISCORD_ADMIN_ROLE')
    IP = os.getenv('MINECRAFT_IP')
    PASS = os.getenv('MINECRAFT_PASS')
    PORT = int(os.getenv('RCON_PORT', 25575))
    BOT_LEVEL = int(os.getenv('BOT_LEVEL', 1))
    ADMIN_CHANNEL_ID = int(os.getenv('DISCORD_ADMIN_CHANNEL_ID'))
