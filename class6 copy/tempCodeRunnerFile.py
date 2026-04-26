#######################匯入模組#######################
from ttkbootstrap import *
import os
import sys
from PIL import Image, ImageTk

#######################設定工作目錄####################
# 設定工作目錄
os.chdir(sys.path[0])

#######################建立視窗########################
# 建立視窗
window = Tk()

# 設定視窗名稱
window.title("Label Image")
