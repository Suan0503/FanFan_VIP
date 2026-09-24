"""
AI 對話指令處理器
與 handlers.py 配合使用
"""

from linebot.v3.messaging import TextMessage, FlexMessage

from app.services.ai_service import ai_service
from app.repositories.user_repository import get_user_by_line_id
from app.repositories.vip_repository import get_vip_subscription
from app.db.session import SessionLocal
from app.ui.ai_cards import build_ai_menu_card, build_ai_conversation_card


def handle_ai_start_command(reply_token: str, user_id: str, user_locale: str = "zh-TW") -> None:
    """
    處理 /ai開始 或 /ai start 指令
    開始新的 AI 對話
    """
    if not ai_service:
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text="❌ AI 服務暫時不可用"))
        return

    db = SessionLocal()
    try:
        # 檢查用戶是否 VIP
        user = get_user_by_line_id(db, user_id)
        vip_status = get_vip_subscription(db, user_id)
        is_vip = bool(vip_status)

        # 開始新對話
        conversation_id = ai_service.start_conversation(user_id, is_group=False)

        # 將 conversation_id 存儲到全局上下文
        from app.bot.handlers import AI對話上下文
        AI對話上下文[f"ai:{user_id}"] = conversation_id

        # 回覆開始對話的菜單
        if user_locale == "zh-TW":
            reply_text = f"✨ 新對話已開始\nID: {conversation_id}\n\n現在輸入你的問題，我會直接回答（不翻譯）。\n\n💡 說 /返回 或 /回到翻譯 可以回到翻譯模式。"
        else:
            reply_text = f"✨ New conversation started\nID: {conversation_id}\n\nJust type your question!\n\n💡 Say /back or /return to translation to go back to translation mode."

        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)

        api.reply_message(
            reply_token,
            TextMessage(text=reply_text)
        )
    finally:
        db.close()


def handle_ai_chat(
    reply_token: str,
    user_id: str,
    message: str,
    conversation_id: str = None,
    user_locale: str = "zh-TW"
) -> None:
    """
    處理 AI 對話
    """
    if not ai_service:
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text="❌ AI 服務暫時不可用"))
        return

    db = SessionLocal()
    try:
        # 檢查用戶是否 VIP
        user = get_user_by_line_id(db, user_id)
        vip_status = get_vip_subscription(db, user_id)
        is_vip = bool(vip_status)

        # 執行 AI 對話
        response, conv_id, stats = ai_service.chat(
            user_id=user_id,
            query=message,
            conversation_id=conversation_id,
            is_vip=is_vip,
            language=user_locale,
        )

        # 檢查是否超過限制
        if stats.get("error") == "daily_limit_exceeded":
            from linebot.v3.messaging import MessagingApi, Configuration
            from app.core.config import settings
            config = Configuration(access_token=settings.line_channel_access_token)
            api = MessagingApi(config)
            api.reply_message(reply_token, TextMessage(text=response))
            return

        # 構建回應卡片
        card = build_ai_conversation_card(
            conversation_id=conv_id,
            query=message,
            response=response,
            daily_used=stats.get("daily_used", 0),
            daily_limit=stats.get("daily_limit", 10),
            user_locale=user_locale,
        )

        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)

        api.reply_message(
            reply_token,
            FlexMessage(altText=user_locale == "zh-TW" and "💬 AI 回應" or "💬 AI Response", contents=card["contents"])
        )
    except Exception as e:
        print(f"AI Chat Error: {str(e)}")
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text=f"❌ 發生錯誤：{str(e)[:50]}"))
    finally:
        db.close()


def handle_ai_menu_command(reply_token: str, user_locale: str = "zh-TW") -> None:
    """
    處理 /ai 或 /ai菜單 指令
    顯示 AI 助手菜單
    """
    card = build_ai_menu_card(user_locale)

    from linebot.v3.messaging import MessagingApi, Configuration, FlexMessage
    from app.core.config import settings
    config = Configuration(access_token=settings.line_channel_access_token)
    api = MessagingApi(config)

    api.reply_message(
        reply_token,
        FlexMessage(
            altText=user_locale == "zh-TW" and "🤖 AI 助手" or "🤖 AI Assistant",
            contents=card["contents"]
        )
    )


def handle_ai_history_command(reply_token: str, user_id: str, user_locale: str = "zh-TW") -> None:
    """
    處理 /ai歷史 或 /ai history 指令
    顯示用戶的對話歷史
    """
    if not ai_service:
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text="❌ AI 服務暫時不可用"))
        return

    try:
        conversations = ai_service.list_user_conversations(user_id, limit=5)

        if not conversations:
            if user_locale == "zh-TW":
                text = "📭 還沒有對話歷史\n\n輸入 /ai開始 開啟新對話吧～"
            else:
                text = "📭 No conversation history yet\n\nType /ai start to begin!"
        else:
            if user_locale == "zh-TW":
                text = "📋 最近的對話：\n\n"
                for i, conv in enumerate(conversations, 1):
                    text += f"{i}. {conv.title}\n   ID: {conv.conversation_id}\n   {conv.message_count}條消息\n\n"
            else:
                text = "📋 Recent Conversations:\n\n"
                for i, conv in enumerate(conversations, 1):
                    text += f"{i}. {conv.title}\n   ID: {conv.conversation_id}\n   {conv.message_count} messages\n\n"

        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)

        api.reply_message(reply_token, TextMessage(text=text))
    except Exception as e:
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text=f"❌ 錯誤：{str(e)[:50]}"))


def handle_ai_stats_command(reply_token: str, user_id: str, user_locale: str = "zh-TW") -> None:
    """
    處理 /ai統計 或 /ai stats 指令
    顯示用戶的 AI 使用統計
    """
    from app.repositories.ai_repository import get_ai_usage_stats
    db = SessionLocal()
    try:
        stats = get_ai_usage_stats(db, user_id, days=7)

        if user_locale == "zh-TW":
            text = f"""📊 AI 使用統計（最近7天）

📝 總查詢數：{stats['total_queries']}
✅ 成功回應：{stats['total_responses']}
👑 VIP對話：{stats['vip_queries']}
🆓 免費對話：{stats['free_queries']}

{'升級VIP享受無限對話！' if stats['free_queries'] > 5 else '使用情況良好'}"""
        else:
            text = f"""📊 AI Usage Stats (Last 7 days)

📝 Total Queries: {stats['total_queries']}
✅ Successful Responses: {stats['total_responses']}
👑 VIP Conversations: {stats['vip_queries']}
🆓 Free Conversations: {stats['free_queries']}

{'Upgrade to VIP for unlimited conversations!' if stats['free_queries'] > 5 else 'Good usage pattern'}"""

        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)

        api.reply_message(reply_token, TextMessage(text=text))
    except Exception as e:
        from linebot.v3.messaging import MessagingApi, Configuration
        from app.core.config import settings
        config = Configuration(access_token=settings.line_channel_access_token)
        api = MessagingApi(config)
        api.reply_message(reply_token, TextMessage(text=f"❌ 錯誤：{str(e)[:50]}"))
    finally:
        db.close()
