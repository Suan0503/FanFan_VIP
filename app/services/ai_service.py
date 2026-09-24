import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Optional
import os

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.ai_repository import (
    create_conversation,
    get_conversation,
    add_message_to_conversation,
    get_conversation_history,
    create_usage_log,
    get_today_conversation_count,
)
from app.repositories.user_repository import get_user_by_line_id
from app.repositories.vip_repository import get_vip_subscription


class AIService:
    def __init__(self):
        """初始化 Gemini API"""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            raise ValueError("GEMINI_API_KEY not configured")

    def check_daily_limit(self, user_id: str, is_vip: bool) -> tuple[bool, int, int]:
        """
        檢查用戶今日對話次數是否超過限制

        Returns:
            (是否超過限制, 已使用次數, 每日限制次數)
        """
        db = SessionLocal()
        try:
            count = get_today_conversation_count(db, user_id)
            limit = settings.ai_vip_daily_limit if is_vip else settings.ai_free_daily_limit
            return count >= limit, count, limit
        finally:
            db.close()

    def start_conversation(
        self,
        user_id: str,
        is_group: bool = False,
        group_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        """
        開始新對話，返回 conversation_id
        """
        db = SessionLocal()
        try:
            conversation = create_conversation(
                db,
                line_user_id=user_id,
                is_group=is_group,
                group_id=group_id,
                title=title,
            )
            return conversation.conversation_id
        finally:
            db.close()

    def get_system_prompt(self, is_vip: bool = False, language: str = "zh-TW") -> str:
        """
        獲得系統提示詞
        """
        vip_note = "You are a premium AI assistant with enhanced capabilities." if is_vip else ""

        if language == "zh-TW":
            return f"""你是翻翻君 (FanFan) 的 AI 助手。
你的角色是幫助用戶解答問題、提供建議、進行對話。

特點：
- 友善、樂於助人
- 回答簡潔且有用
- 支持中文、英文等多語言
- 如有不確定的事項，會坦誠說明
{vip_note}

如果用戶需要翻譯，建議他們使用翻翻君的翻譯功能。
回應時請使用繁體中文。"""

        elif language == "en":
            return f"""You are FanFan's AI Assistant.
Your role is to help users answer questions, provide advice, and have conversations.

Characteristics:
- Friendly and helpful
- Concise and useful responses
- Support multiple languages including English and Chinese
- Be honest if you're uncertain about something
{vip_note}

If users need translation, suggest they use FanFan's translation feature.
Respond in English."""

        else:
            return f"""You are FanFan's AI Assistant.
Help users with questions and provide useful conversations.
{vip_note}"""

    def chat(
        self,
        user_id: str,
        query: str,
        conversation_id: Optional[str] = None,
        is_vip: bool = False,
        language: str = "zh-TW",
    ) -> tuple[str, Optional[str], dict]:
        """
        AI 對話主函數

        Args:
            user_id: 使用者 LINE ID
            query: 用戶查詢
            conversation_id: 對話 ID（None 則建立新對話）
            is_vip: 是否 VIP 用戶
            language: 語言代碼

        Returns:
            (回應文本, 對話ID, 使用統計)
        """
        db = SessionLocal()
        try:
            # 檢查每日限制
            exceeded, used, limit = self.check_daily_limit(user_id, is_vip)
            if exceeded:
                return (
                    f"❌ 今日對話次數已達限制（{used}/{limit}）\n"
                    f"{'✨ 升級 VIP 可享受無限對話' if not is_vip else '明天再來吧！'}",
                    conversation_id,
                    {"error": "daily_limit_exceeded", "used": used, "limit": limit}
                )

            # 如果沒有 conversation_id，建立新對話
            if not conversation_id:
                conversation = create_conversation(db, line_user_id=user_id)
                conversation_id = conversation.conversation_id
            else:
                # 驗證對話是否存在
                conversation = get_conversation(db, conversation_id)
                if not conversation or conversation.line_user_id != user_id:
                    return (
                        "❌ 對話不存在或無權限",
                        conversation_id,
                        {"error": "conversation_not_found"}
                    )

            # 獲得對話歷史（上下文）
            history = get_conversation_history(db, conversation_id, limit=10)

            # 構建 Gemini 對話內容
            system_prompt = self.get_system_prompt(is_vip, language)
            messages = [{"role": "user" if msg.role == "user" else "model", "parts": [msg.content]} for msg in history]

            # 如果沒有歷史，添加系統提示
            if not messages:
                messages = [{"role": "user", "parts": [system_prompt + "\n\n用戶查詢：" + query]}]
            else:
                messages.append({"role": "user", "parts": [query]})

            # 調用 Gemini API
            try:
                response = self.model.generate_content(
                    messages,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=1024,
                    ),
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_ONLY_HIGH",
                        },
                    ]
                )

                response_text = response.text if response else "❌ 無法生成回應"
            except Exception as e:
                response_text = f"❌ AI 服務暫時出錯，請稍後重試"
                print(f"Gemini API Error: {str(e)}")

            # 保存消息到對話歷史
            add_message_to_conversation(db, conversation_id, "user", query)
            add_message_to_conversation(db, conversation_id, "assistant", response_text)

            # 記錄使用日誌
            usage_log = create_usage_log(
                db,
                line_user_id=user_id,
                conversation_id=conversation_id,
                query=query,
                response=response_text,
                is_vip=is_vip,
            )

            # 如果是 VIP，消耗翻譯額度（可選）
            if is_vip:
                from app.services.vip_service import consume_vip_chars
                char_count = len(response_text)
                try:
                    consume_vip_chars(db, user_id, char_count)
                except:
                    pass  # VIP 額度不足不影響對話

            return (
                response_text,
                conversation_id,
                {
                    "tokens_input": getattr(response.usage_metadata, 'prompt_token_count', None),
                    "tokens_output": getattr(response.usage_metadata, 'candidates_token_count', None),
                    "daily_used": used + 1,
                    "daily_limit": limit,
                }
            )

        except Exception as e:
            print(f"AI Chat Error: {str(e)}")
            return (
                "❌ 發生錯誤，請稍後重試",
                conversation_id,
                {"error": str(e)}
            )
        finally:
            db.close()

    def list_user_conversations(self, user_id: str, limit: int = 10):
        """
        列出用戶最近的對話
        """
        from app.repositories.ai_repository import get_user_conversations
        db = SessionLocal()
        try:
            return get_user_conversations(db, user_id, limit=limit)
        finally:
            db.close()

    def clear_expired_conversations(self):
        """
        清理過期對話（超過7天）
        """
        from app.repositories.ai_repository import delete_expired_conversations
        db = SessionLocal()
        try:
            deleted_count = delete_expired_conversations(db)
            return deleted_count
        finally:
            db.close()


# 全局 AI 服務實例
try:
    ai_service = AIService()
except:
    ai_service = None
