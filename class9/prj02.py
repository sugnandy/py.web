#######################模組#######################
import asyncio
import discord
import os  # 用來讀取環境變數
from dotenv import load_dotenv

#######################初始化#####################
load_dotenv()  # 讀取.env檔案

# 建立Discord的bot
# 注意：在 class8/prj01.py 中，我們是使用 requests 模組來發送 API 請求，但在這裡我們需要使用 discord.py 來建立一個 Discord Bot。
# 因此，我們需要先安裝 discord.py 模組（如果還沒安裝的話），然後使用它來建立一個 Bot 實例。

asyncio.set_event_loop(asyncio.new_event_loop())

intents = discord.Intents.default()
intents.message_content = True  # 允許接收訊息

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


#######################事件#######################

#######################指令#######################


#######################啟動#######################
