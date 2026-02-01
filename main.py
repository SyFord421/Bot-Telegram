import telebot
from config import key
import requests

class BaseBot:
    """inisiasi class utama"""
    def __init__(self, bot_api, id_chat, weather_api, city):
        self.id_chat = id_chat
        self.bot = telebot.TeleBot(bot_api)
        self.weather_token = weather_api
        self.city = city

    def send_message(self, text):
        """fungsi untuk mengirimkan pesan dengan library telebot dan error handling"""
        try:
            self.bot.send_message(self.id_chat, text)
            print("[√] Pesan Telah Terkirim ")
        except Exception as e:
            print(f"[!] Error {e}")

    def get_weather_info(self):
        """"Mengambil data cuaca dari OpenWeatherMap API dan mengirimkannya ke Telegram.""" 
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.weather_token}&units=metric&lang=id"
            #&lang=id agar data yang di kirim bebahasa indonnesia
            weatherdata = requests.get(url).json()#Mengubah response mentah dari API menjadi dictionary Python agar mudah diolah.
            if weatherdata.get("cod") != 200:
                print(f"[!] Error: {weatherdata.get('message', 'Kota tidak ditemukan')}")
                return
            weather = weatherdata['weather'][0]['main']
            desc = weatherdata['weather'][0]['description']
            temp = weatherdata['main']['temp']
            msg = (f"---- Forecast Hari ini---\n 📍 Kota : {self.city}\n ☁ Cuaca : {weather}\n 🌡 Suhu : {temp}°C\n 📄 deskripsi : {desc}")
            self.send_message(msg)
        except Exception as e:
            print(f"[!] Error Tidak dapat mendapatakan data {e}")

if __name__ == "__main__":
    BB = BaseBot(key['BOT_TELEGRAM'], key['ID_CHAT'], key['API_CUACA'], key['KOTA'])
    BB.get_weather_info()
