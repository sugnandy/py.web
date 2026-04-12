from ttkbootstrap import *
import sys
import os


#######################定義函數########################
def show_result():
    entry_text = entry.get()
    try:
        result = eval(entry_text)
    except:
        result = "計算錯誤"
    label.config(text=result)


#######################設定工作目錄########################
os.chdir(sys.path[0])

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
label = Label(window, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

#######################建立按鈕########################
button = Button(window, text="顯示計算結果", command=show_result, style="my.TButton")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

#######################輸入欄位########################
entry = Entry(window, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()
