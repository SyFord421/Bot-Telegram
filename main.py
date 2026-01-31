import telebot
from config import key

class BaseBot:
    def __init__(self, bot_token, id_chat):
        self.id_chat = id_chat
        self.bot = telebot.TeleBot(bot_token)
    def send_message(self, text):
        try:
            self.bot.send_message(self.id_chat, text)
            print("[√] Pesan Telah Terkirim ")
        except Exception as e:
            print(f"[!] Error {e}")

if __name__ == "__main__":
    BB = BaseBot(key['BOT_TELEGRAM'], key['ID_CHAT'])
    BB.send_message("Hello World")