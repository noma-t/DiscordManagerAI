import config
from bot.bot import DiscordManager
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)


cmdgroup_manager = app_commands