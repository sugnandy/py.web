#######################匯入模組#######################
import requests  # 用來向天氣網站送出請求，並接住回傳的資料


#######################定義類別#######################
# 這份類別可以看成是把第一次實作天氣功能時的主程式流程拆開整理。
# 原本查天氣、取圖示代碼、組圖示網址、下載圖片都寫在同一段；
# 現在改成一個方法只負責一件事，比較容易看出每個功能各自在做什麼。
class WeatherAPI:
    """把 OpenWeather 的查詢流程整理成可重複使用的工具類別。"""

    def __init__(self, api_key, lang="zh_tw"):
        # __init__() 專門負責準備共用設定。
        # 這樣就不用像早期把所有設定都直接寫在主程式裡那樣，
        # 每次查詢時都重新手動處理 API 金鑰、語言、單位和網址前半段。
        self.api_key = api_key  # api_key 是天氣網站辨認身分用的金鑰
        self.units = "metric"  # 這一版固定用攝氏資料查詢
        self.lang = lang  # lang 代表回傳的語言，這裡使用繁體中文
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"  # 目前天氣 API 的網址前半段
        self.icon_base_url = (
            "https://openweathermap.org/img/wn/"  # 天氣圖示網址的前半段
        )

    def get_current_weather(self, city_name):
        # get_current_weather() 只負責「向天氣網站拿原始資料」。
        # 這一步對應到第一次實作時，先組查詢網址、再 requests.get() 拿資料的部分。
        send_url = f"{self.base_url}appid={self.api_key}&q={city_name}&units={self.units}&lang={self.lang}"

        response = requests.get(send_url)
        return response.json()  # json() 會把網站回傳的 JSON 資料轉成 Python 字典

    def get_icon_url(self, icon_code):
        # get_icon_url() 只負責把 icon_code 組成圖片網址。
        # 這樣如果主程式只想顯示圖片網址，就不用順便做下載圖片的工作。
        return f"{self.icon_base_url}{icon_code}@2x.png"
