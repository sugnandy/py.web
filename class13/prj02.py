import requests  # 用來向天氣網站送出請求，並接住回傳的資料

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
UNITS = "metric"  # 這一版固定用攝氏資料查詢
LANG = "zh_tw"  # lang 代表回傳的語言，這裡使用繁體中文

city_name = "Taipei"

send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的 URL: {send_url}")  # 印出完整的查詢網址，方便除錯

response = requests.get(send_url)
response.raise_for_status()  # raise_for_status() 會檢查 HTTP 狀態碼，
info = response.json()  # 如果是 200 就會回傳 JSON 資料

if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]

        print(dt_txt, temp, weather_description)
else:
    print("找不到該城市")
