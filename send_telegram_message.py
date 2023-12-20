from dotenv import load_dotenv
import os
import telegram
import asyncio

class TelegramMessenger:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('bot_token')
        self.chat_id = os.getenv('chat_id')
        self.bot = telegram.Bot(token=self.bot_token)
    
    async def send_message(self, mensagem):
        await self.bot.send_message(chat_id=self.chat_id, text=mensagem)
        
    async def send_message_with_retry(self, message):
        try:
            await self.send_message(message)
        except telegram.error.RetryAfter as e:
            seconds_to_wait = min(e.retry_after, 300) 
            print(f"Controle de inundação excedido. Tentando novamente em {seconds_to_wait} segundos.")
            await asyncio.sleep(seconds_to_wait)
            await self.send_message_with_retry(message)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
