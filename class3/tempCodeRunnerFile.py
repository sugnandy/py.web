#######################匯入模組#######################
# 匯入 tkinter 模型
from tkinter import *
from PIL import Image, ImageTk

# pip install pillow
import sys
import os

#######################設定工作目錄####################
# 設定工作目錄
os.chdir(sys.path[0])


#######################定義函數#######################
def move_circle(event):
    key = event.keysym
    print(key)
    if key == "Right":
        canva.move(circle, 10, 0)
    elif key == "Left":
        canva.move(circle, -10, 0)
    elif key == "Up":
        canva.move(circle, 0, -10)
    elif key == "Down":
        canva.move(circle, 0, 10)


#######################建立視窗########################
# 建立視窗
windows = Tk()

# 設定視窗名稱
windows.title("My first GUI")

#######################建立畫布########################
# 建立畫布,寬度為600,高度為600
canva = Canvas(windows, width=600, height=600, bg="white")

# 將畫布加入主視窗中
canva.pack()

#######################設定視窗圖片#######################
# 設定視窗圖片
windows.iconbitmap("crocodile2.ico")
#######################載入圖片#######################
image = Image.open("crocodile2.png")
img = ImageTk.PhotoImage(image)

#######################顯示圖片#######################
my_img = canva.create_image(300, 300, image=img)

#######################畫圖形#######################
# 在畫布上畫一個紅色的圓形,圓心座標為(250,150)
circle = canva.create_oval(250, 150, 300, 200, fill="green")

# 在畫布上畫一個矩形,起始座標為(220,400)
rect = canva.create_rectangle(220, 400, 340, 430, fill="purple")
# 在畫布上顯示一段文字,座標為(300,50),文字內容為"Hello World!",字體為Arial,大小為20
msg = canva.create_text(300, 100, text="Hello gay!", fill="blue", font=("Arial", 20))

#######################綁定按鍵事件#######################
canva.bind_all("<Key>", move_circle)


#######################運行應用程式########################
# 開始運行應用程式,讓視窗保持顯示
windows.mainloop()
