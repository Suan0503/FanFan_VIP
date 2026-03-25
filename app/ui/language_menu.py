from linebot.v3.messaging import QuickReply, QuickReplyItem, MessageAction  # 匯入 Quick Reply 元件

from app.core.languages import SUPPORTED_LANGUAGES  # 匯入語言清單


def build_language_menu_quick_reply() -> QuickReply:
    items: list[QuickReplyItem] = []  # 初始化按鈕列表
    for language_name in SUPPORTED_LANGUAGES:
        items.append(
            QuickReplyItem(
                action=MessageAction(
                    label=language_name,
                    text=f"設定語言 {language_name}",
                )
            )
        )  # 依序建立語言按鈕
    items.append(QuickReplyItem(action=MessageAction(label="重設", text="重設翻譯設定")))  # 新增重設按鈕
    return QuickReply(items=items)  # 回傳 Quick Reply
