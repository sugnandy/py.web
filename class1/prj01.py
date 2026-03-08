#######################匯入模組#######################
# 匯入 tkinter 模型
from tkinter import *


#######################定義函數########################
def hi_fun():
    print("hi singular")


#######################建立視窗########################
# 建立視窗
windows = Tk()
# 設定視窗名稱
windows.title("My first GUI")

#######################建立按鈕########################
# 建立按鈕,當被按下時會呼叫 hi_fun 函數
btn1 = Button(windows, text="Click Me!", command=hi_fun)

# 將按鈕加入主視窗中
btn1.pack()

#######################建立標籤########################
# 建立標籤,顯示 "Hi Singular",
# Label參數
display = Label(windows, text="Hi Singular", fg="red", bg="black")

# 將標籤加入主視窗中
display.pack()

#######################運行應用程式########################
# 開始運行應用程式,讓視窗保持顯示
windows.mainloop()
