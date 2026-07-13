#######################模組#######################
# asyncio 是 Python 內建的非同步工具。
# 可以把它想成「任務小管家」：如果某件事需要等網路回應，
# 它可以先去安排別的事，不會讓整個程式傻傻卡住。

import asyncio
import discord  # pip install -U discord.py；這個套件負責和 Discord 溝通
import os  # 用來讀取環境變數
import requests  # 用來向天氣網站送出請求，並接住回傳的資料
from dotenv import load_dotenv  # pip install -U python-dotenv；把 .env 裡的設定讀進程式
from myfunction.myfunction import WeatherAPI, AIAssistant  # pip install -U requests；把 requests 包匯入程式


#######################初始化#######################
load_dotenv()  # 讀取 .env 檔，讓程式可以拿到 DC_BOT_TOKEN 這類設定資料

# event loop 可以想成「非同步任務的轉盤」：
# 哪個工作先做、哪個工作要等一下，會由這個轉盤幫忙安排。
# Python 3.10+ 在主程式裡不一定會先自動準備好這個轉盤，
# 所以我們自己先建立一個給 Discord 使用。
asyncio.set_event_loop(asyncio.new_event_loop())

# Intent 可以想成「先跟 Discord 勾選：我想收到哪些類型的通知」。
# 如果沒有先打開某個 Intent，Discord 就不會把那種資料送給機器人。
intents = discord.Intents.default()
intents.message_content = (
    True  # 允許機器人看到訊息真正的文字內容，這樣它才知道有人是不是輸入了 hello
)

bot = discord.Client(intents=intents)  # 建立機器人本體，並把 intents 交給它
tree = discord.app_commands.CommandTree(
    bot
)  # 建立 slash 指令管理器，專門管理像 /hello 這種指令

weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))  # 建立 WeatherAPI 實例
ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))  # 建立 OpenAI API 實例

CHANNEL_HISTORY_LIMIT = 15

OPENAI_MODEL = "gpt-5.5"
OPENAI_TEMPERATURE = 1

# 這裡的 build_weather_embed() 是把整理好的天氣摘要排成 Discord 卡片的函式，
# 可以把原始資料傳進來，並在回覆時整理出原始資料。

# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣自然、簡短、適合國小學生閱讀。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
每次回覆控制在500字以內，避免Discord訊息過長被截斷。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False, roles=False, users=True, replied_user=True
)

def build_weather_embed(weather_summary):
    """把整理好的天氣摘要排成 Discord 卡片。"""
    # weather_summary 已經是整理好的資料，
    # 所以這個函式只要專心處理卡片外觀，不用再拆 API 原始資料。
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的當前天氣",
        description=f"描述：{weather_summary['description']}",
        color=discord.Colour.from_str("#1E90FF"),
    )

    # get_icon_url() 會把圖示代碼組成圖片網址，再放到卡片右上角
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature_celsius']}°C",
        inline=False,  # inline=False 代表這筆資料單獨一行顯示
    )
    return embed


def build_forecast_embeds(forecast_summary):
    """把整理好的預報摘要排成 Discord 卡片。"""
    # weather_summary 已經是整理好的資料，
    # 所以這個函式只要專心處理卡片外觀，不用再拆 API 原始資料。
    embeds = []

    for forecast in forecast_summary:
        embed = discord.Embed(
            title=f"{forecast['city_name']} 的當前天氣 -{forecast['datetime']}",
            description=f"描述：{forecast['description']}",
            color=discord.Colour.from_str("#1E90FF"),
        )
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)

        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}°C",
            inline=False,  # inline=False 代表這筆資料單獨一行顯示
        )
        embeds.append(embed)

    return embeds


async def get_channel_history(channel, bot_user, limit=20, before=None):
    """取得頻道歷史訊息，預設最多 15 筆，可以指定 before 參數往前查更久的歷史。"""
    old_messages = []   
    history_messages = []
    # 這裡的 async for 是因為 channel.history() 回傳的是一個非同步的資料流（async iterator），
    # 需要用 async for 來逐筆讀取裡面的訊息。
    async for old_message in channel.history(limit=limit, before=before, oldest_first=False):
        old_messages.append(old_message)

    # 把讀到的歷史訊息從最舊到最新排序，然後轉成 OpenAI API 需要的格式。
    for old_message in reversed(old_messages):
        content = old_message.content.strip()
        if not content:  # 如果訊息內容不為空，才加入歷史訊息
            continue

        if old_message.author.id == bot_user.id:
            history_messages.append({"role": "assistant", "content": content})
        else:
            speaker_type = "機器人" if old_message.author.bot else "使用者"
            speaker_mention = old_message.author.mention  # 直接使用 mention 格式，讓 AI 可以在回覆時複製貼上
            user_content = (
                f"{old_message.author.display_name}"
                f"（{speaker_type}，mention：{speaker_mention} 說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages


async def ask_with_discord_history(message):
    """取得頻道歷史訊息，並將其加入訊息中，再呼叫 AI 回應。"""
    history_messages = await get_channel_history(
        channel=message.channel,bot_user=bot.user,limit=CHANNEL_HISTORY_LIMIT,before=message)
    

    user_question = message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not user_question:
        user_question = "請根據前面的頻道對話，接著回應大家。"


    user_message = (
        f"{message.author.display_name}"
        f" (mention:{message.author.mention}) 提到你：{user_question}"
    )

    # 將先前的訊息加入訊息中，並呼叫 AI 回應
    # 沒有歷史時可以不傳，有歷史時就把整理好的舊對話傳給 AI，讓它知道前面大家在聊什麼。
    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_message=user_message,
        history_messages=history_messages,
        temperature=OPENAI_TEMPERATURE,
        model=OPENAI_MODEL,
    )

#######################事件#######################
# @bot.event 這種寫法叫裝飾器，可以把它想成幫下面的函式貼上一張「事件處理員」標籤。
# def 是一般函式，通常會照順序一路做完。
# async def 是可以搭配 await 的函式；遇到需要等一下的工作時，
# 它可以先暫停，等事情完成後再回來繼續做。
@bot.event
async def on_ready():
    print(
        f"{bot.user} is ready and online!"
    )  # 當機器人登入成功並準備好時，印出提示訊息
    # await 的意思比較像「這件事要花時間，先等它完成再往下」。
    # 它和 return 不一樣：await 等完之後還會繼續跑下面的程式；return 則是直接結束函式。
    # 這裡的 tree.sync() 會把我們寫好的 slash 指令送去 Discord 登記。
    await tree.sync()


@bot.event
async def on_message(message):
    # message 就是剛剛出現在頻道裡的一則訊息。
    if message.author == bot.user:
      # 如果這句話是機器人自己說的，就不要回應自己，才不會一直自言自語
        return  # return 是「直接結束這個函式」；它不像 await 只是等一下，而是真的先離開這次工作
    if message.content == "hello":  # 如果訊息內容為 hello
        # send() 需要經過網路把訊息送回 Discord，所以要用 await 等它送完。
        await message.channel.send("Hi,gay!")  # 回應 Hey!

    elif bot.user in message.mentions:
        async with message.channel.typing():  # 顯示「機器人正在輸入中」的狀態
            answer, error = await ask_with_discord_history(message)

            if error:
                await message.channel.send(error)
            else:
                await message.reply(answer, mention_author=True, allowed_mentions=AI_REPLY_ALLOWED_MENTIONS)


#######################指令#######################
# @tree.command(...) 也是裝飾器，作用是幫下面的函式貼上「這是一個 slash 指令」的標籤。
# 使用者在 Discord 輸入 /hello 時，就會呼叫下面這個函式。
# slash 指令通常要和 Discord 來回溝通，所以這裡用 async def 來寫。
@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    """輸入 /hello，機器人會回傳 Hey!"""
    # interaction 可以想成「這次有人使用指令時送來的資料包」，
    # 裡面會記錄是誰按的、在哪個地方按的，以及這次指令的相關資訊。
    # send_message() 也是網路工作，所以前面要加 await。
    await interaction.response.send_message("Hey!")  # 把 Hey! 回傳給使用者


# /weather 的重點是：
# 把「查資料」交給 WeatherAPI，把「回應使用者」留在 Bot 主程式處理。
@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入 /weather 並提供城市名稱，會回傳當前天氣資訊。"""
    # defer() 會先告訴 Discord「機器人正在處理中」，
    # 這樣查天氣需要一點時間時，指令就不會因為等太久而失敗。
    await interaction.response.defer()

    city = city.strip()  # 去掉前後空白，避免多打一格空白造成查詢失敗

    if not weather_api.api_key:
        # 如果 .env 沒有 WEATHER_API_KEY，就先提醒使用者補上設定
        await interaction.followup.send(
            "尚未設定 WEATHER_API_KEY，請先在 .env 檔案中完成設定。"
        )
        return

    try:
        if not forecast:
            # 向 WeatherAPI 拿整理好的天氣摘要，
            # 主程式只要處理結果，不用自己拆很多層字典。
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(f"找不到 **{city}** 的天氣資訊。")
                return

            embed = build_weather_embed(weather_summary)  # 先把整理好的資料排成卡片
            await interaction.followup.send(embed=embed)
            return

        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                # 回傳 None 通常代表城市名稱錯誤，或 API 沒有找到主要天氣資料
                await interaction.followup.send(f"找不到 **{city}** 的天氣預報。")
                return
            embeds = build_forecast_embeds(forecast_summary)
            await interaction.followup.send(embeds=embeds[:10])
            return

        raw_forecast = weather_api.get_forecast(city)
    # defer() 之後，要用 followup.send() 送出正式結果
    except (requests.RequestException, ValueError):
        # 如果查詢途中發生網路錯誤或資料格式問題，就回傳通用錯誤訊息
        await interaction.followup.send("目前無法取得天氣資料，請稍後再試。")
        return

    analysis, error = ai_assistant.ask(
        system_prompt="你是一個專業的氣象預報員，會根據提供的天氣資料，整理出一段簡短的預報摘要，讓一般人也能輕鬆理解未來幾天的天氣狀況。",
        user_message=f"請根據以下的{city}天氣預報資料，幫我整理出一段簡短的預報摘要：\n{raw_forecast}"
    )

    if error:
        await interaction.followup.send(error)
    else:
        await interaction.followup.send(f"**{city}** 的天氣預報摘要：\n{analysis}")
    

    
#######################啟動#######################
# def main() 把「啟動機器人」這件事單獨包成一個步驟。
# 這樣主程式看起來更整齊，以後如果啟動前還要加其他設定，也知道要放在哪裡。
# 這裡用普通的 def 就夠了，因為 main() 只是負責開始執行程式，
# 不需要在裡面 await 其他非同步工作。
def main():
    # os.getenv("DC_BOT_TOKEN") 會去 .env 裡找機器人的 token。
    # bot.run(...) 會讓機器人登入 Discord，然後開始待命。
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 這個 if 可以想成一道入口檢查：
# 只有當這份檔案是「被直接執行」時，才會呼叫 main() 啟動機器人。
# 如果這份檔案只是被別的程式 import 進去，下面的 main() 就不會自動執行。
if __name__ == "__main__":
    main()  # 從這裡正式啟動整個程式
