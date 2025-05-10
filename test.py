# コマンドラインで仮想的に実行
from bot.bot import DiscordManager
import config


def main():
    client = DiscordManager(api_key=config.gemini_api_key, model="gemini-1.5-flash")
    
    client.create_chat()
    client.start_chat()
    
    
