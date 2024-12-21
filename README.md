# 中正大學心理系助理機器人

這是一個基於 Discord 的聊天機器人，專門為中正大學心理系師生設計。機器人能夠回答關於教授研究專長、課程資訊等常見問題。

## 功能特色

### 1. 教授資訊查詢

- 查詢教授研究專長
- 依據研究領域查找教授
- 查詢教授電子郵件

### 2. 課程資訊查詢

- 查詢課程活動
- 查詢考試資訊
- 查詢選課相關資訊

### 3. 自然語言處理

- 使用 Droidtown 的 Articut API 進行中文語意解析
- 支援多種問句模式
- 智慧匹配最相關的回答

## 安裝說明

### 環境需求

- Python 3.8 或以上版本
- pip 套件管理器

### 安裝步驟

1. 複製專案

```bash
git clone [專案網址]
cd benny_loki_bot
```

2. 安裝相依套件

```bash
pip install -r requirements.txt
```

3. 設定環境變數

- 複製 `.env.example` 為 `.env`
- 填入必要的設定值：
  - Discord Bot Token
  - Droidtown API 相關憑證
  - 其他系統設定

4. 啟動機器人

```bash
python DC_bot.py
```

## 使用說明

### 基本指令

- `[教授名稱]的研究專長是什麼？`
- `[領域]有哪些教授？`
- `[教授]的email是什麼？`

### 範例對話

- 問：「姜定宇教授有哪些研究專長？」
- 答：「姜定宇教授的研究專長包括：
  1. 華人組織行為
  2. 華人領導
  3. 主管忠誠與組織忠誠
  4. 組織正義」

## 系統架構

### 主要元件

- `DC_bot.py`：Discord 機器人主程式
- `lib/`：核心功能庫
- `intent/`：意圖判斷模組
- `reply/`：回覆模板
- `data/`：資料檔案

### 技術框架

- Discord.py：Discord 機器人框架
- ArticutAPI：中文自然語言處理
- pandas：資料處理
- python-dotenv：環境變數管理

## 重要設定檔說明

### 環境變數設定 (.env)

1. 複製 `.env.example` 為 `.env`
2. 必須修改的設定：
   - `Loki_Account`：您的 Loki 帳號
   - `Loki_key`：您的 Loki 密鑰
   - `DISCORD_TOKEN`：您的 Discord Bot Token
   - `DROIDTOWN_USERNAME`：您的 Droidtown 帳號
   - `DROIDTOWN_API_KEY`：您的 Droidtown API 密鑰
   - `DROIDTOWN_LOKI_KEY`：您的 LOKI 密鑰
   - `DROIDTOWN_COPYTOASTER_KEY`：您的 COPYTOASTER 密鑰

### 帳號資訊設定 (account.info)

1. 複製 `account.info.example` 為 `account.info`
2. 填入您的個人設定：
   - Loki 相關設定
   - Articut API 設定
   - 其他系統設定

⚠️ **重要提醒**

- 這些檔案包含敏感資訊，請勿上傳至公開的程式碼庫
- 必須完成以上設定，機器人才能正常運作
- 請妥善保管您的 API 金鑰和權杖
- 建議定期更新密鑰以確保安全性

## 開發說明

### 新增功能流程

1. 在 `intent/` 資料夾中新增意圖判斷檔案
2. 在 `reply/` 資料夾中新增對應的回覆模板
3. 在 `data/` 資料夾中新增必要的資料檔案
4. 更新 `Project.py` 中的路由設定

### 程式碼風格

- 使用 PEP 8 程式碼風格指南
- 保持一致的命名規範
- 添加適當的註釋和文件字串

## 注意事項

- 請勿將敏感資訊（如 API 金鑰）直接寫在程式碼中
- 定期備份資料檔案
- 遵守 Discord API 使用規範

## 授權資訊

本專案採用 MIT 授權條款

## 聯絡資訊

如有任何問題或建議，請聯繫：jimmy071919@gmail.com

## Railway 部署說明

### 環境變數設定
在 Railway 上部署時，您需要在專案的 Variables 頁面中設定以下環境變數：

1. 基本設定：
   - `Loki_Account`
   - `Loki_key`
   - `DISCORD_TOKEN`
   - `DROIDTOWN_USERNAME`
   - `DROIDTOWN_API_KEY`
   - `DROIDTOWN_LOKI_KEY`
   - `DROIDTOWN_COPYTOASTER_KEY`
   - `DEBUG_MODE`
   - `CHATBOT_MODE`

2. LLM 設定：
   - `LLM_SYSTEM_PROMPT`
   - `LLM_ASSISTANT_PROMPT`
   - `LLM_USER_PROMPT`

### 部署步驟

1. 在 Railway 建立新專案
2. 連接 GitHub 倉庫
3. 在 Variables 頁面設定所有環境變數
4. 設定啟動命令為 `python DC_bot.py`

### 注意事項

- Railway 的環境變數會自動替代本地的 `.env` 檔案
- 不需要上傳 `.env` 和 `account.info` 到 Git 倉庫
- 建議在本地開發時使用 `.env`，部署時使用 Railway 的環境變數
- 記得在 Railway 的 Variables 中設定所有必要的環境變數
