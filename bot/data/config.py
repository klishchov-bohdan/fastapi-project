import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
REDIS_SERVER_BOT: str = os.getenv("REDIS_SERVER_BOT")
REDIS_PORT_BOT: int = int(os.getenv("REDIS_PORT_BOT"))

admins_id = [
    656634975,
]

chat_id = -972603444

banned_messages = ['qwerty', 'sss']