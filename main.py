import telebot.async_telebot
from config import key
import aiohttp
import asyncio
import pprint as p
import json

class BaseBot:
    """inisiasi class dasar"""
    def __init__(self):
        self.id_chat = key['ID_CHAT']
        self.bot = telebot.async_telebot.AsyncTeleBot(key['BOT_TELEGRAM'])
        
    async def send_message(self, text:str):
        """fungsi untuk mengirimkan pesan dengan library telebot dan error handling"""
        try:
            await self.bot.send_message(self.id_chat, text)
            print("[√] Pesan Telah Terkirim ")
        except Exception as e:
            print(f"[!] Error {e}")
            
class Weather_Bot(BaseBot):
    def __init__(self, regional_code: str, city_name: str):
        super().__init__()
        self.regional_code = regional_code
        self.city_name = city_name
        
        
    def save_to_json(self, data):
        with open("databmkg.json", 'w') as f:
            json.dump(data, f, indent=2)
        
    async def get_weather_info(self) -> tuple | None:
        """"Mengambil data cuaca dari API.""" 
        try:
            url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={self.regional_code}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json()
            return response
        except Exception:
            return None
            
    async def weather_data_parser(self, raw_data: dict) -> dict | None:
        """fungsi khusus untuk memproses data dari api bmkg agar menjadi dictionary yang lebih sederhana"""
        try:
            data_list = raw_data.get('data', [{}])[0]
            locate = data_list.get('lokasi', {})
            weather_nest = data_list.get('cuaca', [[]])
            weather_today = weather_nest[0] if len(weather_nest) > 0 else []
            now = weather_today[0] if len(weather_today) > 0 else {}
            later = weather_today[1] if len(weather_today) > 1 else {}
            return {
                'city': locate.get('kotkab', 'unknown'),
                'village': locate.get('desa', 'unknown'),
                'now': {
                    'temp': now.get('t', '-'),
                    'desc': now.get('weather_desc', '-')
                },
                'later': {
                    'temp': later.get('t', '-'),
                    'desc': later.get('weather_desc', '-')
                }
            }
        except Exception as e:
            print(f"Debug Error: {e}") # Biar tau errornya apa
            return None



    async def full_report(self):
        try:
            desc, temp = await self.get_weather_info()
            if temp is None:
                return
            if temp <= 22:
                message = "🥶 Dingin banget, pake hoodie ya!"
            elif temp >= 29:
                message = "🌤 Panas banget, jangan dehidrasi!"
            else:
                message = "Suhu yang pas untuk jalan-jalan 🍃"
            report = (f"\n☁ Local Forecast ☁\n"
                      f"📍 Lokasi: {self.city_name}\n"
                      f"☁ Cuaca: {desc}\n"
                      f"🌡 Suhu: {temp}°C\n"
                      f"{message}")
            
            await self.send_message(report)
            await asyncio.sleep(0.1)
        except Exception as e:
            await self.send_message(f"Error Report:\n{e}")
    

if __name__ == "__main__":
    bot = Weather_Bot(key['regional_code'], "Padaasih")
    asyncio.run(bot.full_report())
    