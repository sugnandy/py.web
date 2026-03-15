#######################匯入模組#######################
# 匯入 tkinter 模型
from tkinter import *
import random


#######################定義函數########################
def hi_fun():

    fg_COLORS = "#" + "".join([random.choice("0123456789ABCDEF") for i in range(6)])
    """
    fg_COLORS = "#"
    for i in range(6):
        fg_COLORS += random.choice("0123456789ABCDEF")
    """
    bg_COLORS = "#" + "".join([random.choice("0123456789ABCDEF") for i in range(6)])
    display.config(text="Hi Singular", fg=fg_COLORS, bg=bg_COLORS)


#######################建立視窗########################
# 建立視窗
windows = Tk()

# 設定視窗名稱
windows.title("My first GUI")

# 設定視窗的預設字型
windows.option_add("*Font", "新細明體 100")

#######################建立按鈕########################
# 建立按鈕,當被按下時切換顏色
btn_toggle = Button(windows, text="show screen", command=hi_fun)
btn_toggle.pack()

#######################建立標籤########################
# 建立標籤,顯示 "Hi Singular",
# Label參數
display = Label(windows, text="")

# 將標籤加入主視窗中
display.pack()

#######################運行應用程式########################
# 開始運行應用程式,讓視窗保持顯示
windows.mainloop()
