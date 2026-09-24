# 🤖 FanFan VIP - Google Gemini AI 集成指南

## 📖 目錄

1. [功能概述](#功能概述)
2. [環境變量配置](#環境變量配置)
3. [安裝依賴](#安裝依賴)
4. [數據庫遷移](#數據庫遷移)
5. [用戶指令](#用戶指令)
6. [額度管理](#額度管理)
7. [故障排查](#故障排查)

---

## 功能概述

### ✨ AI 對話功能

**FanFan VIP** 現已集成 **Google Gemini AI**，為用戶提供智慧對話能力。

**主要功能：**
- 🤖 自然語言對話（由 Gemini-2.0-Flash 支援）
- 💬 多輪對話上下文記憶（支持7天自動過期）
- 📝 知識檢索、文稿撰寫、創意生成
- 🌍 多語言支持（中文、英文等）
- 👑 VIP 用戶無限對話 vs 免費用戶每日10次

**架構：**
```
User Input (LINE Chat)
    ↓
Gemini API (google-generativeai)
    ↓
Conversation History (SQLite/PostgreSQL)
    ↓
Response + Usage Log
```

---

## 環境變量配置

### 第1步：申請 Gemini API Key

1. 打開 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 點擊 **「Create API Key」**
3. 選擇現有項目或新建項目
4. 複製生成的 API Key

> **📌 免費額度限制：**
> - 每分鐘最多 60 個請求
> - 每月最多 1,500 個請求
> - 完全免費，無需綁定信用卡

### 第2步：更新 .env 文件

```bash
# 複製 .env.example 為 .env（如果還沒有）
cp .env.example .env
```

編輯 `.env` 並添加：

```env
# Google Gemini AI 配置（免費額度）
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# AI 對話每日限制
AI_FREE_DAILY_LIMIT=10          # 免費用戶每日最多10次對話
AI_VIP_DAILY_LIMIT=100          # VIP用戶每日最多100次對話
```

---

## 安裝依賴

```bash
# 1. 進入項目目錄
cd FanFan_VIP

# 2. 激活虛擬環境
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# 3. 升級 pip
pip install --upgrade pip

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 驗證安裝
python -c "import google.generativeai as genai; print('✅ Gemini API installed successfully')"
```

---

## 數據庫遷移

新增的表會在首次啟動時自動建立：

```
ai_conversations   # AI 對話紀錄
ai_messages        # 對話消息記錄
ai_usage_logs      # AI 使用日誌統計
```

啟動應用時，這些表會自動建立：

```bash
# 本機啟動
uvicorn app.main:app --reload

# Railway 部署
git push railway main
```

---

## 用戶指令

### 🚀 啟動 AI 對話

| 指令 | 功能 | 備註 |
|------|------|------|
| `/ai` | 打開 AI 助手菜單 | 顯示功能介紹和快速按鈕 |
| `/ai開始` 或 `/ai start` | 開始新對話 | 進入 AI 對話模式 |
| `/ai歷史` 或 `/ai history` | 查看對話歷史 | 顯示最近5個對話 |
| `/ai統計` 或 `/ai stats` | 查看使用統計 | 7天內的使用數據 |
| `/返回` 或 `/back` | 返回翻譯模式 | 退出 AI 對話模式 |

### 💬 對話流程

```
用戶: /ai開始
FanFan: ✨ 新對話已開始
        ID: conv_abc123...
        現在輸入你的問題，我會直接回答（不翻譯）。
        💡 說 /返回 或 /回到翻譯 可以回到翻譯模式。

用戶: 什麼是人工智能？
FanFan: [顯示 Gemini 回答]
        今日使用: 1/10
        🔋

用戶: 它在現代社會的應用是什麼？
FanFan: [Gemini 根據上下文回答，記得前一個問題]

用戶: /返回
FanFan: ✅ 已返回翻譯模式
        現在輸入文字會直接進行翻譯。
```

---

## 額度管理

### 免費用戶

- **每日限制**：10 次對話
- **重置時間**：每天 UTC 00:00
- **升級提示**：當使用次數 > 5 時，會提示升級 VIP

### VIP 用戶

- **每日限制**：100 次對話（可在 AI_VIP_DAILY_LIMIT 調整）
- **額度計費**：
  - AI 對話 = 回應字符數
  - 翻譯 = 待翻譯字符數
  - **兩者分開計算，不互相影響**
- **優先級**：Azure Translator > Gemini AI

### 查詢額度

```bash
# 查看今日使用次數
用戶輸入: /ai統計

返回:
📊 AI 使用統計（最近7天）
📝 總查詢數：15
✅ 成功回應：15
👑 VIP對話：0
🆓 免費對話：15
```

---

## 對話數據保留

### 自動清理

- **過期時間**：7天
- **清理方式**：
  - 對話 (ai_conversations)
  - 相關消息 (ai_messages)
  - 自動刪除
- **保留日誌**：使用統計日誌 (ai_usage_logs) 永久保留

### 手動清理（可選）

```python
from app.services.ai_service import ai_service
deleted_count = ai_service.clear_expired_conversations()
print(f"Deleted {deleted_count} expired conversations")
```

---

## 故障排查

### ❌ 無法連接 Gemini API

**症狀**：「❌ AI 服務暫時不可用」

**檢查項目：**
```bash
# 1. 驗證 API Key
echo $GEMINI_API_KEY  # 應該輸出你的 API Key

# 2. 測試 API 連接
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_API_KEY')
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content('test')
print(response.text)
"

# 3. 檢查網路連接
ping aistudio.google.com
```

**解決方案：**
- ✅ 確保 GEMINI_API_KEY 正確設定
- ✅ 檢查 API 配額是否超限
- ✅ 確認網路連接正常
- ✅ 重啟應用：`uvicorn app.main:app --reload`

---

### ❌ 「daily_limit_exceeded」錯誤

**症狀**：用戶達到每日限制

**回應示例：**
```
❌ 今日對話次數已達限制（10/10）
✨ 升級 VIP 可享受無限對話
```

**解決方案：**
- ✅ 等待 UTC 00:00 配額重置
- ✅ 升級為 VIP 用戶（如果已實裝支付）

---

### ❌ 對話歷史丟失

**症狀**：重啟後對話歷史消失

**原因**：
- 全局 `AI對話上下文` 存在記憶體中
- 只有數據庫中的數據會持久化

**解決方案**（可選）：
```python
# 改用 Redis 持久化（適合生產環境）
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.set(f"ai:{user_id}", conversation_id, ex=86400)  # 24小時過期
```

---

### ❌ 返回「內容政策違規」

**症狀**：Gemini 拒絕生成內容

**原因**：
- 查詢包含暴力、仇恨言論
- 成人內容
- 非法活動

**回應示例：**
```
❌ 無法生成回應
（由於安全設定，此查詢被系統拒絕）
```

**解決方案**：
- ✅ 修改查詢內容，避免敏感話題
- ✅ 詳見 Gemini [安全設定文檔](https://ai.google.dev/safety-settings)

---

## 性能優化建議

### 1️⃣ 緩存頻繁查詢

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_conversation(conversation_id: str):
    # 緩存對話查詢
    return db.query(AIConversation).filter(...).first()
```

### 2️⃣ 異步處理

```python
import asyncio

async def ai_chat_async(user_id, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ai_service.chat, user_id, query)
```

### 3️⃣ 使用數據庫連接池

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)
```

---

## 支援的語言

| 語言 | 代碼 | 系統提示 |
|------|------|--------|
| 繁體中文 | `zh-TW` | 中文 AI 助手 |
| 英文 | `en` | English AI Assistant |
| 其他語言 | - | 自動檢測並回覆 |

---

##  後續功能規劃

- [ ] 集成 Stripe 支付（VIP 自動續費）
- [ ] 實時對話統計儀表板
- [ ] 群組 AI 對話支援
- [ ] 對話導出為 PDF
- [ ] 自訂系統提示詞
- [ ] 多模型支援（Gemini Pro Vision）

---

## 常見問題 (FAQ)

**Q: AI 對話和翻譯可以同時使用嗎？**
A: 否。用戶需要手動切換，輸入 `/返回` 回到翻譯模式。未來可優化為更平順的切換體驗。

**Q: VIP 用戶的 100 次/日對話會不會太多？**
A: 可以根據需求調整 `AI_VIP_DAILY_LIMIT` 環境變量。

**Q: 如何備份對話歷史？**
A: 所有數據存儲在 `ai_conversations` 和 `ai_messages` 表中，可以定期備份數據庫。

**Q: Gemini 免費額度用完了怎麼辦？**
A: 可以升級為 Google Cloud 付費賬戶，或聯繫 Google 申請更高的配額。

---

## 技術聯絡

如有問題，請檢查：
- 📄 [Google Generative AI 文檔](https://ai.google.dev/)
- 📄 [LINE Bot SDK 文檔](https://line-bot-sdk-python.readthedocs.io/)
- 📄 SQLAlchemy [ORM 文檔](https://docs.sqlalchemy.org/)

---

**版本**：1.0.0  
**最後更新**：2025-09-24  
**作者**：FanFan VIP 開發團隊
