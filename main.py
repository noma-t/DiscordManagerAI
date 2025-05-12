import config
from bot.gemini_client import GeminiClient
from bot.discord_bot import DiscordClient, setup_commands
import discord

intents = discord.Intents.default()
intents.message_content = True
discord_client = DiscordClient(intents=intents)
setup_commands(discord_client)
gemini_client = GeminiClient(config.GEMINI_API_KEY, config.GEMINI_CHAT_CONFIG)

discord_client.run(config.DISCORD_TOKEN)
