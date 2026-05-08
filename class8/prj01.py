#######################匯入模組#######################
# 匯入 ttkbootstrap 模組，提供較美觀的 tkinter 元件
from ttkbootstrap import *

# 匯入 sys、os 模組，用來設定工作目錄
import sys
import os

# 匯入 PIL 模組，用來載入與顯示天氣圖標
from PIL import Image, ImageTk

# 匯入 requests 套件，用來發送天氣 API 請求
import requests

#######################設定工作目錄########################
# 將工作目錄切換到目前程式所在的資料夾，方便讀取相關檔案
os.chdir(sys.path[0])

#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"  # API URL
# API 固定用攝氏資料查詢，畫面要顯示華氏時再做換算
BASE_UNITS = "metric"
LANG = "zh_tw"  # 語言 (繁體中文)
ICON_BASE_URL = "https://openweathermap.org/img/wn/"  # 天氣圖標基礎 URL
ICON_FILE = "weather.png"  # 圖標存檔名稱


#######################定義函數########################
def format_temperature(temperature_celsius):
    # Checkbutton 勾選時顯示攝氏，取消勾選時顯示華氏
    if check_type.get():
        return f"溫度: {temperature_celsius}°C"

    temperature_fahrenheit = round(temperature_celsius * 9 / 5 + 32, 2)
    return f"溫度: {temperature_fahrenheit}°F"


def update_text_labels():
    # 還沒有查詢結果時，只更新目前單位對應的預設溫度文字
    if current_weather is None:
        temperature_label.config(text=f"溫度: ?°{'C' if check_type.get() else 'F'}")
        return

    temperature_label.config(
        text=format_temperature(current_weather["temperature_celsius"])
    )
    description_label.config(text=f"描述: {current_weather['description']}")


def clear_icon():
    # 清空圖片時，要把圖片與保留參照一起重設
    icon_label.config(image="", text="天氣圖標")
    icon_label.image = None


def download_icon(icon_code):
    # 根據圖標代碼組合下載網址
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"

    try:
        icon_response = requests.get(icon_url)
    except:
        return False

    # 若下載成功，就照 adv-03/prj-04-get_icon.py 的方式把圖標寫成 png 檔
    if icon_response.status_code == 200:
        with open(ICON_FILE, "wb") as icon_file:
            icon_file.write(icon_response.content)
        return True

    return False


def show_icon():
    # Image.open() 與 ImageTk.PhotoImage() 的流程可參考 adv-02/prj-01-loadmage_2.py
    image = Image.open(ICON_FILE)
    tk_image = ImageTk.PhotoImage(image)

    # Label 顯示圖片與保留圖片參照的做法可參考 adv-04/prj-02-label_image.py
    icon_label.config(image=tk_image, text="")
    icon_label.image = tk_image


def get_weather_data(city_name):
    # 組合查詢天氣資料的 API URL
    send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={BASE_UNITS}&lang={LANG}"

    try:
        # requests.get() / response.json() 的流程可參考 adv-03/prj-03-get_request.py
        response = requests.get(send_url)
        info = response.json()
    except:
        return None

    # 若成功取得 weather 與 main 資訊，就整理成一份查詢結果回傳
    if "weather" in info and "main" in info:
        return {
            "temperature_celsius": round(info["main"]["temp"], 2),
            "description": info["weather"][0]["description"],
            "icon_code": info["weather"][0]["icon"],
        }

    return None


def get_weather_info():
    global current_weather

    # Entry 的讀值方式在 adv-03/prj-01-caculate.py 已經介紹過
    # strip() 可以去掉字串前後的空白，避免使用者不小心輸入空格導致查詢失敗
    city_name = city_name_entry.get().strip()

    # 若沒有輸入城市名稱，就直接顯示提醒文字
    if city_name == "":
        current_weather = None
        clear_icon()
        description_label.config(text="描述: 請先輸入城市名稱")
        update_text_labels()
        return

    weather_data = get_weather_data(city_name)

    # 若查不到城市資料，顯示錯誤訊息並清空舊圖示
    if weather_data is None:
        current_weather = None
        clear_icon()
        description_label.config(text="描述: 找不到該城市")
        update_text_labels()
        return

    # 保存最近一次成功查詢的結果，之後切換單位時就不用重新查 API
    current_weather = weather_data

    if download_icon(current_weather["icon_code"]):
        show_icon()
    else:
        clear_icon()

    update_text_labels()


#######################建立視窗########################
# 建立主視窗
window = Tk()

# 設定視窗標題
window.title("Weather App")

#######################設定字型########################
# 設定全域預設字型大小
font_size = 20

# 設定所有元件的預設字型
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
# 設定視窗主題樣式
style = Style(theme="minty")

# 設定按鈕與 Checkbutton 的字型樣式
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))

#######################建立變數########################
# BooleanVar / Checkbutton 的搭配方式在 adv-04/prj-01-check_button.py 已經介紹過
check_type = BooleanVar()

# 預設為勾選狀態，也就是使用攝氏單位
check_type.set(True)

#######################建立標籤########################
# 這裡用 Label 搭配 grid 排出查詢提示與結果區；基本寫法可參考 adv-02/prj-04-ttk_GUI.py
city_name_label = Label(window, text="請輸入想搜尋的城市:")
city_name_label.grid(row=0, column=0)

icon_label = Label(window, text="天氣圖標")
icon_label.grid(row=1, column=0)

temperature_label = Label(window, text="溫度: ?°C")
temperature_label.grid(row=1, column=1)

description_label = Label(window, text="描述: ?")
description_label.grid(row=1, column=2)

#######################建立輸入框########################
# Entry 的建立方式在 adv-03/prj-01-caculate.py 已經介紹過
city_name_entry = Entry(window)
city_name_entry.grid(row=0, column=1)

#######################建立按鈕########################
# Button 搭配 style 的寫法在 adv-02/prj-04-ttk_GUI.py 已經介紹過
search_button = Button(
    window, text="獲得天氣資訊", command=get_weather_info, style="my.TButton"
)
search_button.grid(row=0, column=2)

#######################建立Checkbutton########################
# Checkbutton 的寫法在 adv-04/prj-01-check_button.py 已經介紹過，這裡用來切換溫度單位
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=update_text_labels,
    style="my.TCheckbutton",
    text="溫度單位(°C/°F)",
)
check.grid(row=2, column=1, padx=10, pady=10)

#######################運行應用程式########################
# 開始執行主迴圈，等待使用者操作
window.mainloop()
