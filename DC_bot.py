import os
import discord
from pprint import pprint
from dotenv import load_dotenv
from CCUPSY_officer.lib.Project import execLoki

# 載入環境變數
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 設置 Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 已經上線了！')

@bot.event
async def on_message(message):
    # 如果訊息來自 bot 本身，則忽略
    if message.author == bot.user:
        return

    try:
        # 獲取訊息內容
        contentSTR = message.content
        
        # 處理訊息
        filterLIST = []
        resultDICT = execLoki(contentSTR, filterLIST)
        
        # 如果有回應，發送訊息
        if resultDICT and "response" in resultDICT:
            response = resultDICT["response"]
            # 判斷回應類型
            if isinstance(response, str):
                await message.channel.send(response)
            else:
                await message.channel.send(response[0])
        else:
            # 可以設置一個預設回應
            await message.channel.send("抱歉，我不太理解您的意思。")
            
    except Exception as e:
        print(f"處理訊息時發生錯誤: {str(e)}")
        await message.channel.send("抱歉，處理您的訊息時發生錯誤。")

# 運行 bot
bot.run(TOKEN)