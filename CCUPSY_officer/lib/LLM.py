#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from Account import *
"""
Account 變數函數清單
[變數] BASE_PATH       => 根目錄位置
[變數] LIB_PATH        => lib 目錄位置
[變數] INTENT_PATH     => intent 目錄位置
[變數] REPLY_PATH      => reply 目錄位置
[變數] ACCOUNT_DICT    => account.info 內容
[變數] ARTICUT         => ArticutAPI (需安裝 ArticutAPI 及有效的 username, api_key)
"""

from collections import Counter
from random import choice
from requests import post
from time import sleep
import math

def getCopyToaster(inputSTR, count=3):
    resultLIST = []
    if ACCOUNT_DICT["username"] and ACCOUNT_DICT["copytoaster_key"]:
        url = f"{ACCOUNT_DICT['server']}/CopyToaster/API/V2/"
        payload = {
            "username": ACCOUNT_DICT["username"],
            "copytoaster_key": ACCOUNT_DICT["copytoaster_key"],
            "input_str": inputSTR,
            "count": count
        }

        for category in ACCOUNT_DICT["copytoaster_category"]:
            payload["category"] = category
            while True:
                try:
                    response = post(url, json=payload).json()
                    if response["status"]:
                        if response["progress_status"] == "completed":
                            for r in response["result_list"]:
                                resultLIST.append(r["document"].split(">>\\n")[1])
                                break
                    else:
                        print(f"[getCopyToaster] Category: {category} => {response['msg']}")
                        break
                except Exception as e:
                    print(f"[getCopyToaster] {str(e)}")
                    break

                sleep(1.2)

    return resultLIST
"""
使用 CopyToaster API 搜尋相關文件內容
參數:
    inputSTR: 輸入的查詢字串
    count: 要返回的結果數量（預設為3）
返回:
    resultLIST: 包含搜尋結果的列表
"""


def getLokiLLM(inputSTR, referenceSTR=""):
    responseSTR = ""
    sourceSTR = ""
    if ACCOUNT_DICT["chatbot_prompt"]:
        url = f"{ACCOUNT_DICT['server']}/Loki/Call/"
        payload = {
            "username": ACCOUNT_DICT["username"],
            "loki_key": ACCOUNT_DICT["loki_key"],
            "intent": list(ACCOUNT_DICT["chatbot_prompt"])[0],
            "func": "run_alias",
            "data": {
                "messages": []
            }
        }
        if ACCOUNT_DICT["llm_prompt"]["system"]:
            payload["data"]["messages"].append({"role": "system", "content": ACCOUNT_DICT["llm_prompt"]["system"]})
        if ACCOUNT_DICT["llm_prompt"]["assistant"]:
            payload["data"]["messages"].append({"role": "assistant", "content": ACCOUNT_DICT["llm_prompt"]["assistant"]})

        headerSTR = ""
        if referenceSTR and type(referenceSTR) == str:
            contentSTR = f"你將只使用以下參考事實，且僅使用以下事實：\n{referenceSTR}\n"
            if "{{INPUT}}" in ACCOUNT_DICT["llm_prompt"]["user"]:
                contentSTR += ACCOUNT_DICT["llm_prompt"]["user"].replace("{{INPUT}}", inputSTR)
            else:
                contentSTR += inputSTR

            payload["data"]["messages"].append({"role": "user", "content": contentSTR})
            sourceSTR = "RAG_reply"
        else:
            contentSTR = inputSTR
            if "{{INPUT}}" in ACCOUNT_DICT["llm_prompt"]["user"]:
                contentSTR = ACCOUNT_DICT["llm_prompt"]["user"].replace("{{INPUT}}", inputSTR)

            payload["data"]["messages"].append({"role": "user", "content": contentSTR})
            sourceSTR = "LLM_reply"
            try:
                headerSTR = choice(ACCOUNT_DICT["llm_prompt"]["resp_header"])
            except:
                headerSTR = "使用者您好: 我的資料庫沒有相關的資料，但網路資料顯示..."

        try:
            result = post(url, json=payload).json()
            if result["status"]:
                responseSTR = result["result_list"][0]["message"]["content"]
                if headerSTR:
                    responseSTR = f"{headerSTR}\n{responseSTR}"
            else:
                print(f"[getLokiLLM] {result['msg']}")
        except Exception as e:
            print(f"[getLokiLLM] {str(e)}")

    return responseSTR, sourceSTR
"""
使用 Loki LLM API 生成回應
參數:
    inputSTR: 使用者輸入的文字
    referenceSTR: 參考文本（可選）
返回:
    responseSTR: LLM 生成的回應
    sourceSTR: 回應來源（'RAG_reply' 或 'LLM_reply'）
"""


def callLLM(inputSTR):
    copyToasterResultLIST = getCopyToaster(inputSTR)
    if copyToasterResultLIST:
        referenceSTR = "\n".join(copyToasterResultLIST)
    else:
        referenceSTR = ""

    llmResultSTR, sourceSTR = getLokiLLM(inputSTR, referenceSTR=referenceSTR)
    return llmResultSTR, sourceSTR
"""
整合 CopyToaster 和 Loki LLM 的功能
先使用 CopyToaster 搜尋相關內容，再將結果作為參考傳給 LLM
參數:
    inputSTR: 使用者輸入的文字
返回:
    llmResultSTR: LLM 生成的回應
    sourceSTR: 回應來源
"""


def counterCosineSimilarity(count1DICT, count2DICT):
    terms = set(count1DICT).union(count2DICT)
    dotprod = sum(count1DICT.get(k, 0) * count2DICT.get(k, 0) for k in terms)
    magA = math.sqrt(sum(count1DICT.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(count2DICT.get(k, 0)**2 for k in terms))
    similarity = dotprod / (magA * magB) if magA and magB else 0
    return similarity
"""
計算兩個計數字典之間的餘弦相似度
參數:
    count1DICT: 第一個計數字典
    count2DICT: 第二個計數字典
返回:
    similarity: 相似度分數（0-1之間）
"""


def getCosineSimilarityUtterance(inputSTR, utteranceDICT):
    scoreDICT = {
        "utterance": "",
        "score": 0
    }
    if ARTICUT:
        atcResultDICT = ARTICUT.parse(inputSTR)
        verbLIST = [x[2] for x in sum(ARTICUT.getVerbStemLIST(atcResultDICT), [])]
        nounLIST = [x[2] for x in sum(ARTICUT.getNounStemLIST(atcResultDICT), [])]
        wordCountDICT = dict(Counter([x.strip().lower() for x in verbLIST + nounLIST]))
        for utterance_s, count_d in utteranceDICT.items():
            score = counterCosineSimilarity(count_d, wordCountDICT)
            if score > scoreDICT["score"]:
                scoreDICT["utterance"] =  utterance_s
                scoreDICT["score"] = score

    return scoreDICT
"""
計算輸入文字與預設語句之間的相似度
使用 Articut 進行中文分詞，並計算詞彙相似度
參數:
    inputSTR: 輸入的文字
    utteranceDICT: 預設語句字典
返回:
    scoreDICT: 包含最相似語句和分數的字典
"""

def getCosineSimilarity(input1STR, input2STR):
    score = 0
    if ARTICUT:
        # [input1STR result, input2STR result]
        atcResultLIST = [ARTICUT.parse(input1STR), ARTICUT.parse(input2STR)]
        verbLIST = []
        nounLIST = []
        wordCountLIST = []
        for atcResultDICT in atcResultLIST:
            verbLIST.append([x[2] for x in sum(ARTICUT.getVerbStemLIST(atcResultDICT), [])])
            nounLIST.append([x[2] for x in sum(ARTICUT.getNounStemLIST(atcResultDICT), [])])
            wordCountLIST.append(dict(Counter([x.strip().lower() for x in verbLIST + nounLIST])))

        score = counterCosineSimilarity(wordCountLIST[0], wordCountLIST[1])

    return score
"""
計算兩段文字之間的相似度
使用 Articut 進行中文分詞，並計算詞彙相似度
參數:
    input1STR: 第一段文字
    input2STR: 第二段文字
返回:
    score: 相似度分數（0-1之間）
"""


def getLLM(system="", assistant="", user=""):
    resultSTR = ""
    if ACCOUNT_DICT["chatbot_prompt"]:
        url = f"{ACCOUNT_DICT['server']}/Loki/Call/"
        payload = {
            "username": ACCOUNT_DICT["username"],
            "loki_key": ACCOUNT_DICT["loki_key"],
            "intent": list(ACCOUNT_DICT["chatbot_prompt"])[0],
            "func": "run_alias",
            "data": {
                "messages": []
            }
        }
        if system:
            payload["data"]["messages"].append({"role": "system", "content": system})
        if assistant:
            payload["data"]["messages"].append({"role": "assistant", "content": assistant})
        if user:
            payload["data"]["messages"].append({"role": "user", "content": user})

        if payload["data"]["messages"]:
            try:
                result = post(url, json=payload).json()
                if result["status"]:
                    try:
                        headerSTR = choice(ACCOUNT_DICT["llm_prompt"]["resp_header"])
                    except:
                        headerSTR = "使用者您好:我的資料庫沒有相關的資料，但網路資料顯示..."

                    resultSTR = result["result_list"][0]["message"]["content"]
                    resultSTR = f"{headerSTR}\n{resultSTR}"
                else:
                    print(f"[getLLM] {result['msg']}")
            except Exception as e:
                print(f"[getLLM] {str(e)}")

    return resultSTR
"""
直接調用 Loki LLM API 進行對話
參數:
    system: 系統提示詞（可選）
    assistant: 助理回應（可選）
    user: 使用者輸入（可選）
返回:
    resultSTR: LLM 生成的回應
"""


if __name__ == "__main__":
    inputSTR = "你好，請問你是甚麼機器人"
    resultSTR, sourceSTR = callLLM(inputSTR)
    print(sourceSTR)
    print(resultSTR)