from google import genai


class DiscordManager(genai.Client):
    def __init__(self, api_key: str, model: str, debug=False):
        super().__init__(api_key=api_key)
        self.model: str = model
        self.current_chat = None
        self.debug = debug

    def create_chat(self):
        if self.current_chat is not None:
            raise ValueError("A chat session is already active.")
        
        self.current_chat = self.chats.create(model=self.model)
    
    def start_chat(self):
        if self.current_chat is None:
            raise ValueError("No chat session found. Create a chat session first.")

        while True:
            try:
                text = input("You: ")
            except KeyboardInterrupt:
                print("\nExiting chat.")
                break

            response = self.current_chat.send_message(text)
            print(f"Bot: {response.text}")
    
    def debug_message(self, text):
        if self.debug:
            print(f"[DEBUG]: {text}")