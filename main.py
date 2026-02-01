import telebot
from config import key
import requests


class BaseBot:
    def __init__(self, bot_api, id_chat, weather_api, city):
        self.id_chat = bot_api
        self.bot = telebot.TeleBot(bot_api)
        self.weather_token = weather_token
        self.city = city

    def send_message(self, text):
        try:
            self.bot.send_message(self.id_chat, text)
            print("[√] Pesan Telah Terkirim ")
        except Exception as e:
            print(f"[!] Error {e}")

    def get_weather_info(self):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.weather_token}&units=metric&lang=id"
            weatherdata = requests.get(url).json()
            if weatherdata.get("cod") != 200:
                print("[!] Error Kota Tidak ditemukan")
            weather = weatherdata['weather'][0]['main']
            desc = weatherdata['weather'][0]['description']
            temp = weatherdata['main']['temp']
            self.send_message(f"---- Forecast Hari ini---\n 📍 Kota : {self.city}\n ☁ Cuaca : {weather}\n 🌡 Suhu : {temp}°C\n 📄 deskripsi : {desc}"
        except Exception as e:
            print("[!] Error Tidak dapat mendapatakan data")

if __name__ == "__main__":
    BB = BaseBot(key['BOT_TELEGRAM'], key['ID_CHAT'], key['API_CUACA'], key['KOTA'])
    BB.get_weather_info()
