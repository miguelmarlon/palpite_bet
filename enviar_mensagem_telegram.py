import asyncio
from dotenv import load_dotenv
import os
import telegram


async def enviar_mensagem(mensagem):
    load_dotenv()
    bot_token = os.getenv('bot_token')
    chat_id = os.getenv('chat_id')
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=mensagem)
