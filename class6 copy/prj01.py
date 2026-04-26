#######################匯入模組#######################
from ttkbootstrap import *
import os
import sys

#######################設定工作目錄####################
# 設定工作目錄
os.chdir(sys.path[0])


#######################定義函數########################
def on_switch_change():
    check_label.config(text=str(check_type.get()))


#######################建立視窗########################
# 建立視窗
window = Tk()

# 設定視窗名稱
window.title("Checkbutton")


#######################設定字型########################
font_size = 20
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
style = Style(theme="superhero")

# 設定按鈕與Checkbutton的樣式
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))

#######################建立變數########################
# BooleanVar()：用於存儲布爾值（True或False）的變數類型，常用於Checkbutton等控件的狀態管理。
check_type = BooleanVar()
# 預設為勾選狀態
check_type.set(True)

#######################建立標籤########################
# 建立標籤,顯示目前 Checkbutton的狀態
check_label = Label(window, text="Ture")
check_label.grid(row=1, column=2, padx=10, pady=10)

#######################建立Checkbutton########################
# Checkbutton會和check_type變數綁定，當Checkbutton被勾選或取消勾選時，check_type的值會自動更新為True或False。
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)
check.grid(row=1, column=1, padx=10, pady=10)
# 開始主循環,等待用戶操作
window.mainloop()
