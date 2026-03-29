#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os


#######################定義函數########################
def test():
    print("test")


#######################建立視窗########################
# 建立視窗
window = Tk()

# 設定視窗名稱
window.title("My GUI")


#######################設定自型########################
font_size = 20
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
style = Style(theme="cyborg")
style.configure("my.TButton", font=("Helvetica", font_size))

#######################建立標籤########################
label = Label(window, text="Hello World!")
label.grid(row=0, column=0, sticky="E")

#######################建立按鈕########################
button = Button(window, text="瀏覽", command=test, style="my.TButton")
button.grid(row=0, column=1, sticky="W")
button2 = Button(window, text="顯示", command=test, style="my.TButton")
button2.grid(row=1, column=0, columnspan=2, sticky="EW")

#######################運行應用程式########################
# 開始運行應用程式,讓視窗保持顯示
window.mainloop()
