#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for professor_PersonalInterest

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

from random import sample
import json
import os
import sys
import pandas as pd

INTENT_NAME = "professor_PersonalInterest"
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

def get_all_professors():
    """
    獲取所有教授名字
    """
    try:
        filepath = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", "professor_PersonalInterest.xlsx")
        df = pd.read_excel(filepath)
        # 獲取列名（教授名字）
        professors = df.columns.tolist()
        # 排除非教授名字的列
        professors = [name for name in professors if pd.notna(name) and isinstance(name, str) and name != 'Unnamed: 0']
        return professors
    except Exception as e:
        print(f"獲取教授名單時發生錯誤: {str(e)}")
        return []

def getprofessor_PersonalInterest(args):
    """
    根據參數查找教授
    """
    try:
        professors = get_all_professors()
        # 檢查args中有無教授名稱
        if args:
            for arg in args:
                if arg in professors:
                    return arg
        return None
    except Exception as e:
        print(f"查找教授時發生錯誤: {str(e)}")
        return None

def get_professor_interests(professor_name):
    """
    獲取特定教授的研究專長
    """
    try:
        filepath = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", "professor_PersonalInterest.xlsx")
        df = pd.read_excel(filepath)
        
        # 檢查教授是否在列名中
        if professor_name in df.columns:
            # 獲取該教授的所有研究專長（排除NaN值）
            interests = df[professor_name].dropna().tolist()
            return interests
        return []
    except Exception as e:
        print(f"獲取教授研究專長時發生錯誤: {str(e)}")
        return []

def getReply(utterance, args):
    try:
        professor = getprofessor_PersonalInterest(args)
        if professor and utterance in replyDICT:
            # 獲取教授的研究專長
            interests = get_professor_interests(professor)
            if interests:
                # 格式化研究專長列表
                interests_str = "\n".join(f"{i+1}. {interest}" for i, interest in enumerate(interests))
                # 組合完整回應
                replySTR = f"{replyDICT[utterance].format(professor)}\n{interests_str}"
            else:
                replySTR = f"抱歉，找不到{professor}教授的研究專長資訊。"
        else:
            replySTR = replyDICT.get("default", "")
    except Exception as e:
        print(f"getReply 發生錯誤: {str(e)}")
        replySTR = replyDICT.get("default", "")

    return replySTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
    debugInfo(inputSTR, utterance)
    if utterance == "[姜定宇][教授]有哪些[研究專長]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[姜定宇][老師]在[社心][中]有哪些[研究專長]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[姜定宇][老師]的[研究專長]是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[姜定宇][老師]的[研究專長]有哪些":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[姜定宇]的[研究專長]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[社心][姜定宇][老師]的[研究專長]是什麼":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    return resultDICT


if __name__ == "__main__":
    from pprint import pprint

    resultDICT = getResult("姜定宇的研究專長", "[姜定宇]的[研究專長]", [], {}, {})
    pprint(resultDICT)