#######################匯入模組#######################
import requests
import os
import sys


#######################定義常數########################
API_KEY = "438939987c4337b28d9ce90965cc4c3c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "http://openweathermap.org/img/wn/"

#######################主程式########################
os.chdir(sys.path[0])
city = input("請輸入城市名稱: ")
send_url = f"{BASE_URL}appid={API_KEY}&q={city}&units={UNITS}&lang={LANG}"

print(f"發送的 URL: {send_url}")
response = requests.get(send_url)
info = response.json()

if not (info.get("cod") == "404"):
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]

    print(f"城市: {city}")
    print(f"描述: {weather_description}")
    print(f"溫度: {current_temperature}°C")

    # 下載天氣圖示
    icon_url = f"{ICON_BASE_URL}{icon_code}@4x.png"

    # 下載天氣圖標
    print(f"下載天氣圖標: {icon_url}")
    icon_response = requests.get(icon_url)
    # 將圖標保存到本地
    if icon_response.status_code == 200:
        # 打開文件以二進制寫入模式
        # 使用 with 語句確保文件在寫入完成後正確關閉
        # 將圖標內容寫入文件
        with open(f"weather.png", "wb") as icon_file:
            # 將圖標內容寫入文件
            icon_file.write(icon_response.content)
        print("天氣圖標已成功下載並保存為 weather.png")

else:
    # 如果找不到城市的天氣資訊，則輸出錯誤訊息
    print("找不到該城市的天氣資訊")
