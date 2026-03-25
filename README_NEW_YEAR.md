# 🎊 FanFan LINE Bot - 新年版

> 🧧 恭喜發財 萬事如意 🧧

一個功能強大的 LINE 翻譯機器人，現已升級為新年風格並支援功能分級管理！

## ✨ 最新更新 (2026-01-08)

### 🎨 新年風格選單
- 全新紅金配色主題
- 節慶祝福語整合
- 溫馨的用戶體驗

### 🔧 功能開關系統
- 支援 5 種功能獨立控制
- 每個群組唯一 TOKEN
- 適合對外販售功能分級

## 🌟 核心功能

### 翻譯功能
- 🌍 支援 9 種語言即時翻譯
- 🤖 自動翻譯模式
- 🎤 語音翻譯支援
- 🔄 Google + DeepL 雙引擎

### 管理功能
- 👥 群組管理員系統
- 📊 使用統計分析
- 🎛️ 功能開關控制
- 🔑 TOKEN 認證系統

### 新年特色
- 🎊 節慶主題選單
- 🧧 新春祝福語
- 🏮 喜慶配色設計

## 🎯 支援語言

| 語言 | 代碼 | 圖示 |
|------|------|------|
| 繁體中文 | zh-TW | 🇹🇼 |
| 英文 | en | 🇺🇸 |
| 日文 | ja | 🇯🇵 |
| 韓文 | ko | 🇰🇷 |
| 泰文 | th | 🇹🇭 |
| 越南文 | vi | 🇻🇳 |
| 印尼文 | id | 🇮🇩 |
| 緬甸文 | my | 🇲🇲 |
| 俄文 | ru | 🇷🇺 |

## 📋 功能開關清單

| 功能 | 代碼 | 說明 |
|------|------|------|
| 翻譯功能 | `translate` | 基本翻譯功能 |
| 語音翻譯 | `voice` | 語音訊息翻譯 |
| 管理功能 | `admin` | 管理相關功能 |
| 自動翻譯 | `auto_translate` | 自動翻譯模式 |
| 統計功能 | `statistics` | 使用統計查詢 |

## 🚀 快速開始

### 安裝需求
```bash
pip install -r requirements.txt
```

### 環境設定
在 `.env` 檔案中設定（建議）：
```env
CHANNEL_ACCESS_TOKEN=your_line_channel_token
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_token
CHANNEL_SECRET=your_line_channel_secret
ADMIN_TOKEN=your_admin_token
DATABASE_URL=postgresql://user:pass@host:5432/dbname
PORT=5000
```

資料庫說明：
- 若未設定 `DATABASE_URL`，系統會自動改用本機 SQLite（`instance/fanfan_vip.db`）
- 若有設定 `DATABASE_URL`，會優先使用 PostgreSQL

### 啟動服務
```bash
python main.py
```

## 💡 使用指南

### 基本指令

#### 用戶指令
```
/主選單                       - 顯示會員中心與可用操作
/我的會員                     - 查看會員狀態與到期時間
/兌換序號 FANVIPXXXXXXXXXX    - 啟用或續期會員
直接貼上 FANVIPXXXXXXXXXX      - 等同兌換序號
```

#### 管理者指令（僅主人）
```
/產生序號 5 30天              - 產生 5 組 30 天序號
/序號 5 30天                  - 舊寫法相容
```

#### 管理 API（需 ADMIN_TOKEN）
```
POST /admin/generate_codes
GET  /admin/codes
GET  /admin/export_codes
POST /admin/run_expiry_check
```

### 使用範例

#### 新用戶啟用流程
1. 在 LINE 輸入 `/主選單`
2. 輸入 `/兌換序號 FANVIPXXXXXXXXXX`
3. 輸入 `/我的會員` 確認到期時間

#### 管理者發序號流程
```bash
/產生序號 10 30天
```

系統會回覆可直接使用的序號清單。

## 🎁 商業方案建議

### 免費版
- ✅ 基本翻譯
- ✅ 自動翻譯
- ❌ 語音翻譯
- ❌ 統計功能
- **適合**: 個人用戶、試用

### 標準版 (NT$ 299/月)
- ✅ 基本翻譯
- ✅ 自動翻譯
- ✅ 語音翻譯
- ✅ 統計功能
- **適合**: 小型團隊、商務用戶

### 專業版 (NT$ 599/月)
- ✅ 所有功能
- ✅ 優先支援
- ✅ 客製化設定
- **適合**: 企業用戶、大型團隊

## 📚 文件導覽

- [功能控制指南](FEATURE_CONTROL_GUIDE.md) - 完整功能說明
- [快速開始](QUICK_START.md) - 快速上手指南
- [更新總結](UPDATE_SUMMARY.md) - 更新內容詳情
- [功能對比](COMPARISON.md) - 新舊版本對比

## 🔐 安全性

- 🔑 每個群組擁有唯一 TOKEN
- 👮 分級權限管理
- 💾 資料本地儲存
- 🛡️ 自動清理機制（20天未使用自動退出）

## 🛠️ 技術架構

### 核心技術
- **框架**: Flask
- **LINE API**: linebot-sdk-python
- **資料庫**: SQLAlchemy (支援 PostgreSQL/SQLite)
- **翻譯引擎**: Google Translate + DeepL API

### 資料結構
```python
{
  "user_whitelist": [],
  "user_prefs": {},
  "voice_translation": {},
  "group_admin": {},
  "translate_engine_pref": {},
  "feature_switches": {
    "GROUP_ID": {
      "features": ["translate", "voice", ...],
      "token": "unique_token",
      "created_at": "2026-01-08T..."
    }
  }
}
```

## 📊 系統特色

### 效能優化
- ⚡ 非同步翻譯處理
- 🧵 多執行緒架構
- 💾 智慧記憶體管理
- 🔄 自動重啟機制

### 用戶體驗
- 🎨 新年主題設計
- 📱 響應式選單
- 💬 友善錯誤提示
- 🌈 多語言支援

## 🐛 除錯模式

查看系統狀態：
```
/狀態    - 運行時間、翻譯次數
/記憶體  - 記憶體使用狀況
/流量    - 今日字元數統計
```

## 📝 開發計畫

### 已完成 ✅
- [x] 新年風格選單
- [x] 功能開關系統
- [x] TOKEN 認證機制
- [x] 多引擎翻譯支援
- [x] 群組管理功能

### 規劃中 🚧
- [ ] Web 管理後台
- [ ] 付費系統整合
- [ ] API 端點擴展
- [ ] 使用量分析儀表板
- [ ] 自訂回應功能

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

本專案採用 MIT 授權條款

## 🎊 致謝

感謝所有使用者的支持與反饋！

---

**🧧 祝您新年快樂，生意興隆！🧧**

*Made with ❤️ in Taiwan*
