#######################匯入模組#######################
import requests


#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"

#######################主程式########################
city = input("請輸入城市名稱: ")
send_url = f"{BASE_URL}appid={API_KEY}&q={city}&units={UNITS}&lang={LANG}"

print(f"發送的 URL: {send_url}")
response = requests.get(send_url)
info = response.json()
