#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for ask_lecture_activity

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
import requests
from lxml import html
import pandas as pd

INTENT_NAME = "ask_lecture_activity"
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

def get_activities():
    """
    用爬蟲爬取系上活動
    """
    try:
        # 發送請求到系網
        url = "https://psy.ccu.edu.tw/p/403-1085-1956-1.php?Lang=zh-tw"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 設置正確的編碼
        
        # 解析HTML
        tree = html.fromstring(response.content)
        
        # 使用XPath提取活動標題
        activities = tree.xpath('//*[@id="pageptlist"]//a/@title')
        
        # 格式化活動資訊
        if activities:
            return "\n".join(activities[:5])
        else:
            return "目前沒有最新活動資訊，請參考系網公告。"
            
    except requests.exceptions.RequestException as e:
        print(f"網絡請求出錯: {str(e)}")
        return "抱歉，無法取得活動資訊，請檢查您的網路連線或直接查看系網公告。"
    except Exception as e:
        print(f"解析活動資訊時發生錯誤: {str(e)}")
        return "抱歉，目前無法取得活動資訊，請直接查看系網公告。"

def get_courses(args):
    """
    從Excel檔案讀取課程資訊
    Args:
        args: 參數列表，包含學期和學制資訊
    Returns:
        str: 格式化的課程清單
    """
    # 定義關鍵字
    semesters = ['上學期', '下學期']
    programs = ['大學部', '研究所']
    
    # 從args中找出學期和學制
    semester = next((arg for arg in args if arg in semesters), None)
    program = next((arg for arg in args if arg in programs), None)
    
    # 如果只有學制沒有學期，返回該學制的所有課程
    if program and not semester:
        try:
            all_courses = []
            # 讀取該學制的上下學期課程
            for sem in semesters:
                filename = get_filename(sem, program)
                if filename:
                    file_path = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", filename)
                    df = pd.read_excel(file_path)
                    courses = df['Subject'].tolist()
                    # 為每個學期的課程添加標題
                    all_courses.append(f"\n{sem}：")
                    all_courses.extend([f"{i+1}. {course}" for i, course in enumerate(courses)])
            
            if all_courses:
                return f"{program}課程如下：{''.join(all_courses)}"
            else:
                return f"找不到{program}的課程資訊。"
                
        except Exception as e:
            print(f"讀取課程資訊時發生錯誤: {str(e)}")
            return "抱歉，無法讀取課程資訊。"
    
    # 如果有完整的學期和學制資訊
    if semester and program:
        try:
            filename = get_filename(semester, program)
            if not filename:
                return "無法找到對應的課程資訊。"
                
            file_path = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", filename)
            df = pd.read_excel(file_path)
            courses = df['Subject'].tolist()
            
            formatted_courses = "\n".join(f"{i+1}. {course}" for i, course in enumerate(courses))
            return f"{semester}{program}課程如下：\n{formatted_courses}"
            
        except Exception as e:
            print(f"讀取課程資訊時發生錯誤: {str(e)}")
            return "抱歉，無法讀取課程資訊。"
    
    return "請指定要查詢的學制（大學部/研究所）。"

def get_filename(semester, program):
    """
    獲取對應的檔案名稱
    """
    file_mapping = {
        ('上學期', '大學部'): "Undergraduate_Program_First_Semester.xlsx",
        ('下學期', '大學部'): "Undergraduate_Program_second_Semester.xlsx",
        ('上學期', '研究所'): "Graduate_Program_First_Semester.xlsx",
        ('下學期', '研究所'): "Graduate_Program_second_Semester.xlsx"
    }
    return file_mapping.get((semester, program))

def getReply(utterance, args):
    try:
        # 檢查 args 中是否包含"活動"
        has_activity = any("活動" in arg for arg in args) if args else False
        
        if has_activity:
            # 爬取系網活動資訊
            activities = get_activities()
            replySTR = f"最近的系上活動：\n{activities}\n\n更多內容請參考：https://psy.ccu.edu.tw/p/403-1085-1956-1.php?Lang=zh-tw"
        else:
            # 處理課程查詢
            if args:
                replySTR = get_courses(args)
            else:
                replySTR = (replyDICT[utterance], 1)[0]
        
    except Exception as e:
        print(f"處理回覆時發生錯誤: {str(e)}")
        replySTR = "抱歉，處理您的請求時發生錯誤。"

    return replySTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
    debugInfo(inputSTR, utterance)
    if utterance == "[上學期][大學部]有哪些課程":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[大學部]有哪些課程":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[上學期][大學部]的[課程]有哪些":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[上學期][大學部]課程":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[上學期][大學部]開哪些課程":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[系上][最近]有哪些[活動]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[系上][最近]的[活動]有哪些":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[系上]有哪些[活動]":
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
