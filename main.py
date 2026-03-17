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
            weatherdata = requests.get(url).json()
            if weatherdata.get("cod") != 200:
                print(f"[!] Error: {weatherdata.get('message', 'Kota tidak ditemukan')}")
                return
            weather = weatherdata['weather'][0]['main']
            desc = weatherdata['weather'][0]['description']
            temp = weatherdata['main']['temp']
            return weather, desc, temp
        except Exception:
            return None, None, None

    def full_report(self):
        try:
            weather, desc, temp = self.get_weather_info()
            if temp <= 22:
                message = "🥶 Dingin banget jangan lupa pake hoodie yah biar nggak kedinginan "
            elif temp >= 29:
                message = "🌤 cuaca-nya panas banget hari ini jangan lupa banyakin minum air putih biar nggak dehidrasi"
            else:
                message = "Suhu yang pas untuk jalan-jalan 🍃"
            self.send_message(f"\n ☁ Local Forecast ☁ \n📍 Kota: {self.city}\n ☁ Cuaca  : {desc.capitalize()}\n🌡 Suhu : {temp}°C\n {message}")
        except Exception as e:
            self.send_message(f"Error:\n{e}")

if __name__ == "__main__":
    BB = BaseBot(key['BOT_TELEGRAM'], key['ID_CHAT'], key['API_CUACA'], key['KOTA'])
    BB.full_report()