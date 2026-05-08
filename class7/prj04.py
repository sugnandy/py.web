import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk

API_KEY = "438939987c4337b28d9ce90965cc4c3c"

current_temp_c = None  # 儲存攝氏溫度


def get_weather():
    global current_temp_c

    city = entry.get()
    if not city:
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    res = requests.get(url)

    if res.status_code != 200:
        temp_label.config(text="溫度: 查無資料")
        desc_label.config(text="描述: -")
        icon_label.config(image="", text="❌")
        return

    data = res.json()

    current_temp_c = data["main"]["temp"]  # 永遠存攝氏
    desc = data["weather"][0]["description"]
    icon_code = data["weather"][0]["icon"]

    desc_label.config(text=f"描述: {desc}")

    update_temperature()

    # 下載圖標
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    img_data = requests.get(icon_url).content

    img = Image.open(BytesIO(img_data))
    img = img.resize((80, 80))

    photo = ImageTk.PhotoImage(img)
    icon_label.config(img=photo, text="weather icon")
    icon_label.image = photo


def update_temperature():
    if current_temp_c is None:
        return

    if unit_var.get():  # True = 攝氏
        temp_label.config(text=f"溫度: {round(current_temp_c,1)}°C")
    else:  # 華氏
        f = current_temp_c * 9 / 5 + 32
        temp_label.config(text=f"溫度: {round(f,1)}°F")


# ===== UI =====
root = tk.Tk()
root.title("Weather App")
root.geometry("720x300")

# 上方
top_frame = tk.Frame(root)
top_frame.pack(pady=15)

tk.Label(top_frame, text="請輸入想搜尋的城市:", font=("Arial", 14)).pack(side="left")

entry = tk.Entry(top_frame, font=("Arial", 14), width=25)
entry.pack(side="left", padx=10)

tk.Button(
    top_frame,
    text="獲得天氣資訊",
    font=("Arial", 12),
    bg="#7DB7A3",
    fg="white",
    command=get_weather,
).pack(side="left")

# 中間
middle_frame = tk.Frame(root)
middle_frame.pack(pady=20)

icon_label = tk.Label(middle_frame, text="天氣圖標")
icon_label.grid(row=0, column=0, padx=90)

temp_label = tk.Label(middle_frame, text="溫度: ?°C", font=("Arial", 16))
temp_label.grid(row=0, column=1, padx=40)

desc_label = tk.Label(middle_frame, text="描述: ?", font=("Arial", 16))
desc_label.grid(row=0, column=2, padx=40)

# 下方（重點）
unit_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    root,
    text="溫度單位 (°C/°F)",
    variable=unit_var,
    command=update_temperature,  # ⭐ 切換時即時更新
    font=("Arial", 12),
).pack()

root.mainloop()
