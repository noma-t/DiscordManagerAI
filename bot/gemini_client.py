from google import genai
from google.genai.types import GenerateContentConfig
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(
        self,
        api_key: str,
        chat_config: GenerateContentConfig,
        model: str ="gemini-1.5-flash",
        debug: bool = False,
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.debug = debug
        self.current_chat = None
        self.chat_config = chat_config
        
        if self.debug:
            logger.setLevel(logging.DEBUG)
        
        self._log("GeminiClient Initialized")
            
    
    def create_chat(self):
        if self.current_chat is not None:
            raise Exception("Chat already exists.")
        
        self.current_chat = self.client.chats.create(model=self.model, config=self.chat_config)
        self._log("Chat created")
    
    def send_message(self, text: str):
        if self.current_chat is None:
            raise Exception("Chat not created.")
        
        return self.current_chat.send_message(text)
            
    
    def _log(self, message: str, level=logging.DEBUG):
        if self.debug:
            logger.log(level, f"[GEMINI CLIENT] {message}")
