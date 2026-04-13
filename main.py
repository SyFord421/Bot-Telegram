import telebot.async_telebot
from config import key
import aiohttp
import asyncio

class BaseBot:
    """inisiasi class utama"""
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
        
        
    async def get_weather_info(self) -> tuple[str, float] | None:
        """"Mengambil data cuaca dari API dan mengirimkannya ke Telegram.""" 
        try:
            url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={self.regional_code}"
            #&lang=id agar data yang di kirim bebahasa indonnesia
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
            desc = data['data'][0]['cuaca'][0][0]['weather_desc']
            temp = data['data'][0]['cuaca'][0][0]['t']
            return desc, temp 
        except Exception:
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