# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# """
#     Loki module for ask_examination

#     Input:
#         inputSTR      str,
#         utterance     str,
#         args          str[],
#         resultDICT    dict,
#         refDICT       dict,
#         pattern       str

#     Output:
#         resultDICT    dict
# """

# from random import sample
# import json
# import os
# import sys

# INTENT_NAME = "ask_examination"
# CWD_PATH = os.path.dirname(os.path.abspath(__file__))

# sys.path.append(os.path.join(os.path.dirname(CWD_PATH), "lib"))

# from Account import *
# """
# Account 變數函數清單
# [變數] BASE_PATH       => 根目錄位置
# [變數] LIB_PATH        => lib 目錄位置
# [變數] INTENT_PATH     => intent 目錄位置
# [變數] REPLY_PATH      => reply 目錄位置
# [變數] ACCOUNT_DICT    => account.info 內容
# [變數] ARTICUT         => ArticutAPI (用法：ARTICUT.parse()。 #需安裝 ArticutAPI.)
# """

# sys.path.pop(-1)

# userDefinedDICT = {}
# try:
#     userDefinedDICT = json.load(open(os.path.join(CWD_PATH, "USER_DEFINED.json"), encoding="utf-8"))
# except:
#     pass

# replyDICT = {}
# replyPathSTR = os.path.join(REPLY_PATH, "reply_{}.json".format(INTENT_NAME))
# if os.path.exists(replyPathSTR):
#     try:
#         replyDICT = json.load(open(replyPathSTR, encoding="utf-8"))
#     except Exception as e:
#         print("[ERROR] reply_{}.json => {}".format(INTENT_NAME, str(e)))
# CHATBOT = True if replyDICT else False

# # 將符合句型的參數列表印出。這是 debug 或是開發用的。
# def debugInfo(inputSTR, utterance):
#     if ACCOUNT_DICT["debug"]:
#         print("[{}] {} ===> {}".format(INTENT_NAME, inputSTR, utterance))

# def getReply(utterance, args):
#     try:
#         replySTR = (replyDICT[utterance], 1)[0].format(*args)
#     except:
#         replySTR = ""

#     return replySTR

# def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
#     debugInfo(inputSTR, utterance)
#     if utterance == "[心理所][榜單][差不多]在什麼[時候]公布":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]有哪些[科目]要考":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]有哪些考試[科目]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]甄試[大約]在[每年]的[幾月]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]甄試[時間]落在[每年]的[幾月份]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]甄試在[每年幾月]開始":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]甄試在[每年幾月份]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]甄試的[時間][大約]在[幾月份]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]的[榜單][會]在什麼[時候]公布":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]的[榜單]什麼[時候][會]公布":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]的考試[科目]有哪些":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     if utterance == "[心理所]要考哪些[科目]":
#         if CHATBOT:
#             replySTR = getReply(utterance, args)
#             if replySTR:
#                 resultDICT["response"] = replySTR
#                 resultDICT["source"] = "reply"
#         else:
#             # write your code here
#             # resultDICT[key].append(value)
#             pass

#     return resultDICT


# if __name__ == "__main__":
#     from pprint import pprint

#     resultDICT = getResult("心理所要考哪些科目", "[心理所]要考哪些[科目]", [], {}, {})
#     pprint(resultDICT)