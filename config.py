from dotenv import load_dotenv
import os
from data import prompts
from google.genai.types import GenerateContentConfig

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_CHAT_CONFIG = GenerateContentConfig(
    system_instruction=prompts.INSTRUCTION_PROMPT
)

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

WELCOME_MESSAGE = """\
{}
作成したいカテゴリ・チャンネルについて教えてください。\
"""

CONFIRMATION_MESSAGE = """\
以下の設定でよろしいでしょうか？

「OK」を選択すると設定が適用されます。
再調整が必要な場合は、メッセージを送信してください。\
"""

TIMEOUT_MESSAGE = """\
長時間の応答がなかったため、セッションを終了します。
新しいセッションを開始するには `/dmai start` を実行してください。\
"""