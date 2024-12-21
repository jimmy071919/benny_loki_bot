#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Loki 4.0 Chatbot AI 回應產生器
"""

from Account import *
#去導入 Account.py 文件中所有的公開變數、函數和類別
"""
Account 變數函數清單
[變數] BASE_PATH       => 根目錄位置
[變數] LIB_PATH        => lib 目錄位置
[變數] INTENT_PATH     => intent 目錄位置
[變數] REPLY_PATH      => reply 目錄位置
[變數] ACCOUNT_DICT    => account.info 內容
[變數] ARTICUT         => ArticutAPI (需安裝 ArticutAPI 及有效的 username, api_key)
"""

from random import sample
from requests import post
import re
import os
import json

UTTERANCE_PAT = re.compile("^ *if utterance == \"([^\"]+)\":", re.M)
ARGS_PAT = re.compile("[\[\]]")
RESPONSE_ORDER_PAT = re.compile("^[\*\-\+\d•]+[ \.\)]*")
RESPONSE_MARK_PAT = re.compile("^[\"「]|[\"」]$")
MESSAGE_LIMIT = 3500

LOKI_CALL_URL = "{}/Loki/Call/".format(ACCOUNT_DICT["server"])

"""
COLOR_DICT = {
    "GREY":   "30",
    "RED":    "31",
    "GREEN":  "32",
    "YELLOW": "33",
    "BLUE":   "34",
    "PURPLE": "35",
    "CYAN":   "36",
    "WHITE":  "37"
}
"""
#設定顏色
#此功能於DC機器人中可以刪除 故在此註解掉

"""
def setColor(inputSTR, color=COLOR_DICT["WHITE"]):
    return f"\033[1;{color}m{inputSTR}\033[0m"
"""
#此功能於DC機器人中可以刪除 故在此註解掉

def getResponse(intent, system, assistant, user): #用以向 Loki API 發送請求獲取回應
    resultLIST = []
    try:
        payload = {
            "username": ACCOUNT_DICT["username"],
            "loki_key": ACCOUNT_DICT["loki_key"],
            "intent": intent,
            "func": "run_alias",
            "data": {"messages": []}
        }
        
        if assistant: #此為有assistant回應時要做的事情 #assistant為助理的歷史回應
            for assistant_l in assistant:
                payload["data"]["messages"] = system + assistant_l + user
                # 組合訊息：系統訊息 + 助理回應 + 使用者輸入

                result = post(LOKI_CALL_URL, json=payload).json()
                if result["status"]:
                    contentLIST = getLlmResult(result["result_list"][0]).split("\n")
                    for content in contentLIST:
                        content = RESPONSE_ORDER_PAT.sub("", content.strip())
                        content = RESPONSE_MARK_PAT.sub("", content.strip())
                        content = content.strip()
                        if content:
                            resultLIST.append(content)
                else:
                    print("[ERROR] getResponse")
                    print(result)
                    break

            if resultLIST:
                resultLIST = sample(resultLIST, int(len(resultLIST)/len(assistant)))

        else: #此為無assistant回應時要做的事情
            payload["data"]["messages"] = system + user
            # 組合訊息：系統訊息 + 使用者輸入

            result = post(LOKI_CALL_URL, json=payload).json()
            if result["status"]:
                contentLIST = getLlmResult(result["result_list"][0]).split("\n")
                for content in contentLIST:
                    content = RESPONSE_ORDER_PAT.sub("", content.strip())
                    content = RESPONSE_MARK_PAT.sub("", content.strip())
                    content = content.strip()
                    if content:
                        resultLIST.append(content)
            else:
                print("[ERROR] getResponse")
                print(result)
    except Exception as e:
        print("[ERROR] getResponse")
        print(str(e))

    return resultLIST
#這邊的設計，可以讓機器人判斷是「新開始的對話」還是「已經有舊紀錄的對話」 => 進行不同行為

def getLlmResult(resultDICT):
    resultSTR = ""
    keyPAT = re.compile("(^|/)message/content(/|$)")
    pathLIST = _getDictPath(resultDICT)
    for path in pathLIST:
        if keyPAT.search(str(path)):
            resultSTR = _getDictValueByPath(resultDICT, path.split("/"))
            break

    return resultSTR

def _getDictPath(data):
    resultLIST = []
    if type(data) in [dict, list]:
        dataITER = enumerate(data) if type(data) is list else data.items()
        for key, value in dataITER:
            if type(value) in [dict, list]:
                resultLIST.append(key)
                newKeyLIST = _getDictPath(value)
                for newKey in newKeyLIST:
                    resultLIST.append(f"{key}/{newKey}")
            else:
                resultLIST.append(key)

    return resultLIST

def _getDictValueByPath(data, keyLIST):
    if keyLIST:
        keySTR = int(keyLIST[0]) if keyLIST[0].isnumeric() else keyLIST[0]
        return _getDictValueByPath(data[keySTR], keyLIST[1:])
    else:
        return data

def generateReply():
    if ACCOUNT_DICT["chatbot_mode"]:
        # 建立 reply 資料夾
        if not os.path.exists(REPLY_PATH):
            os.mkdir(REPLY_PATH)

        # 讀取 intent utterance
        for intentSTR in ACCOUNT_DICT["chatbot_prompt"]:
            filePath = os.path.join(INTENT_PATH, "Loki_{}.py".format(intentSTR))
            if os.path.exists(filePath):
                textSTR = open(filePath, encoding="utf-8").read()
                utteranceLIST = [gg.group(1) for gg in UTTERANCE_PAT.finditer(textSTR)]
                if utteranceLIST:
                    print(setColor("[Intent] {}".format(intentSTR), COLOR_DICT["YELLOW"]))
                    print("------------------------------------------")
                    promptDICT = {
                        "system": [],
                        "assistant": [],
                        "user": []
                    }

                    # 讀取 prompt, document
                    intentDICT = ACCOUNT_DICT["chatbot_prompt"][intentSTR]
                    if intentDICT["prompt"]["system"]:
                        promptDICT["system"] = [{"role": "system", "content": intentDICT["prompt"]["system"]}]

                    if intentDICT["document"]:
                        if intentDICT["prompt"]["assistant"] == "":
                            keyLIST = ["「{{" + x + "}}」" for x in intentDICT["document"][0]["content"]]
                            intentDICT["prompt"]["assistant"] = "請閱讀內容：{{}}".format("，".join(keyLIST))

                        promptDICT["assistant"] = [[]]
                        for document_d in intentDICT["document"]:
                            contentSTR = intentDICT["prompt"]["assistant"]
                            for k in document_d["content"]:
                                contentSTR = contentSTR.replace("{{" + k + "}}", document_d["content"][k])
                            if contentSTR:
                                if promptDICT["assistant"][-1] and sum(len(assistant_d["content"]) for assistant_d in promptDICT["assistant"][-1]) + len(contentSTR) >= MESSAGE_LIMIT:
                                    promptDICT["assistant"].append([])
                                promptDICT["assistant"][-1].append({"role": "assistant", "content": contentSTR})

                    # 生成回覆
                    try:
                        resultDICT = json.load(open(os.path.join(REPLY_PATH, "reply_{}.json".format(intentSTR)), encoding="utf-8"))
                    except:
                        resultDICT = {}
                    for utterance in utteranceLIST:
                        contentSTR = intentDICT["prompt"]["user"].replace("{{UTTERANCE}}", ARGS_PAT.sub("", utterance))
                        if contentSTR:
                            promptDICT["user"] = [{"role": "user", "content": contentSTR}]

                            responseLIST = getResponse(intentSTR, promptDICT["system"], promptDICT["assistant"], promptDICT["user"])
                            if utterance in resultDICT:
                                resultDICT[utterance].extend(responseLIST)
                                resultDICT[utterance] = list(set(resultDICT[utterance]))
                            else:
                                resultDICT[utterance] = responseLIST
                            print("[Utterance] {}".format(utterance))

                    # 儲存 reply
                    with open(os.path.join(REPLY_PATH, "reply_{}.json".format(intentSTR)), "w", encoding="utf-8") as replyFile:
                        json.dump(resultDICT, replyFile, ensure_ascii=False, indent=4)
                        print("[Success] reply_{}.json".format(intentSTR))

                    print("------------------------------------------")

            else:
                print("[ERROR] {} is not found".format(intentSTR))

        return True
    else:
        print("[INFO] Disable Chatbot Mode")

    return False


if __name__ == "__main__":
    status = generateReply()
