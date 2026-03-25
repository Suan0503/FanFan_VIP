# 🚀 快速開始指南（會員版）

本版本以會員管理為主，指令已全面中文化，並且預設啟用資料庫。

## 1) 安裝與啟動

### 安裝套件
```bash
pip install -r requirements.txt
```

### 環境變數（建議）
```env
CHANNEL_ACCESS_TOKEN=your_line_channel_token
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_token
ADMIN_TOKEN=your_admin_token
DATABASE_URL=postgresql://user:pass@host:5432/dbname
PORT=5000
```

說明：
- 若未設定 `DATABASE_URL`，系統會自動使用本機 SQLite：`instance/fanfan_vip.db`
- `CHANNEL_ACCESS_TOKEN` 與 `LINE_CHANNEL_ACCESS_TOKEN` 兩者擇一即可

### 啟動服務
```bash
python main.py
```

## 2) 使用者指令（中文、明確）

| 指令 | 功能 |
|------|------|
| `/主選單` | 顯示會員中心與可用操作 |
| `/我的會員` | 查看會員狀態與到期時間 |
| `/兌換序號 FANVIPXXXXXXXXXX` | 啟用或續期會員 |
| 直接貼上 `FANVIPXXXXXXXXXX` | 等同兌換序號 |

## 3) 管理者指令（主人）

| 指令 | 功能 |
|------|------|
| `/產生序號 5 30天` | 建立 5 組 30 天啟用序號 |
| `/序號 5 30天` | 舊指令相容寫法 |

補充：
- 使用 `/產生序號 數量 天數` 格式，例如 `/產生序號 10 7天`

## 4) 常見流程

### 新用戶啟用
1. 輸入 `/主選單`
2. 輸入 `/兌換序號 FANVIPXXXXXXXXXX`
3. 輸入 `/我的會員` 確認到期時間

### 會員續期
1. 貼上新序號（或輸入 `/兌換序號 ...`）
2. 系統會自動往後延長有效時間

## 5) 管理 API（需 ADMIN_TOKEN）

- `POST /admin/generate_codes`
- `GET /admin/codes`
- `GET /admin/export_codes`
- `POST /admin/run_expiry_check`

HTTP Header 需帶：
```text
X-Admin-Token: <你的 ADMIN_TOKEN>
```

---

如要擴充下一步（例如：多層級會員方案、後台管理頁），建議先保持上述指令不變，再新增功能。
