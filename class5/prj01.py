#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os
from tkinter import filedialog
from PIL import Image, ImageTk


#######################定義函數########################
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    label.config(text=file_path)


def show_image():
    global file_path
    image = Image.open(file_path)
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.image = photo  # Keep a reference to avoid garbage collection


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
label = Label(window, text="選擇檔案:")
label.grid(row=0, column=0, sticky="E")

label = Label(window, text="無")
label.grid(row=0, column=1, sticky="E")


#######################建立按鈕########################
button = Button(window, text="瀏覽", command=open_file, style="my.TButton")
button.grid(row=0, column=2, sticky="W")

button2 = Button(window, text="顯示", command=show_image, style="my.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")

canvas = Canvas(window, width=600, height=600)
canvas.grid(row=2, column=0, columnspan=3)

#######################運行應用程式########################
# 開始運行應用程式,讓視窗保持顯示
window.mainloop()
