#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #用於設定根目錄
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

LIB_PATH = os.path.join(BASE_PATH, "lib")
if LIB_PATH not in sys.path:
    sys.path.insert(1, LIB_PATH)
#設定lib目錄的路徑

INTENT_PATH = os.path.join(BASE_PATH, "intent")
if INTENT_PATH not in sys.path:
    sys.path.insert(2, INTENT_PATH)
#設定intent目錄的路徑

REPLY_PATH = os.path.join(BASE_PATH, "reply")
if REPLY_PATH not in sys.path:
    sys.path.insert(3, REPLY_PATH)
#設定reply目錄的路徑

ACCOUNT_DICT = {
    "debug": os.getenv('DEBUG_MODE', 'True').lower() == 'true',
    "server": os.getenv('DROIDTOWN_SERVER', 'https://api.droidtown.co'),
    "username": os.getenv('DROIDTOWN_USERNAME'),
    "api_key": os.getenv('DROIDTOWN_API_KEY'),
    "loki_key": os.getenv('DROIDTOWN_LOKI_KEY'),
    "copytoaster_key": os.getenv('DROIDTOWN_COPYTOASTER_KEY'),
    "copytoaster_category": [],
    "llm_prompt": {
        "system": os.getenv('LLM_SYSTEM_PROMPT', '你是一個只會使用繁體中文的對話助理。嚴格執行：1.絕對禁止使用任何英文 2.絕對禁止使用任何拼音 3.絕對禁止進行任何形式的翻譯 4.絕對禁止進行任何語言解釋 5.只允許純繁體中文對話 6.收到訊息後直接用中文回應，不要做任何額外的事情'),
        "assistant": os.getenv('LLM_ASSISTANT_PROMPT', '我只會用純繁體中文回應'),
        "user": os.getenv('LLM_USER_PROMPT', "'{{INPUT}}'。請直接用純繁體中文回應。禁止：翻譯、解釋、英文、拼音。"),
        "resp_header": [""]
    },
    "chatbot_mode": os.getenv('CHATBOT_MODE', 'True').lower() == 'true',
    "chatbot_prompt": {}
}
#設定系統需要的token或是參數的設定環節

try:
    accountInfo = json.load(open(os.path.join(BASE_PATH, "account.info"), encoding="utf-8"))
    ACCOUNT_DICT.update(accountInfo)
except Exception as e:
    print("[ERROR] AccountInfo => {}".format(str(e)))

from ArticutAPI import ArticutAPI
try:
    ARTICUT = ArticutAPI.Articut(username=ACCOUNT_DICT["username"], apikey=ACCOUNT_DICT["api_key"])
except Exception as e:
    print("[ERROR] ArticutAPI => {}".format(str(e)))
    ARTICUT = None