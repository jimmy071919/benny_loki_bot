#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
名稱： Loki 意圖更新工具 3.0
作者： Droidtown
日期： 2022-06-13
信箱： info@droidtown.co

功能說明：
此工具用於更新 Loki 意圖檔案，主要功能包括：
1. 更新現有意圖檔案中的句型（Utterance）
2. 更新使用者自定義詞典（UserDefined）
3. 自動備份更新前的檔案
4. 處理新增的意圖檔案

使用方法：
Updater.py <new_intent_dir>

處理流程：
1. 備份現有的意圖檔案到 backup_{timestamp} 目錄
2. 更新句型和使用者自定義詞典
3. 處理新增的意圖檔案
4. 提示使用者在 Project.py 中加入必要的程式碼

注意事項：
- 新增的 Loki 意圖檔需要在 Project.py 的 runLoki() 中加入呼叫程式碼
- 建議在更新前先備份重要檔案
"""

from Account import *
"""
Account 模組變數說明：
[變數] BASE_PATH    - 專案根目錄位置
[變數] LIB_PATH     - 函式庫目錄位置
[變數] INTENT_PATH  - 意圖檔案目錄位置
[變數] REPLY_PATH   - 回覆檔案目錄位置
[變數] ACCOUNT_DICT - account.info 設定內容
[變數] ARTICUT      - ArticutAPI 實例（需安裝 ArticutAPI 並有效的 username, api_key）
"""

from argparse import ArgumentParser
from datetime import datetime
from shutil import copyfile
import os
import re

# 時間戳記，用於備份檔案
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d%H%M%S")
BACKUP_FOLDER = "backup_{}".format(TIMESTAMP)
USER_DEFINED_FILE = "USER_DEFINED.json"

# 檔案匹配模式
intentFilePAT = re.compile("^Loki_.+(?<!_updated)\.py$")  # 排除 1.0 版本產生的 _updated.py 檔案
intentFileNamePAT = re.compile("^Loki_(.+)\.py$")
utterancePAT = re.compile("if utterance == \".+\":$")
userDefinedPAT = re.compile("userDefinedDICT = (\{.*\})$")
endResultPAT = re.compile("^    return resultDICT$")

def updateUtterance(newIntentPath):
    """
    更新意圖檔案中的句型（Utterance）
    
    參數：
        newIntentPath (str): 新意圖檔案的目錄路徑
    
    功能：
    1. 掃描新目錄中的所有意圖檔案
    2. 對每個意圖檔案：
       - 如果檔案已存在：更新其中的句型
       - 如果是新檔案：直接複製到目標目錄
    3. 自動備份原有檔案
    
    返回：
        bool: 更新是否成功
    """
    # 取得目前目錄下的意圖檔案
    intentFileLIST = sorted([f for f in os.listdir(newIntentPath) if intentFilePAT.search(f)])
    for intentFile in intentFileLIST:
        filePath = os.path.join(INTENT_PATH, intentFile)
        if os.path.exists(filePath):
            print("\n[{}]".format(intentFile))

            # 取出舊意圖檔案的所有內容
            sourceLIST = []
            with open(filePath, encoding="utf-8") as f:
                sourceLIST = f.readlines()

            # 移除結尾空白列
            while sourceLIST[-1] == "\n":
                sourceLIST = sourceLIST[:-1]

            # 取出舊意圖檔案中的句型
            intentLIST = []
            for source in sourceLIST:
                for g in utterancePAT.finditer(source):
                    intentLIST.append(g.group())

            # 取出新意圖檔案中的句型
            newIntentLIST = []
            with open(os.path.join(newIntentPath, intentFile), encoding="utf-8") as f:
                lineLIST = f.readlines()
                for line in lineLIST:
                    for g in utterancePAT.finditer(line):
                        newIntentLIST.append(g.group())

            # 新意圖檔案中的句型不存在於舊意圖檔案中才更新
            updatedBOOL = False
            for newIntent in newIntentLIST:
                if newIntent not in intentLIST:
                    indexLIST = [i for i, source in enumerate(sourceLIST) if utterancePAT.search(source)]
                    if indexLIST:
                        indexINT = indexLIST[-1]
                    else:
                        indexLIST = [i for i, source in enumerate(sourceLIST) if endResultPAT.search(source)]
                        indexINT = indexLIST[-1]

                    sourceLIST.insert(indexINT, """    {}
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

""".format(newIntent))

                    updatedBOOL = True
                    print("=> 新增 {}".format(newIntent))

            if updatedBOOL:
                try:
                    # 備份意圖檔案
                    copyfile(filePath, os.path.join(INTENT_PATH, BACKUP_FOLDER, intentFile))
                    try:
                        # 更新意圖檔案
                        f = open(filePath, "w", encoding="utf-8")
                        f.write("".join(sourceLIST))
                        f.close()
                        print("=> 更新成功")
                    except Exception as e:
                        print("=> 更新失敗 {}".format(str(e)))
                except Exception as e:
                    print("=> 備份失敗 {}".format(str(e)))
            else:
                print("=> 沒有新句型")

        else:
            # 新意圖檔案直接複製
            print("\n[新增 {}]".format(intentFile))
            try:
                copyfile(os.path.join(newIntentPath, intentFile), os.path.join(INTENT_PATH, intentFile))
                intentNameSTR = intentFileNamePAT.findall(intentFile)[0]
                print("=> 請在 Project.py 中加入以下的程式碼")
                print("from intent import Loki_{}\n".format(intentNameSTR))
                print("def runLoki(...):")
                print("    # {}".format(intentNameSTR))
                print("    if lokiRst.getIntent(index, resultIndex) == \"{}\":".format(intentNameSTR))
                print("        lokiResultDICT = Loki_{}.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT, pattern=lokiRst.getPattern(index, resultIndex), toolkitDICT=toolkitDICT)".format(intentNameSTR))
            except Exception as e:
                print("=> 新增失敗 {}".format(str(e)))

    return True

def updateUserDefined(newIntentPath):
    """
    更新使用者自定義詞典（UserDefined）
    
    參數：
        newIntentPath (str): 新意圖檔案的目錄路徑
    
    功能：
    1. 支援兩種格式：
       - 2.0 版本：使用獨立的 USER_DEFINED.json 檔案
       - 1.0 版本：從意圖檔案中提取 userDefinedDICT
    2. 自動備份原有檔案
    3. 更新所有意圖檔案中的使用者自定義詞典
    
    返回：
        bool: 更新是否成功
    """
    if os.path.exists(os.path.join(newIntentPath, USER_DEFINED_FILE)):
        # 2.0 使用 USER_DEFINED.json
        print("\n[{}]".format(USER_DEFINED_FILE))
        # 備份 UserDefined
        try:
            copyfile(os.path.join(INTENT_PATH, USER_DEFINED_FILE), os.path.join(INTENT_PATH, BACKUP_FOLDER, USER_DEFINED_FILE))
        except Exception as e:
            print("=> 備份失敗 {}".format(str(e)))
            return False

        # 更新 UserDefined
        try:
            copyfile(os.path.join(newIntentPath, USER_DEFINED_FILE), os.path.join(INTENT_PATH, USER_DEFINED_FILE))
            print("=> 更新成功")
        except Exception as e:
            print("=> 更新失敗 {}".format(str(e)))
            return False
    else:
        # 1.0 使用意圖檔案內的 userDefinedDICT
        # 取得目前目錄下的意圖檔案
        intentFileLIST = sorted([f for f in os.listdir(INTENT_PATH) if intentFilePAT.search(f)])

        # 讀取 UserDefined
        userDefinedSTR = ""
        for intentFile in intentFileLIST:
            if os.path.exists(os.path.join(newIntentPath, intentFile)):
                flagBOOL = False
                with open(os.path.join(newIntentPath, intentFile), encoding="utf-8") as f:
                    lineLIST = f.readlines()
                    for line in lineLIST:
                        for g in userDefinedPAT.finditer(line):
                            try:
                                userDefinedSTR = line
                                flagBOOL = False
                                break
                            except:
                                pass

                if flagBOOL:
                    break

        # 更新所有意圖檔案的 userDefinedDICT
        for intentFile in intentFileLIST:
            print("\n[{}]".format(intentFile))

            # 取出舊意圖檔案的所有內容
            sourceLIST = []
            with open(os.path.join(INTENT_PATH, intentFile), encoding="utf-8") as f:
                sourceLIST = f.readlines()

            # 更新 UserDefined
            for i, source in enumerate(sourceLIST):
                if userDefinedPAT.search(source):
                    sourceLIST[i] = userDefinedSTR
                    break

            # 備份意圖檔案
            if not os.path.exists(os.path.join(INTENT_PATH, BACKUP_FOLDER, intentFile)):
                try:
                    copyfile(os.path.join(INTENT_PATH, intentFile), os.path.join(INTENT_PATH, BACKUP_FOLDER, intentFile))
                except Exception as e:
                    print("=> 備份失敗 {}".format(str(e)))
                    continue

            try:
                # 更新意圖檔案
                f = open(os.path.join(INTENT_PATH, intentFile), "w", encoding="utf-8")
                f.write("".join(sourceLIST))
                f.close()
                print("=> 更新成功")
            except Exception as e:
                print("=> 更新失敗 {}".format(str(e)))

    return True

if __name__ == "__main__":
    progSTR = "Loki 意圖更新工具 3.0"
    usageSTR = "\nUpdater.py <new_intent_dir>"
    descriptionSTR = """
    Loki 意圖更新工具 3.0 會將新目錄 (new_intent_dir) 中的 Utterance 及 UserDefined 更新至現在目錄中的 Loki 意圖檔 (Loki_{intent}.py)，
    並自動備份更新前的 Loki 圖檔至 backup_{timestamp} 目錄中。

    注意：新增的 Loki 意圖檔需要使用者至 Project.py 中加入呼叫程式碼！
    """
    argParser = ArgumentParser(prog=progSTR, usage=usageSTR, description=descriptionSTR, epilog=None)
    # Updater 1.0
    argParser.add_argument("-o", "--old-intent-dir", required=False, help="Old intent(s) directory", dest="oldIntentDirectory")
    argParser.add_argument("-n", "--new-intent-dir", required=False, help="New intent(s) directory", dest="newIntentDirectory")
    # Updater 2.0
    argParser.add_argument("new_intent_dir", nargs="?", default="", help="New intent directory")
    args = argParser.parse_args()

    newIntentPath = None
    if args.new_intent_dir:
        newIntentPath = args.new_intent_dir
    if args.newIntentDirectory:
        newIntentPath = args.newIntentDirectory

    if newIntentPath:
        if os.path.exists(newIntentPath):
            # 取得新目錄完整路徑
            newIntentPath = os.path.abspath(newIntentPath)
            if os.path.isdir(newIntentPath):
                print("新 Intent 目錄 {}".format(newIntentPath))
                # 建立備份資料夾
                os.mkdir(os.path.join(INTENT_PATH, BACKUP_FOLDER))
                print("備份目錄 {}".format(os.path.join(INTENT_PATH, BACKUP_FOLDER)))
                print("\n--------------------")

                # 檢查 Utterance
                print("\n[1] 檢查 Utterance")
                updateUtterance(newIntentPath)
                print("\n--------------------")

                # 檢查 UserDefined
                print("\n[2] 檢查 UserDefined")
                updateUserDefined(newIntentPath)

                print("\n--------------------\n\n作業完成")
            else:
                print("{} 不是有效的目錄".format(newIntentPath))
        else:
            print("{} 不是有效的路徑".format(newIntentPath))
    else:
        argParser.print_help()