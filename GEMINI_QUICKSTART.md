# ⚡ Google Gemini AI 集成 - 快速開始 (5 分鐘)

## 🎯 目標
在 FanFan VIP 中集成 Google Gemini AI，添加 AI 對話功能。

---

## ✅ 完成的任務

### 1. 依賴更新
- ✅ `requirements.txt` 已添加 `google-generativeai==0.7.2`

### 2. 配置更新
- ✅ `app/core/config.py` 已添加 Gemini 配置
  - `GEMINI_API_KEY`
  - `GEMINI_MODEL`
  - `AI_FREE_DAILY_LIMIT` (默認 10)
  - `AI_VIP_DAILY_LIMIT` (默認 100)

### 3. 數據模型
- ✅ `app/db/models.py` 已添加 3 個新表：
  - `AIConversation` - 對話紀錄
  - `AIMessage` - 消息記錄
  - `AIUsageLog` - 使用統計

### 4. 服務層
- ✅ `app/services/ai_service.py` - AI 服務核心
  - `check_daily_limit()` - 檢查配額
  - `start_conversation()` - 開始對話
  - `chat()` - 執行對話邏輯
  - `get_system_prompt()` - 系統提示詞

### 5. 數據層
- ✅ `app/repositories/ai_repository.py` - 數據訪問層
  - CRUD 操作
  - 統計查詢
  - 自動清理過期對話

### 6. UI 菜單
- ✅ `app/ui/ai_cards.py` - Flex 卡片設計
  - AI 菜單卡片
  - 對話結果卡片

### 7. 指令處理
- ✅ `app/bot/handlers_ai.py` - 所有 AI 指令處理
  - `/ai` - 菜單
  - `/ai開始` - 開始對話
  - `/ai歷史` - 查看歷史
  - `/ai統計` - 查看統計

### 8. 主 Handlers 集成
- ✅ `app/bot/handlers.py` 已集成 AI 指令
  - 添加 AI 指令定義
  - 添加 AI 返回翻譯指令
  - 在翻譯前檢查 AI 對話上下文

### 9. 環境配置
- ✅ `.env.example` 已更新 Gemini 配置

---

## 🚀 本地測試步驟

### 第1步：申請 Gemini API Key（1分鐘）

```bash
# 打開網頁申請
# https://aistudio.google.com/app/apikey

# 點擊 "Create API Key" → "Create API Key in new Google Cloud project"
# 複製生成的 Key
```

### 第2步：配置環境變量（1分鐘）

```bash
# 1. 複製 .env 文件
cp .env.example .env

# 2. 編輯 .env，添加：
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
AI_FREE_DAILY_LIMIT=10
AI_VIP_DAILY_LIMIT=100
```

### 第3步：安裝依賴（2分鐘）

```bash
# 激活虛擬環境
python -m venv .venv
source .venv/Scripts/activate

# 安裝新依賴
pip install google-generativeai==0.7.2 python-dotenv==1.0.1
```

### 第4步：啟動應用（1分鐘）

```bash
# 啟動 FastAPI 應用
uvicorn app.main:app --reload

# 應該看到：
# INFO:     Uvicorn running on http://127.0.0.1:8000
# ✅ 數據表已自動建立
```

---

## 📱 LINE 測試流程

### 1. 打開菜單
```
用戶輸入：/ai
FanFan回覆：[顯示 AI 助手菜單卡片]
```

### 2. 開始對話
```
用戶輸入：/ai開始
FanFan回覆：
✨ 新對話已開始
ID: conv_abc123...

現在輸入你的問題，我會直接回答（不翻譯）。
💡 說 /返回 或 /回到翻譯 可以回到翻譯模式。
```

### 3. 發送問題
```
用戶輸入：什麼是人工智能？
FanFan回覆：[Gemini 的回答 + Flex 卡片]

💬 AI 回應
你的提問：什麼是人工智能？

🤖 AI 回答：
人工智能（AI）是指由人制造出來的...

今日使用: 1/10
🔋
```

### 4. 繼續對話
```
用戶輸入：它有什麼應用？
FanFan回覆：[Gemini 基於上下文回答]
（記得前一個問題）

今日使用: 2/10
```

### 5. 查看統計
```
用戶輸入：/ai統計
FanFan回覆：
📊 AI 使用統計（最近7天）

📝 總查詢數：2
✅ 成功回應：2
👑 VIP對話：0
🆓 免費對話：2
```

### 6. 返回翻譯
```
用戶輸入：/返回
FanFan回覆：
✅ 已返回翻譯模式

現在輸入文字會直接進行翻譯。

用戶輸入：Hello
FanFan回覆：翻譯結果：嗨
```

---

## ⚙️ 配置調整

### 調整每日限制

編輯 `.env`：
```env
AI_FREE_DAILY_LIMIT=20      # 免費用戶改為 20 次/日
AI_VIP_DAILY_LIMIT=200      # VIP 用戶改為 200 次/日
```

### 切換 Gemini 模型

```env
GEMINI_MODEL=gemini-2.0-flash           # 快速、便宜（推薦）
GEMINI_MODEL=gemini-1.5-pro             # 更強大、更貴
GEMINI_MODEL=gemini-1.5-flash           # 快速版本
```

### 自訂系統提示詞

編輯 `app/services/ai_service.py`，修改 `get_system_prompt()` 方法：

```python
def get_system_prompt(self, is_vip: bool = False, language: str = "zh-TW") -> str:
    if language == "zh-TW":
        return """你是翻翻君的 AI 助手。
# 自訂你的提示詞...
"""
```

---

## 🔍 驗證安裝

### 檢查 1：API 連接

```bash
python << 'EOF'
import google.generativeai as genai
genai.configure(api_key="your_key_here")
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("Say 'hello'")
print("✅ API 連接成功:", response.text)
EOF
```

### 檢查 2：數據庫表

```bash
python << 'EOF'
from app.db.session import SessionLocal
from app.db.models import AIConversation, AIMessage, AIUsageLog

db = SessionLocal()
print("✅ AIConversation 表存在:", db.query(AIConversation).count())
print("✅ AIMessage 表存在:", db.query(AIMessage).count())
print("✅ AIUsageLog 表存在:", db.query(AIUsageLog).count())
EOF
```

### 檢查 3：匯入檢查

```bash
python << 'EOF'
from app.services.ai_service import ai_service
from app.bot.handlers_ai import handle_ai_chat
print("✅ 所有模塊導入成功")
print("✅ AI 服務已初始化:", ai_service is not None)
EOF
```

---

## 📊 Gemini 免費配額

| 項目 | 限制 | 備註 |
|------|------|------|
| 請求數/分鐘 | 60 | 對話不會超過 |
| 請求數/月 | 1,500 | ~50次/天 |
| 成本 | 免費 | 完全免費 |
| 響應時間 | ~1-3秒 | 取決於網路 |

**計算：**
- 如果每天 50 個免費用戶各對話 1 次 = 50 次/天
- 10 個 VIP 用戶各對話 5 次 = 50 次/天
- 總計 100 次/天 < 1,500 次/月 ✅

---

## 🐛 常見問題

**Q: 安裝後還要重啟 LINE bot 嗎？**  
A: 是的，需要重新部署或重啟應用，以便加載新的數據表。

**Q: 免費配額用完了怎麼辦？**  
A: 
1. 等待下個月配額重置
2. 升級為 Google Cloud 付費用戶
3. 改用其他 AI 服務（OpenAI、Anthropic 等）

**Q: 如何導出對話歷史？**  
A: 
```bash
# 直接查詢數據庫
sqlite3 translator.db "SELECT * FROM ai_conversations;"
sqlite3 translator.db "SELECT * FROM ai_messages;" > history.sql
```

**Q: 如何清理舊對話？**  
A:
```python
from app.services.ai_service import ai_service
deleted = ai_service.clear_expired_conversations()
print(f"已刪除 {deleted} 個過期對話")
```

---

## 📚 後續優化

### 優先級 1（推薦立即實裝）
- [ ] 實現 `/ai菜單 功能選擇卡片`（而不是 `/ai開始`）
- [ ] 添加 `/ai清空` 清除當前對話
- [ ] 支援對話導出為文本文件

### 優先級 2（未來增強）
- [ ] 群組 AI 對話模式（共享額度）
- [ ] 自訂系統提示詞（VIP 功能）
- [ ] 對話成本計費（不同模型不同價格）
- [ ] 與支付系統集成（自動充值）

### 優先級 3（長期計劃）
- [ ] 集成 Gemini Vision（圖像理解）
- [ ] 多模型支援切換（Claude、GPT-4 等）
- [ ] 實時流式回應（減少延遲）
- [ ] 對話分析儀表板

---

## 📞 技術支援

遇到問題？
1. 檢查 `.env` 是否正確設置
2. 查看日誌：`tail -f logs/fanfan.log`
3. 閱讀完整指南：`GEMINI_SETUP.md`
4. 查詢官方文檔：[Google AI Documentation](https://ai.google.dev/)

---

✅ **恭喜！Gemini AI 已成功集成到 FanFan VIP。祝您使用愉快！**
