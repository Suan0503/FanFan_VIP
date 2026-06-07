from datetime import datetime

from linebot.v3 import WebhookHandler  # 匯入 Webhook Handler
from linebot.v3.exceptions import InvalidSignatureError  # 匯入簽章錯誤
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    FlexMessage,
    LocationAction,
    MessagingApi,
    MessagingApiBlob,
    QuickReply,
    QuickReplyItem,
    ReplyMessageRequest,
    TextMessage,
)  # 匯入 Messaging API
from linebot.v3.webhooks import AudioMessageContent, FollowEvent, JoinEvent, LocationMessageContent, MemberJoinedEvent, MemberLeftEvent, MessageEvent, TextMessageContent  # 匯入事件型別

from app.core.config import settings  # 匯入設定
from app.core.languages import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE_CODE  # 匯入語言設定
from app.db.session import SessionLocal  # 匯入資料庫 Session
from app.repositories.user_repository import create_user, get_user_by_line_id, update_user_admin_flag, update_user_language  # 匯入使用者存取
from app.repositories.group_repository import (
    get_group,
    create_group,
    bind_group_inviter,
    set_group_inviter,
    get_group_languages,
    set_group_languages,
)  # 匯入群組存取
from app.services.id_service import generate_member_code  # 匯入編號服務
from app.services.vip_service import activate_vip_by_serial, generate_unique_vip_serial, get_vip_status
from app.services.travel_assistant_service import build_travel_progress_text, build_travel_reply, transcribe_audio_with_whisper_open_source
from app.services.travel_context import consume_awaiting_location, get_last_location, mark_awaiting_location, set_last_location
from app.services.translation_service import translate_text, translate_text_vip_pro  # 匯入翻譯服務
from app.services.permission_service import can_manage_group  # 匯入權限服務
from app.ui.menu_cards import build_language_setting_card, build_main_menu_card, build_vip_main_menu_card  # 匯入新版 Flex 小卡
from app.ui.travel_cards import build_travel_mode_card
from app.ui.travel_i18n import get_travel_back_commands, get_travel_confirm_commands, get_travel_entry_commands, get_travel_i18n
from app.ui.welcome_i18n import get_welcome_i18n
from app.fanfan_core.language_profile import resolve_language_code, parse_language_labels  # 匯入舊版語言解析核心
from app.fanfan_core.group_service import ensure_group_exists, toggle_or_set_languages, reset_languages  # 匯入舊版群組設定核心
from app.fanfan_core.formatting import format_language_updated, format_translation_results, detect_source_language  # 匯入舊版輸出格式核心


configuration = Configuration(access_token=settings.line_channel_access_token)  # 建立 LINE API 設定
line_handler = WebhookHandler(settings.line_channel_secret)  # 建立 webhook handler

語言選單指令 = {"語言設定", "語言選單"}  # 中文語言選單指令
主選單指令 = {"主選單", "功能選單", "選單小卡", "選單", "menu"}  # 主選單指令（含斜線正規化）
綁定邀請者指令 = "綁定邀請者"  # 綁定邀請者代表指令
管理員白名單指令 = {"查看群組設定", "重設邀請者"}  # 僅管理者可用的群組指令
說明指令 = {"指令說明", "使用說明", "幫助"}  # 顯示說明指令
重設翻譯指令 = {"重設翻譯設定", "重設語言"}  # 重設群組翻譯語言
自動偵測啟用指令 = {"啟用自動偵測", "自動偵測"}  # 啟用非中文轉中文
自動偵測關閉指令 = {"關閉自動偵測"}  # 關閉自動偵測
即時翻譯啟用指令 = {"開啟即時翻譯"}  # 開啟即時翻譯
即時翻譯關閉指令 = {"關閉即時翻譯"}  # 關閉即時翻譯
旅遊模式指令 = get_travel_entry_commands()  # 旅遊模式入口（依語言模組自動彙整）
旅遊模式確認指令 = get_travel_confirm_commands()  # 同意並分享定位（依語言模組自動彙整）
旅遊模式返回指令 = get_travel_back_commands()  # 取消並返回主選單（依語言模組自動彙整）

即時翻譯狀態: dict[str, bool] = {}  # 依使用情境保存即時翻譯開關
自動偵測狀態: dict[str, bool] = {}  # 依使用情境保存自動偵測開關
使用者智慧配置: dict[str, dict[str, str | bool]] = {}  # 使用者地區與語言自動配置
語言模式顯示 = {
    "zh-TW": "TW 中文",
    "en": "US English",
    "th": "TH ไทย",
    "ja": "JP 日本語",
    "vi": "VN Tiếng Việt",
    "ko": "KR 한국어",
    "id": "ID Bahasa Indonesia",
    "my": "MM မြန်မာ",
    "ru": "RU Русский",
}  # 語言模式顯示文字


語言區域配置 = {
    "zh-TW": ("台灣 Taiwan", "Asia｜Taiwan"),
    "en": ("美國 USA", "Global｜US"),
    "th": ("泰國 Thailand", "Asia｜Thailand"),
    "ja": ("日本 Japan", "Asia｜Japan"),
    "vi": ("越南 Vietnam", "Asia｜Vietnam"),
    "ko": ("韓國 Korea", "Asia｜Korea"),
    "id": ("印尼 Indonesia", "Asia｜Indonesia"),
    "my": ("緬甸 Myanmar", "Asia｜Myanmar"),
    "ru": ("俄羅斯 Russia", "Europe｜Russia"),
}  # 語言對應地區與節點

群組語言上限 = 2  # 群組翻譯最多僅支援兩種語言
超級管理員ID = "U5ce6c382d12eaea28d98f2d48673b4b8"  # 超級管理員固定 ID

VIP啟用指令 = {"vip開通", "啟用VIP", "vip"}
VIP主選單指令 = {"VIP主選單", "vip主選單"}
VIP序號產生指令 = "產生序號"
超管新增管理員指令 = "新增管理員"

待輸入VIP序號使用者: set[str] = set()  # 等待輸入序號狀態
超管群組在場狀態: dict[str, bool] = {}  # 記錄超級管理員是否在群組內


def _狀態鍵(source_type: str, user_id: str | None, group_id: str | None) -> str:
    if source_type == "group" and group_id:
        return f"group:{group_id}"  # 群組模式鍵
    return f"user:{user_id or 'anonymous'}"  # 個人模式鍵


def _目前開關狀態(state_key: str, default_auto_detect: bool) -> tuple[bool, bool]:
    translation_enabled = 即時翻譯狀態.get(state_key, True)  # 預設開啟即時翻譯
    auto_detect_enabled = 自動偵測狀態.get(state_key, default_auto_detect)  # 預設依語言狀態決定
    return translation_enabled, auto_detect_enabled


def _提取_line_language(event: FollowEvent) -> str | None:
    language = getattr(event, "language", None) or getattr(getattr(event, "source", None), "language", None)  # 取可能欄位
    if not isinstance(language, str):
        return None
    value = language.strip().lower()
    return value if value else None


def _line_language_對應語言代碼(line_language: str) -> str:
    normalized = line_language.lower()
    if normalized.startswith("zh"):
        return "zh-TW"
    if normalized.startswith("en"):
        return "en"
    if normalized.startswith("th"):
        return "th"
    if normalized.startswith("ja"):
        return "ja"
    if normalized.startswith("vi"):
        return "vi"
    if normalized.startswith("ko"):
        return "ko"
    if normalized.startswith("id"):
        return "id"
    if normalized.startswith("my"):
        return "my"
    if normalized.startswith("ru"):
        return "ru"
    return "en"  # 無法解析時預設英文


def _文字偵測語言代碼(text: str) -> str:
    candidate_codes = list(語言區域配置.keys())  # 目前支援語言
    detected = detect_source_language(text, candidate_codes)
    return detected if detected else "en"  # 偵測不到時預設英文


def _設定使用者智慧配置(user_id: str, language_code: str, configured: bool) -> dict[str, str | bool]:
    region_name, service_node = 語言區域配置.get(language_code, 語言區域配置["en"])
    profile = {
        "configured": configured,
        "language_code": language_code,
        "region_name": region_name,
        "service_node": service_node,
    }
    使用者智慧配置[user_id] = profile  # 寫入地區配置
    return profile


def _取得使用者智慧配置(user_id: str) -> dict[str, str | bool] | None:
    return 使用者智慧配置.get(user_id)


def _建立智慧配置歡迎訊息(member_code: str, profile: dict[str, str | bool]) -> str:
    language_code = str(profile.get("language_code", "en"))
    language_mode = 語言模式顯示.get(language_code, "US 英文")
    region_name = str(profile.get("region_name", "美國 USA"))
    service_node = str(profile.get("service_node", "Global｜US"))
    i18n = get_welcome_i18n(language_code)
    return (
        f"{i18n['title']}\n"
        f"{i18n['started']}\n"
        "━━━━━━━━━━━━━━\n\n"
        f"{i18n['account_id']}\n"
        f"{member_code}\n\n"
        f"{i18n['system_status']}\n"
        f"{i18n['running']}\n\n"
        f"{i18n['smart_region']}\n"
        f"{i18n['auto_detected'].format(region=region_name)}\n\n"
        f"{i18n['auto_config_done']}\n"
        f"{i18n['language_mode'].format(mode=language_mode)}\n"
        f"{i18n['service_node'].format(node=service_node)}\n"
        "━━━━━━━━━━━━━━"
    )  # 回傳新版歡迎訊息


def _語言代碼轉名稱(language_code: str) -> str:
    for language_name, code in SUPPORTED_LANGUAGES.items():
        if code == language_code:
            return language_name  # 找到對應語言名稱
    return f"未知語言({language_code})"  # 找不到時保留代碼


def _群組語言摘要(language_codes: list[str]) -> str:
    if not language_codes:
        return "(無)"  # 防禦性回傳
    labels = [_語言代碼轉名稱(code) for code in language_codes]  # 轉成語言名稱
    return "、".join(labels)  # 組合摘要文字


def _自動偵測目標語言(source_type: str, user, group_id: str | None, db) -> str:
    if source_type == "group" and group_id:
        group_codes = get_group_languages(db, group_id)
        return group_codes[0] if group_codes else DEFAULT_LANGUAGE_CODE  # 群組沿用第一個主語言
    if user and getattr(user, "target_language", None):
        return user.target_language  # 個人模式沿用目前選單語言
    return DEFAULT_LANGUAGE_CODE  # 無資料時回退預設語言


def _智慧偵測群組語言(db, group_id: str, text: str) -> tuple[list[str], str | None]:
    current_codes = get_group_languages(db, group_id)  # 目前群組語言
    if not current_codes:
        current_codes = [DEFAULT_LANGUAGE_CODE]

    detected_code = _文字偵測語言代碼(text)  # 從訊息內容偵測語言
    if detected_code in {DEFAULT_LANGUAGE_CODE, "en"}:
        return current_codes, None  # 中文與英文不觸發語言擴充

    if detected_code in current_codes:
        return current_codes, None  # 已存在語言不變更

    if len(current_codes) >= 群組語言上限:
        return current_codes, "ℹ 群組智慧翻譯僅支援 2 種語言，維持目前設定。"

    next_codes = [DEFAULT_LANGUAGE_CODE, detected_code]  # 固定中文為主語，第二語言自動加入
    updated_codes = set_group_languages(db, group_id, next_codes)
    return updated_codes, f"🧠 已啟用智慧雙語：{_群組語言摘要(updated_codes)}（最多 2 種語言）"


def _標準化指令文字(text: str) -> str:
    normalized = text.strip()  # 清理首尾空白
    while normalized.startswith(("/", "／")):
        normalized = normalized[1:].strip()  # 移除開頭斜線
    return normalized  # 回傳正規化後指令


def _是超級管理員(user_id: str | None) -> bool:
    return bool(user_id and user_id == 超級管理員ID)


def _是可產生序號管理者(user) -> bool:
    return bool(user and user.is_admin)


def _格式化時間(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def _查詢顯示名稱(source_type: str, group_id: str | None, user_id: str | None) -> str:
    if not user_id:
        return "Unknown"

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        try:
            if source_type == "group" and group_id:
                profile = messaging_api.get_group_member_profile(group_id=group_id, user_id=user_id)
                name = getattr(profile, "display_name", None)
                if isinstance(name, str) and name.strip():
                    return name.strip()
            profile = messaging_api.get_profile(user_id=user_id)
            name = getattr(profile, "display_name", None)
            if isinstance(name, str) and name.strip():
                return name.strip()
        except Exception:
            return "Unknown"
    return "Unknown"


def _抽取被提及用戶ID(message) -> str | None:
    mention = getattr(message, "mention", None)
    mentionees = getattr(mention, "mentionees", None)
    if mentionees:
        for mentionee in mentionees:
            user_id = getattr(mentionee, "user_id", None) or getattr(mentionee, "userId", None)
            if isinstance(user_id, str) and user_id.strip():
                return user_id.strip()
    return None


def _vip是否啟用(vip_status) -> bool:
    return bool(vip_status and bool(vip_status.get("is_active", False)))


def _建立說明文字(source_type: str, is_group_manager: bool) -> str:
    lines = [
        "翻翻君指令說明：",
        "1. /選單 /menu /主選單",
        "   開啟主選單（Flex 卡片）。",
        "2. 語言設定 / 語言選單",
        "   開啟語言快速選單。",
        "3. 設定語言 中文",
        "   個人聊天可切換單一翻譯語言。",
        "4. 指令說明 / 使用說明 / 幫助",
        "   顯示這份說明。",
        "5. 預設翻譯通道：DeepL（失敗時自動備援）。",
        "6. vip開通",
        "   輸入序號啟用 VIP，預設 DeepL Pro 10萬字元。",
        "7. VIP主選單",
        "   查看開通時間、當前方案、剩餘字數。",
    ]  # 基礎說明

    if source_type == "group":
        lines.extend(
            [
                "8. 綁定邀請者",
                "   由群組第一位綁定者成為邀請者代表。",
                "9. 設定語言 中文、泰文",
                "   群組可複選語言，之後每句都會翻譯成多語。",
                "10. 重設翻譯設定",
                "   把群組翻譯語言重設成中文。",
                "11. 查看群組設定",
                "   查看本群翻譯語言與邀請者代表。",
                "12. 重設邀請者",
                "   把邀請者代表改成目前發送指令的人。",
            ]
        )  # 群組指令
        if not is_group_manager:
            lines.append("※ 查看群組設定 / 重設邀請者 僅限邀請者代表、管理員、所有者使用。")  # 權限說明

    return "\n".join(lines)  # 組合說明文字


def _reply_text(reply_token: str, message: str, with_language_menu: bool = False) -> None:
    quick_reply = None  # 關閉底部 Quick Reply 小按鈕
    _reply_messages(reply_token, [TextMessage(text=message, quickReply=quick_reply, quoteToken=None)])  # 回覆單一文字


def _reply_messages(reply_token: str, messages: list[TextMessage | FlexMessage]) -> None:
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)  # 建立訊息 API
        messaging_api.reply_message(
            ReplyMessageRequest(
                replyToken=reply_token,
                messages=messages,
                notificationDisabled=False,
            )
        )  # 回覆文字


def _download_message_content(message_id: str) -> bytes | None:
    with ApiClient(configuration) as api_client:
        blob_api = MessagingApiBlob(api_client)
        try:
            raw = blob_api.get_message_content(message_id=message_id)
        except Exception:
            return None

    if isinstance(raw, (bytes, bytearray)):
        return bytes(raw)
    data = getattr(raw, "data", None)
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    reader = getattr(raw, "read", None)
    if callable(reader):
        try:
            content = reader()
        except Exception:
            return None
        if isinstance(content, (bytes, bytearray)):
            return bytes(content)
    return None


def _current_language_code(source_type: str, user, group_id: str | None, db) -> str:
    if source_type == "group" and group_id:
        group_codes = get_group_languages(db, group_id)
        return group_codes[0] if group_codes else DEFAULT_LANGUAGE_CODE
    if user and getattr(user, "target_language", None):
        return user.target_language
    return DEFAULT_LANGUAGE_CODE


@line_handler.add(FollowEvent)
def handle_follow(event: FollowEvent) -> None:
    reply_token = event.reply_token  # 取得回覆 token
    user_id = getattr(event.source, "user_id", None)  # 取得使用者 ID
    if not reply_token:
        return  # 無法回覆就跳過
    if not user_id:
        return  # 無使用者 ID 時跳過

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id)  # 查詢使用者
        if not user:
            member_code = generate_member_code(db)  # 產生綁定編號
            user = create_user(db, user_id, member_code, DEFAULT_LANGUAGE_CODE)  # 建立使用者資料
        line_language = _提取_line_language(event)  # 取得 LINE language
        if line_language:
            language_code = _line_language_對應語言代碼(line_language)  # 有值時直接配置
            update_user_language(db, user, language_code)  # 寫入語言模式
            profile = _設定使用者智慧配置(user_id, language_code, True)  # 寫入地區配置
            message = _建立智慧配置歡迎訊息(user.member_code, profile)
            vip_enabled = _vip是否啟用(get_vip_status(db, user_id))
            _reply_messages(
                reply_token,
                [
                    TextMessage(text=message, quickReply=None, quoteToken=None),
                    build_main_menu_card(source_type="user", is_group_manager=False, current_language_code=language_code, vip_enabled=vip_enabled),
                ],
            )  # 有 LINE language 時直接發歡迎訊息
            return

        _設定使用者智慧配置(user_id, "en", False)  # 先建立待配置狀態

    _reply_text(
        reply_token,
        "⚙ 正在等待智慧地區配置\n"
        "請用自己國家語言輸入：你好\n"
        "我會自動偵測地區與語言後完成啟動。\n\n"
        "⚙ Smart region setup is pending.\n"
        "Please type 'hello' in your native language.\n"
        "I will auto-detect your region and language to complete activation.",
    )  # 無 language 時先等待第一句（中英雙語）


@line_handler.add(JoinEvent)
def handle_join(event: JoinEvent) -> None:
    reply_token = event.reply_token  # 取得回覆 token
    group_id = getattr(event.source, "group_id", None)  # 取得群組 ID
    if not reply_token:
        return  # 無法回覆就跳過
    if not group_id:
        return  # 不是群組就跳過

    with SessionLocal() as db:
        group = get_group(db, group_id)  # 查詢群組設定
        if not group:
            create_group(db, group_id)  # 首次進群建立資料

    _reply_messages(
        reply_token,
        [
            TextMessage(
                text="翻翻君已加入群組！\n目前為智慧偵測模式：預設中文，偵測到第二語言會自動切換為雙語翻譯。\n英文訊息會直接翻譯成群組內兩種語言（最多 2 種）。\n請先輸入 /選單 或 /menu 開啟功能選單。\n若要管理群組語言，請邀請者再輸入：綁定邀請者。",
                quickReply=None,
                quoteToken=None,
            ),
            build_main_menu_card(source_type="group", is_group_manager=False, current_language_code=DEFAULT_LANGUAGE_CODE),
        ],
    )  # 回覆群組初始化提示與主選單小卡


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent) -> None:
    reply_token = event.reply_token  # 取得回覆 token
    if not reply_token:
        return  # 無法回覆就跳過

    text = _標準化指令文字(getattr(event.message, "text", ""))  # 取得並正規化文字內容
    text_for_command = text.lower()  # 英文指令以小寫比對
    source_type = getattr(event.source, "type", "")  # 來源型別
    user_id = getattr(event.source, "user_id", None)  # 來源使用者
    group_id = getattr(event.source, "group_id", None) if source_type == "group" else None  # 來源群組
    state_key = _狀態鍵(source_type, user_id, group_id)

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id) if user_id else None  # 查詢使用者資料
        if user_id and not user:
            member_code = generate_member_code(db)  # 產生新編號
            user = create_user(db, user_id, member_code, DEFAULT_LANGUAGE_CODE)  # 自動補建使用者

        vip_status = get_vip_status(db, user_id) if user_id else None
        vip_enabled = _vip是否啟用(vip_status)

        if source_type == "group" and group_id and _是超級管理員(user_id):
            超管群組在場狀態[group_id] = True
            即時翻譯狀態[state_key] = False  # 超級管理員在群組內時強制關閉翻譯

        if source_type == "user" and user_id and user:
            profile = _取得使用者智慧配置(user_id)
            if profile and not bool(profile.get("configured", False)):
                detected_code = _文字偵測語言代碼(text)  # 等第一句 AI 偵測
                update_user_language(db, user, detected_code)  # 寫入語言模式
                configured_profile = _設定使用者智慧配置(user_id, detected_code, True)  # 寫入地區
                message = _建立智慧配置歡迎訊息(user.member_code, configured_profile)
                _reply_messages(
                    reply_token,
                    [
                        TextMessage(text=message, quickReply=None, quoteToken=None),
                        build_main_menu_card(source_type="user", is_group_manager=False, current_language_code=detected_code, vip_enabled=vip_enabled),
                    ],
                )  # 產生歡迎訊息
                return

        current_group = get_group(db, group_id) if group_id else None  # 先讀取群組資料供說明與權限判斷使用
        is_group_manager = bool(current_group and can_manage_group(current_group, user, user_id))  # 是否具備群組管理權限

        if text.startswith(超管新增管理員指令):
            if not _是超級管理員(user_id):
                _reply_text(reply_token, "此指令僅限超級管理員使用。")
                return

            target_user_id = _抽取被提及用戶ID(event.message)
            if not target_user_id:
                words = text.split()
                for word in words:
                    if word.startswith("U") and len(word) >= 20:
                        target_user_id = word
                        break

            if not target_user_id:
                _reply_text(reply_token, "請使用：新增管理員 @用戶")
                return

            target_user = get_user_by_line_id(db, target_user_id)
            if not target_user:
                target_code = generate_member_code(db)
                target_user = create_user(db, target_user_id, target_code, DEFAULT_LANGUAGE_CODE)
            updated_user = update_user_admin_flag(db, target_user, True)
            _reply_text(reply_token, f"✅ 已新增管理員\n會員：{updated_user.member_code}\nUser ID：{updated_user.line_user_id}")
            return

        if text.startswith(VIP序號產生指令):
            if not (_是超級管理員(user_id) or _是可產生序號管理者(user)):
                _reply_text(reply_token, "此指令僅限管理員使用。")
                return

            creator_name = _查詢顯示名稱(source_type, group_id, user_id)
            creator_code = user.member_code if user else None
            serial = generate_unique_vip_serial(
                db=db,
                created_by_user_id=user_id or "",
                created_by_name=creator_name,
                created_by_member_code=creator_code,
            )
            _reply_text(
                reply_token,
                "✅ 已產生 VIP 序號\n"
                f"管理員名稱：{serial.created_by_name}\n"
                f"序號號碼：{serial.serial_code}\n"
                "方案：DeepL Pro 10萬字元\n"
                "狀態：未使用",
            )
            return

        if text_for_command in VIP啟用指令:
            if not user_id:
                _reply_text(reply_token, "無法識別會員，請稍後再試。")
                return
            待輸入VIP序號使用者.add(user_id)
            _reply_text(reply_token, "請輸入 VIP 序號（16 碼，開頭 FANVIP）。")
            return

        if text_for_command in VIP主選單指令:
            if not vip_enabled or not vip_status:
                _reply_text(reply_token, "你目前尚未啟用 VIP，請先點選『vip開通』並輸入序號。")
                return
            _reply_messages(
                reply_token,
                [
                    build_vip_main_menu_card(
                        started_at_text=_格式化時間(vip_status["started_at"]),
                        current_plan=str(vip_status["current_plan"]),
                        remaining_chars=int(vip_status["remaining_chars"]),
                    )
                ],
            )
            return

        if user_id and user_id in 待輸入VIP序號使用者:
            if text in {"取消", "cancel", "取消開通"}:
                待輸入VIP序號使用者.discard(user_id)
                _reply_text(reply_token, "已取消 VIP 開通流程。")
                return

            subscription, message = activate_vip_by_serial(db, user_id, user.member_code if user else "", text)
            if not subscription:
                _reply_text(reply_token, f"❌ 開通失敗：{message}")
                return

            待輸入VIP序號使用者.discard(user_id)
            _reply_messages(
                reply_token,
                [
                    TextMessage(
                        text=(
                            "開通完成 感謝成為翻翻君VIP會員\n"
                            f"剩餘字數：{subscription.remaining_chars}"
                        ),
                        quickReply=None,
                        quoteToken=None,
                    ),
                    build_vip_main_menu_card(
                        started_at_text=_格式化時間(subscription.started_at),
                        current_plan=subscription.current_plan,
                        remaining_chars=subscription.remaining_chars,
                    ),
                ],
            )
            return

        if text_for_command in 語言選單指令:
            selected_codes = get_group_languages(db, group_id) if group_id else [user.target_language] if user else [DEFAULT_LANGUAGE_CODE]  # 取得目前勾選語言
            _reply_messages(
                reply_token,
                [
                    TextMessage(text="請使用下方小卡設定翻譯語言。", quickReply=None, quoteToken=None),
                    build_language_setting_card(selected_codes, source_type, is_group_manager),
                ],
            )  # 顯示語言設定小卡
            return

        if text_for_command in 主選單指令:
            selected_codes = get_group_languages(db, group_id) if group_id else [user.target_language] if user else [DEFAULT_LANGUAGE_CODE]
            state_key = _狀態鍵(source_type, user_id, group_id)
            translation_enabled, auto_detect_enabled = _目前開關狀態(
                state_key,
                default_auto_detect=(source_type != "group"),
            )
            _reply_messages(
                reply_token,
                [
                    TextMessage(text="這是翻翻君主選單，請直接點擊小卡按鈕操作。", quickReply=None, quoteToken=None),
                    build_main_menu_card(
                        source_type=source_type,
                        is_group_manager=is_group_manager,
                        current_language_code=selected_codes[0] if selected_codes else DEFAULT_LANGUAGE_CODE,
                        translation_enabled=translation_enabled,
                        auto_detect_enabled=auto_detect_enabled,
                        vip_enabled=vip_enabled,
                    ),
                ],
            )  # 顯示主選單小卡
            return

        if text_for_command in 旅遊模式指令:
            current_language_code = _current_language_code(source_type, user, group_id, db)
            _reply_messages(
                reply_token,
                [
                    build_travel_mode_card(current_language_code),
                ],
            )
            return

        if text_for_command in 旅遊模式確認指令:
            if not user_id:
                _reply_text(reply_token, "無法識別使用者，請稍後再試。")
                return
            current_language_code = _current_language_code(source_type, user, group_id, db)
            travel_i18n = get_travel_i18n(current_language_code)
            mark_awaiting_location(user_id)
            _reply_messages(
                reply_token,
                [
                    TextMessage(
                        text=travel_i18n["location_prompt"],
                        quickReply=QuickReply(
                            items=[
                                QuickReplyItem(
                                    action=LocationAction(label=travel_i18n["location_quick_reply_label"]),
                                )
                            ]
                        ),
                        quoteToken=None,
                    )
                ],
            )
            return

        if text_for_command in 旅遊模式返回指令:
            selected_codes = get_group_languages(db, group_id) if group_id else [user.target_language] if user else [DEFAULT_LANGUAGE_CODE]
            state_key = _狀態鍵(source_type, user_id, group_id)
            translation_enabled, auto_detect_enabled = _目前開關狀態(
                state_key,
                default_auto_detect=(source_type != "group"),
            )
            _reply_messages(
                reply_token,
                [
                    build_main_menu_card(
                        source_type=source_type,
                        is_group_manager=is_group_manager,
                        current_language_code=selected_codes[0] if selected_codes else DEFAULT_LANGUAGE_CODE,
                        translation_enabled=translation_enabled,
                        auto_detect_enabled=auto_detect_enabled,
                        vip_enabled=vip_enabled,
                    ),
                ],
            )
            return

        if text_for_command in 說明指令:
            selected_codes = get_group_languages(db, group_id) if group_id else [user.target_language] if user else [DEFAULT_LANGUAGE_CODE]
            state_key = _狀態鍵(source_type, user_id, group_id)
            translation_enabled, auto_detect_enabled = _目前開關狀態(
                state_key,
                default_auto_detect=(source_type != "group"),
            )
            _reply_messages(
                reply_token,
                [
                    TextMessage(
                        text=_建立說明文字(source_type, is_group_manager),
                        quickReply=None,
                        quoteToken=None,
                    ),
                    build_main_menu_card(
                        source_type=source_type,
                        is_group_manager=is_group_manager,
                        current_language_code=selected_codes[0] if selected_codes else DEFAULT_LANGUAGE_CODE,
                        translation_enabled=translation_enabled,
                        auto_detect_enabled=auto_detect_enabled,
                        vip_enabled=vip_enabled,
                    ),
                ],
            )  # 顯示指令說明與主選單小卡
            return

        if text_for_command in 即時翻譯啟用指令:
            即時翻譯狀態[state_key] = True
            _reply_text(reply_token, "✅ 即時翻譯功能已開啟")
            return

        if text_for_command in 即時翻譯關閉指令:
            即時翻譯狀態[state_key] = False
            _reply_text(reply_token, "⛔ 即時翻譯功能已關閉")
            return

        if text_for_command in 自動偵測啟用指令:
            target_code = _自動偵測目標語言(source_type, user, group_id, db)
            target_label = _語言代碼轉名稱(target_code)
            自動偵測狀態[state_key] = True
            _reply_text(
                reply_token,
                f"✅ 已啟用自動偵測模式\n現在會優先偵測語言，遇到非{target_label}訊息時會翻譯成{target_label}。",
            )
            return

        if text_for_command in 自動偵測關閉指令:
            自動偵測狀態[state_key] = False
            _reply_text(reply_token, "⛔ 已關閉自動偵測模式")
            return

        if text.startswith("設定語言 "):
            selected_labels = parse_language_labels(text.replace("設定語言 ", "", 1).strip())  # 解析語言名稱
            if not selected_labels:
                _reply_text(reply_token, "請至少指定一種語言，例如：設定語言 中文")  # 參數不足
                return
            selected_codes: list[str] = []  # 有效語言代碼
            invalid_labels: list[str] = []  # 無效語言名稱
            for label in selected_labels:
                code = resolve_language_code(label)
                if code:
                    selected_codes.append(code)
                else:
                    invalid_labels.append(label)

            if invalid_labels:
                _reply_text(reply_token, f"以下語言不支援：{'、'.join(invalid_labels)}", with_language_menu=True)  # 語言不存在
                return

            unique_selected_codes: list[str] = []
            for code in selected_codes:
                if code not in unique_selected_codes:
                    unique_selected_codes.append(code)  # 保留順序並去重

            if source_type == "group" and group_id:
                group = current_group or ensure_group_exists(db, group_id)  # 取得群組設定
                if not can_manage_group(group, user, user_id):
                    _reply_text(reply_token, "你沒有群組設定權限，僅邀請者代表/管理員/所有者可設定。")  # 權限不足
                    return

                current_codes = get_group_languages(db, group_id)
                if len(unique_selected_codes) > 群組語言上限:
                    _reply_text(reply_token, "群組翻譯最多只能設定 2 種語言。")
                    return

                if len(unique_selected_codes) == 1 and len(selected_labels) == 1:
                    toggle_code = unique_selected_codes[0]
                    if toggle_code not in current_codes and len(current_codes) >= 群組語言上限:
                        _reply_text(reply_token, "群組翻譯最多只能設定 2 種語言，請先移除一種語言再新增。")
                        return

                updated_codes = toggle_or_set_languages(
                    db,
                    group_id,
                    unique_selected_codes,
                    toggle_single=(len(selected_codes) == 1 and len(selected_labels) == 1),
                )  # 使用舊版群組語言切換核心

                _reply_messages(
                    reply_token,
                    [
                        TextMessage(text=format_language_updated(updated_codes), quickReply=None, quoteToken=None),
                        build_language_setting_card(updated_codes, source_type, True),
                    ],
                )  # 顯示更新後小卡
                return

            if user:
                update_user_language(db, user, selected_codes[0])  # 更新個人語言（單語）
            _reply_messages(
                reply_token,
                [
                    TextMessage(text=format_language_updated([selected_codes[0]]), quickReply=None, quoteToken=None),
                    build_language_setting_card([selected_codes[0]], source_type, True),
                ],
            )  # 個人模式更新語言與顯示小卡
            return

        if text_for_command in 重設翻譯指令:
            if source_type == "group" and group_id:
                group = current_group or create_group(db, group_id)  # 取得群組資料
                if not can_manage_group(group, user, user_id):
                    _reply_text(reply_token, "此指令僅限邀請者代表/管理員/所有者使用。")  # 權限不足
                    return
                updated_codes = reset_languages(db, group_id)  # 重設群組翻譯語言
                _reply_messages(
                    reply_token,
                    [
                        TextMessage(text=format_language_updated(updated_codes), quickReply=None, quoteToken=None),
                        build_language_setting_card(updated_codes, source_type, True),
                    ],
                )  # 回覆重設成功並顯示小卡
                return

            if user:
                update_user_language(db, user, DEFAULT_LANGUAGE_CODE)  # 重設個人翻譯語言
            _reply_messages(
                reply_token,
                [
                    TextMessage(text=format_language_updated([DEFAULT_LANGUAGE_CODE]), quickReply=None, quoteToken=None),
                    build_language_setting_card([DEFAULT_LANGUAGE_CODE], source_type, True),
                ],
            )  # 個人模式重設成功並顯示小卡
            return

        if source_type == "group" and group_id and text_for_command in 管理員白名單指令:
            group = current_group or create_group(db, group_id)  # 取得群組資料
            if not can_manage_group(group, user, user_id):
                _reply_text(reply_token, "此指令僅限邀請者代表/管理員/所有者使用。")  # 白名單權限不足
                return

            if text == "查看群組設定":
                inviter_text = group.inviter_user_id if group.inviter_user_id else "尚未綁定"  # 邀請者代表資訊
                language_codes = get_group_languages(db, group_id)  # 取得群組語言清單
                language_label = _群組語言摘要(language_codes)  # 轉換語言名稱
                _reply_text(
                    reply_token,
                    f"群組設定：\n翻譯語言：{language_label}\n邀請者代表：{inviter_text}",
                )  # 顯示群組設定
                return

            if text == "重設邀請者":
                if not user_id:
                    _reply_text(reply_token, "無法識別使用者，請稍後重試。")  # 無使用者 ID
                    return
                set_group_inviter(db, group, user_id)  # 直接重設為目前使用者
                _reply_text(reply_token, "邀請者代表已重設為你，現在你可管理本群翻譯設定。")  # 回覆成功
                return

        if source_type == "group" and group_id and text == 綁定邀請者指令:
            if not user_id:
                _reply_text(reply_token, "無法識別使用者，請稍後重試。")  # 無法取得使用者
                return
            group = current_group or create_group(db, group_id)  # 取得群組資料
            if group.inviter_user_id and group.inviter_user_id != user_id:
                _reply_text(reply_token, "此群組邀請者代表已綁定，無法重複綁定。")  # 已被他人綁定
                return
            bind_group_inviter(db, group, user_id)  # 綁定邀請者代表
            _reply_text(reply_token, "邀請者代表綁定完成，現在你可管理本群翻譯語言。")  # 回覆成功
            return

        translation_enabled, auto_detect_enabled = _目前開關狀態(
            state_key,
            default_auto_detect=(source_type != "group"),
        )

        if source_type == "group" and group_id and 超管群組在場狀態.get(group_id, False):
            _reply_text(reply_token, "超級管理員在群組內 翻譯系統自動關閉")
            return

        if not translation_enabled:
            _reply_text(reply_token, "⛔ 目前即時翻譯功能為關閉中\n可點選主選單中的開啟按鈕恢復翻譯。")
            return

        target_code = DEFAULT_LANGUAGE_CODE  # 預設語言
        if source_type == "group" and group_id:
            group = current_group or create_group(db, group_id)  # 取得群組設定
            target_codes, smart_detect_notice = _智慧偵測群組語言(db, group_id, text)  # 智慧偵測第二語言
            translated_text = format_translation_results(text, target_codes, translate_text)  # 使用舊版核心輸出格式
            if smart_detect_notice:
                translated_text = f"{smart_detect_notice}\n\n{translated_text}"
            _reply_text(reply_token, translated_text)  # 回覆多語翻譯
            return
        elif user:
            target_code = user.target_language  # 採用個人語言

        if auto_detect_enabled:
            source_code = detect_source_language(text, [target_code])  # 判斷是否已是目標語言
            if source_code == target_code:
                _reply_text(reply_token, f"翻譯結果：\n{text}")  # 中文原文直接回傳
                return

        translate_func = translate_text_vip_pro if (source_type == "user" and vip_enabled) else translate_text
        translated = translate_func(text, target_code)  # 執行翻譯
        _reply_text(reply_token, f"翻譯結果：\n{translated}")  # 回覆翻譯結果


@line_handler.add(MemberJoinedEvent)
def handle_member_joined(event: MemberJoinedEvent) -> None:
    reply_token = event.reply_token
    group_id = getattr(event.source, "group_id", None)
    if not reply_token or not group_id:
        return

    joined = getattr(event, "joined", None)
    members = getattr(joined, "members", []) if joined else []
    for member in members:
        member_id = getattr(member, "user_id", None)
        if member_id == 超級管理員ID:
            超管群組在場狀態[group_id] = True
            即時翻譯狀態[_狀態鍵("group", None, group_id)] = False
            _reply_text(reply_token, "超級管理員在群組內 翻譯系統自動關閉")
            return


@line_handler.add(MemberLeftEvent)
def handle_member_left(event: MemberLeftEvent) -> None:
    reply_token = event.reply_token
    group_id = getattr(event.source, "group_id", None)
    if not reply_token or not group_id:
        return

    left = getattr(event, "left", None)
    members = getattr(left, "members", []) if left else []
    for member in members:
        member_id = getattr(member, "user_id", None)
        if member_id == 超級管理員ID:
            超管群組在場狀態[group_id] = False
            即時翻譯狀態[_狀態鍵("group", None, group_id)] = True
            _reply_text(reply_token, "超級管理員在群組內 翻譯系統自動開啟")
            return


def verify_signature(body: str, signature: str) -> None:
    try:
        line_handler.handle(body, signature)  # 驗證並分派事件
    except InvalidSignatureError as exc:
        raise ValueError("Invalid LINE signature") from exc  # 包裝簽章錯誤


@line_handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event: MessageEvent) -> None:
    reply_token = event.reply_token
    if not reply_token:
        return

    source_type = getattr(event.source, "type", "")
    user_id = getattr(event.source, "user_id", None)
    group_id = getattr(event.source, "group_id", None) if source_type == "group" else None

    latitude = getattr(event.message, "latitude", None)
    longitude = getattr(event.message, "longitude", None)
    if latitude is None or longitude is None:
        _reply_text(reply_token, "無法取得定位資訊，請再試一次。")
        return

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id) if user_id else None
        current_language_code = _current_language_code(source_type, user, group_id, db)
        travel_i18n = get_travel_i18n(current_language_code)
        vip_enabled = _vip是否啟用(get_vip_status(db, user_id) if user_id else None)

        if not user_id:
            _reply_text(reply_token, travel_i18n["not_enabled_yet"])
            return

        set_last_location(user_id, float(latitude), float(longitude))

        if not consume_awaiting_location(user_id):
            _reply_text(reply_token, travel_i18n["not_enabled_yet"])
            return

        try:
            result = build_travel_reply(float(latitude), float(longitude), current_language_code)
        except Exception:
            result = travel_i18n["temporary_unavailable"]
        progress_text = build_travel_progress_text(current_language_code)

        _reply_messages(
            reply_token,
            [
                TextMessage(text=progress_text, quickReply=None, quoteToken=None),
                TextMessage(text=result, quickReply=None, quoteToken=None),
                build_main_menu_card(
                    source_type=source_type,
                    is_group_manager=False,
                    current_language_code=current_language_code,
                    translation_enabled=True,
                    auto_detect_enabled=自動偵測狀態.get(_狀態鍵(source_type, user_id, group_id), source_type != "group"),
                    vip_enabled=vip_enabled,
                ),
            ],
        )


@line_handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event: MessageEvent) -> None:
    reply_token = event.reply_token
    if not reply_token:
        return

    source_type = getattr(event.source, "type", "")
    user_id = getattr(event.source, "user_id", None)
    group_id = getattr(event.source, "group_id", None) if source_type == "group" else None

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id) if user_id else None
        current_language_code = _current_language_code(source_type, user, group_id, db)
        travel_i18n = get_travel_i18n(current_language_code)

    if not user_id:
        _reply_text(reply_token, travel_i18n["audio_need_location"])
        return

    last_location = get_last_location(user_id)
    if not last_location:
        _reply_messages(
            reply_token,
            [
                TextMessage(
                    text=travel_i18n["audio_need_location"],
                    quickReply=QuickReply(
                        items=[QuickReplyItem(action=LocationAction(label=travel_i18n["location_quick_reply_label"]))]
                    ),
                    quoteToken=None,
                )
            ],
        )
        return

    message_id = str(getattr(event.message, "id", ""))
    if not message_id:
        _reply_text(reply_token, travel_i18n["audio_transcribe_failed"])
        return

    audio_bytes = _download_message_content(message_id)
    if not audio_bytes:
        _reply_text(reply_token, travel_i18n["audio_transcribe_failed"])
        return

    transcript = transcribe_audio_with_whisper_open_source(audio_bytes)
    if not transcript:
        _reply_text(reply_token, travel_i18n["audio_transcribe_failed"])
        return

    try:
        result = build_travel_reply(last_location[0], last_location[1], current_language_code, user_query=transcript)
    except Exception:
        result = travel_i18n["temporary_unavailable"]
    progress_text = build_travel_progress_text(current_language_code)

    _reply_messages(
        reply_token,
        [
            TextMessage(text=progress_text, quickReply=None, quoteToken=None),
            TextMessage(text=f"🎙 {transcript}\n\n{result}", quickReply=None, quoteToken=None),
        ],
    )
