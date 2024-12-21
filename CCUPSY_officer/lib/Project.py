#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    中正大學心理系辦公室聊天機器人核心處理模組

    主要功能：
    1. 意圖識別：識別用戶輸入的意圖（例如：詢問信箱、課程資訊等）
    2. 動態模組載入：自動載入所有意圖處理模組
    3. API 整合：與 Loki API 進行通訊，處理自然語言理解
    4. 回應生成：根據識別結果生成適當的回應

    處理流程：
    1. 接收用戶輸入
    2. 將輸入發送給 Loki API 進行意圖識別
    3. 根據識別結果調用對應的處理模組
    4. 生成回應並返回

    API 回應格式範例：
    {
        "status": True,
        "msg": "Success!",
        "version": "v223",
        "word_count_balance": 2000,
        "result_list": [
            {
                "status": True,
                "msg": "Success!",
                "results": [
                    {
                        "intent": "intentName",
                        "pattern": "matchPattern",
                        "utterance": "matchUtterance",
                        "argument": ["arg1", "arg2", ... "argN"]
                    },
                    ...
                ]
            },
            {
                "status": False,
                "msg": "No matching Intent."
            }
        ]
    }
"""
#此為回應的格式

# 導入必要的模組
from .Account import *
"""
Account 變數函數清單
[變數] BASE_PATH       => 根目錄位置
[變數] LIB_PATH        => lib 目錄位置
[變數] INTENT_PATH     => intent 目錄位置
[變數] REPLY_PATH      => reply 目錄位置
[變數] ACCOUNT_DICT    => account.info 內容
[變數] ARTICUT         => ArticutAPI (需安裝 ArticutAPI 及有效的 username, api_key)
"""
from .LLM import callLLM

# 導入 Python 標準庫
from copy import deepcopy  # 用於深度複製字典
from glob import glob      # 用於檔案路徑模式匹配
from importlib import import_module  # 用於動態導入模組
from pathlib import Path   # 用於處理檔案路徑
from requests import post, codes  # 用於發送 HTTP 請求
import json
import math
import os
import re

# 動態載入所有意圖處理模組
lokiIntentDICT = {}
for modulePath in glob("{}/intent/Loki_*.py".format(BASE_PATH)):
    moduleNameSTR = Path(modulePath).stem[5:]  # 取得模組名稱（移除 'Loki_' 前綴）
    modulePathSTR = modulePath.replace(BASE_PATH, "").replace(".py", "").replace("/", ".").replace("\\", ".")[1:]
    globals()[moduleNameSTR] = import_module(modulePathSTR)  # 動態導入模組
    lokiIntentDICT[moduleNameSTR] = globals()[moduleNameSTR]  # 儲存模組引用


INTENT_FILTER = []
INPUT_LIMIT = 20
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖



class LokiResult():
    """
    Loki API 結果處理類別
    用於處理和存儲來自 Loki API 的回應結果
    """
    
    def __init__(self, inputLIST, filterLIST):
        """
        初始化 LokiResult 物件
        參數：
            inputLIST：輸入句子列表
            filterLIST：意圖過濾列表
        """
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            # 發送請求到 Loki API
            url = "{}/Loki/BulkAPI/".format(ACCOUNT_DICT["server"])
            result = post(url, json={
                "username": ACCOUNT_DICT["username"],
                "input_list": inputLIST,
                "loki_key": ACCOUNT_DICT["loki_key"],
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    if "word_count_balance" in result:
                        self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "{} Connection failed.".format(result.status_code)
        except Exception as e:
            self.message = str(e)

    # 以下是各種獲取結果的方法
    def getStatus(self):
        """獲取整體處理狀態"""
        return self.status

    def getMessage(self):
        """獲取處理訊息"""
        return self.message

    def getVersion(self):
        """獲取 API 版本"""
        return self.version

    def getBalance(self):
        """獲取剩餘字數額度"""
        return self.balance

    def getLokiStatus(self, index):
        """獲取特定索引的處理狀態"""
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        """獲取特定索引的處理訊息"""
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        """獲取特定索引的結果數量"""
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        """獲取特定位置的完整結果"""
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        """獲取特定位置的意圖"""
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        """獲取特定位置的匹配模式"""
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        """獲取特定位置的原始句子"""
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        """獲取特定位置的參數列表"""
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[], refDICT={}, toolkitDICT={}):
    """
    執行 Loki 意圖分析
    參數：
        inputLIST：輸入句子列表
        filterLIST：意圖過濾列表
        refDICT：參考字典
        toolkitDICT：工具字典
    返回：
        resultDICT：處理結果字典
    """
    resultDICT = deepcopy(refDICT)
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            lokiResultDICT = {k: [] for k in refDICT}
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                if lokiRst.getIntent(index, resultIndex) in lokiIntentDICT:
                    lokiResultDICT = lokiIntentDICT[lokiRst.getIntent(index, resultIndex)].getResult(
                        key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex),
                        lokiResultDICT, refDICT, pattern=lokiRst.getPattern(index, resultIndex), toolkitDICT=toolkitDICT)

            # 將處理結果合併到最終結果中
            for k in lokiResultDICT:
                if k not in resultDICT:
                    resultDICT[k] = []
                if type(lokiResultDICT[k]) == list:
                    resultDICT[k].extend(lokiResultDICT[k])
                else:
                    resultDICT[k].append(lokiResultDICT[k])

    return resultDICT

def execLoki(content, filterLIST=[], splitLIST=[], refDICT={}, toolkitDICT={}):
    """
    執行 Loki 處理流程
    參數：
        content：輸入內容
        filterLIST：意圖過濾列表
        splitLIST：分句符號列表
        refDICT：參考字典
        toolkitDICT：工具字典
    返回：
        resultDICT：處理結果字典
    """
    # 將輸入內容轉換為句子列表
    if isinstance(content, str):
        contentLIST = [content]
    else:
        contentLIST = content

    # 如果沒有提供分句符號列表，使用預設的
    if splitLIST == []:
        splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "　", ";"]

    # 將句子按照分句符號分割
    splitLIST = list(filter(None, splitLIST))
    resultDICT = {}
    lokiResultDICT = runLoki(contentLIST, filterLIST, refDICT, toolkitDICT)

    # 如果有結果
    if lokiResultDICT and "response" in lokiResultDICT:
        resultDICT["response"] = lokiResultDICT["response"]
        if "source" in lokiResultDICT:
            resultDICT["source"] = lokiResultDICT["source"]
    else:
        # 如果沒有匹配到任何意圖，使用 LLM
        try:
            llm_response, source = callLLM(content)
            resultDICT["response"] = "使用者您好: 我的資料庫沒有相關的資料，可以請你換種方式再問我一次。而對此我不懂的內容我會先經過網路進行查詢，網路資料顯示...(為不準確之答案，請謹慎參考)" + llm_response
            resultDICT["source"] = source if source else "LLM_reply"
        except Exception as e:
            print(f"LLM 調用失敗: {str(e)}")
            resultDICT["response"] = "抱歉，我暫時無法回答這個問題。請稍後再試。"
            resultDICT["source"] = "error"

    return resultDICT

def testLoki(inputLIST, filterLIST=[]):
    """
    測試 Loki 處理結果
    參數：
        inputLIST：測試句子列表
        filterLIST：意圖過濾列表
    """
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            print("#", key)
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                print("\t", lokiRst.getIntent(index, resultIndex))
                print("\t", lokiRst.getPattern(index, resultIndex))
                print("\t", lokiRst.getUtterance(index, resultIndex))
                print("\t", lokiRst.getArgs(index, resultIndex))
            print()
    else:
        print(lokiRst.getMessage())

def testIntent():
    """
    測試所有已載入的意圖模組
    """
    # 打印分隔線
    print("="*80)
    # 打印標題
    print("測試所有意圖模組：")
    print("-"*80)
    # 測試每個意圖模組
    for moduleName in lokiIntentDICT:
        print("Intent:", moduleName)
        print("Pattern:", lokiIntentDICT[moduleName].PATTERN)
        print("utterance:", lokiIntentDICT[moduleName].UTTERANCE)
        print()
    print("="*80)

if __name__ == "__main__":
    # 測試程式進入點
    from pprint import pprint
    # 測試句子
    contentSTR = "蔡玲玲教授有哪些研究專長"  # 改為單一字符串
    filterLIST = []
    resultDICT = execLoki(contentSTR, filterLIST)  # 傳入字符串而不是列表
    print("Result:")
    pprint(resultDICT)