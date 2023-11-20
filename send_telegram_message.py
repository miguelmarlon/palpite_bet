from dotenv import load_dotenv
import os
import telegram
import asyncio

async def send_message(mensagem):
    load_dotenv()
    bot_token = os.getenv('bot_token')
    chat_id = os.getenv('chat_id')
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=mensagem)
    
async def send_message_with_retry(message):
    try:
        await send_message(message)
    except telegram.error.RetryAfter as e:
        seconds_to_wait = min(e.retry_after, 300) 
        print(f"Controle de inundação excedido. Tentando novamente em {seconds_to_wait} segundos.")
        await asyncio.sleep(seconds_to_wait)
        await send_message_with_retry(message)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
