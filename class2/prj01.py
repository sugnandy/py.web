#######################匯入模組#######################
# 匯入 tkinter 模型
from tkinter import *


#######################定義函數########################

is_green = False


def hi_toggle():
    global is_green
    is_green = not is_green
    if is_green:
        print("Click Me!")
        display.config(text="Green", fg="black", bg="green")
        try:
            btn_toggle.config(text="click me!")
        except NameError:
            pass
    else:
        print("Click Me!")
        display.config(text="Red", fg="black", bg="red")
        try:
            btn_toggle.config(text="click me!")
        except NameError:
            pass


#######################建立視窗########################
# 建立視窗
windows = Tk()
# 設定視窗名稱
windows.title("My first GUI")

#######################建立按鈕########################
# 建立按鈕,當被按下時切換顏色
btn_toggle = Button(windows, text="click me!", command=hi_toggle)
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
