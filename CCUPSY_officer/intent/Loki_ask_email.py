#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for ask_email

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""

from ast import arg
from random import sample
import json
import os
import sys
from tabnanny import check
import pandas as pd

INTENT_NAME = "ask_email"
CWD_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(os.path.dirname(CWD_PATH), "lib"))

from Account import *
"""
Account 變數函數清單
[變數] BASE_PATH       => 根目錄位置
[變數] LIB_PATH        => lib 目錄位置
[變數] INTENT_PATH     => intent 目錄位置
[變數] REPLY_PATH      => reply 目錄位置
[變數] ACCOUNT_DICT    => account.info 內容
[變數] ARTICUT         => ArticutAPI (用法：ARTICUT.parse()。 #需安裝 ArticutAPI.)
"""

sys.path.pop(-1)

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(CWD_PATH, "USER_DEFINED.json"), encoding="utf-8"))
except:
    pass

replyDICT = {}
replyPathSTR = os.path.join(REPLY_PATH, "reply_{}.json".format(INTENT_NAME))
if os.path.exists(replyPathSTR):
    try:
        replyDICT = json.load(open(replyPathSTR, encoding="utf-8"))
    except Exception as e:
        print("[ERROR] reply_{}.json => {}".format(INTENT_NAME, str(e)))
CHATBOT = True if replyDICT else False

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if ACCOUNT_DICT["debug"]:
        print("[{}] {} ===> {}".format(INTENT_NAME, inputSTR, utterance))

def getReply(utterance, args):
    try:
        # 使用 os.path.join 來組合路徑
        file_path = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", "ccu_emails.xlsx")
        print(f"讀取信箱資料: {file_path}")
        df = pd.read_excel(file_path)
        
        # 取得查詢的名字
        query_name = args[0] if args else None
        if not query_name:
            replySTR = "無法識別查詢對象"
            
        # 使用 str.contains 進行部分匹配
        matched_row = df[df['Name'].str.contains(query_name, na=False)]
        
        if not matched_row.empty:
            # 找到對應的信箱
            email = matched_row.iloc[0]['Email']
            replySTR = replyDICT[utterance].format(query_name) + email
        else:
            replySTR = f"抱歉，找不到 {query_name} 的信箱資訊"

    except Exception as e:
        print(f"查詢過程發生錯誤: {str(e)}")
        replySTR = "查詢信箱時發生錯誤"

    return replySTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
    debugInfo(inputSTR, utterance)
    
    # 初始化 response
    if "response" not in resultDICT:
        resultDICT["response"] = ""
    
    if utterance == "[姜定宇][信箱]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass
    if utterance == "[姜定宇]的[信箱]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass
    
    if utterance == "[姜定宇][教授]的[信箱]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[姜定宇][教授]的[信箱]是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[系辦][信箱]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[電腦][助教][信箱]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[電腦][助教]的[信箱]是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[電腦][助教]的電子郵件地址是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "系辦的[信箱]是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "系辦的電子郵件地址是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass
    
    # 如果沒有找到對應的回應，設置預設回應
    if resultDICT["response"] == "":
        resultDICT["response"] = "抱歉，找不到相關資訊"
        resultDICT["source"] = "default"

    return resultDICT
