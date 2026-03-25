# 翻翻君（FanFan）翻譯機器人

模組化 LINE 翻譯機器人，支援 Railway 部署與未來功能擴充。

## 功能

1. 中文介面語言選單（中文、英文、泰文、越南文、印尼文、日文、俄文）
2. 好友加入自動綁定個人編號（格式：`FAN000001`）
3. 群組設定權限控管：僅群組邀請者（以首次綁定者認定）與程式所有者/管理員可設定

## LINE 指令（全中文）

- `主選單` / `功能選單` / `選單小卡`：顯示功能小卡選單
- `語言設定` / `語言選單` / `選單`：開啟語言快速選單
- `指令說明` / `使用說明` / `幫助`：顯示機器人指令說明
- `設定語言 中文`（個人）：切換個人翻譯語言
- `設定語言 中文`（群組）：加上/取消該語言（可複選）
- `設定語言 中文、泰文`（群組）：一次指定多語翻譯清單
- `重設翻譯設定`（群組）：重設為僅中文
- `綁定邀請者`：群組首次綁定邀請者代表

### 管理員白名單指令（僅邀請者代表/管理員/所有者）

- `查看群組設定`：查看本群語言與邀請者代表
- `重設邀請者`：把邀請者代表重設為目前發指令的人

## 群組多語翻譯規則

- 群組可同時設定多種目標語言（例如：中文、泰文）
- 設定完成後，群組每一句訊息都會回覆所有已勾選語言
- 語言快捷按鈕可重複點擊：已選語言會取消，未選語言會加入
- 輸入 `語言設定` 會開啟彩色語言設定小卡，卡片上可看到目前勾選狀態

## 專案結構

```text
app/
  bot/                 # LINE 事件處理
  core/                # 設定與常數
  db/                  # 資料庫連線與模型
  repositories/        # 資料存取層
  services/            # 商業邏輯層
  ui/                  # 選單與訊息格式
  main.py              # FastAPI 入口
```

## 本機啟動

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## Railway 部署

1. 專案推到 GitHub
2. Railway 建立新專案並連結 GitHub Repo
3. 設定環境變數：
  - `LINE_CHANNEL_ACCESS_TOKEN`（也相容你目前的 `CHANNEL_ACCESS_TOKEN`）
  - `LINE_CHANNEL_SECRET`（也相容你目前的 `CHANNEL_SECRET`）
  - `DEEPL_API_KEY`
   - `APP_OWNER_USER_IDS`
  - `DATABASE_URL`（請使用 Railway Postgres 的 `DATABASE_URL` 變數參照）
4. Deploy 後把 `https://你的網址/webhook/line` 設為 LINE Webhook URL

### LINE 沒反應時優先檢查

- Railway 是否已有 `CHANNEL_ACCESS_TOKEN` / `CHANNEL_SECRET` 或 `LINE_CHANNEL_ACCESS_TOKEN` / `LINE_CHANNEL_SECRET`
- 是否已設定 `DATABASE_URL`
- 是否已設定 `DEEPL_API_KEY`
- LINE Developers 的 Webhook URL 是否指向 `https://你的網域/webhook/line`
- LINE Official Account Manager 是否已開啟 Webhook
- 現在支援 `/選單`、`/主選單`、`/指令說明` 這類斜線輸入

### Railway 資料庫連線重點

- 本專案會在啟動時自動建表（`user_profiles`、`group_settings`）
- 支援 Railway 常見連線格式：`postgres://...` 或 `postgresql://...`
- 系統會自動轉為 SQLAlchemy 可用格式並補上 `sslmode=require`

## 管理員初始化（你剛需要的功能）

### 本機指令

```bash
python tools/admin_manager.py 升級管理員 --使用者ID Uxxxxxxxx --自動建立
python tools/admin_manager.py 升級管理員 --編號 FAN000001
python tools/admin_manager.py 取消管理員 --編號 FAN000001
python tools/admin_manager.py 查詢使用者 --編號 FAN000001
python tools/admin_manager.py 列出管理員
```

### Railway 一次性執行（推薦）

在 Railway 的 App 服務開啟 Shell 後執行：

```bash
python tools/admin_manager.py 升級管理員 --使用者ID Uxxxxxxxx --自動建立
```

說明：

- `--使用者ID`：用 LINE User ID 指定對象
- `--編號`：用 FAN 編號指定對象
- `--自動建立`：若該 LINE ID 尚未建立資料，會自動建立並升為管理員

## 群組權限規則說明

LINE API 不會直接提供「邀請機器人的那位使用者」ID，因此本系統採以下可操作方案：

- 機器人進群後，第一位在群組輸入 `綁定邀請者` 的人會被記錄為該群「邀請者代表」
- 只有該使用者、全域管理員與所有者可執行群組設定

這個設計可穩定落地，也方便未來擴充多角色管理。
