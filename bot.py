from dotenv import load_dotenv
from google import genai
import config

load_dotenv()


def main():
    client = genai.Client(api_key=config.gemini_api_key)
    model = "gemini-1.5-flash"

    chat = client.chats.create(model=model)
    while True:
        text = input()
        if text == "exit":
            break

        response = chat.send_message(text)
        print(response.text)


class DiscordManager(genai.Client):
    def __init__(self, api_key, model=None):
        super().__init__(api_key=api_key)
        self.model = model
        
        
        