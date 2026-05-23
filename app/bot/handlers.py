from linebot.v3 import WebhookHandler  # 匯入 Webhook Handler
from linebot.v3.exceptions import InvalidSignatureError  # 匯入簽章錯誤
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    FlexMessage,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)  # 匯入 Messaging API
from linebot.v3.webhooks import FollowEvent, JoinEvent, MessageEvent, TextMessageContent  # 匯入事件型別

from app.core.config import settings  # 匯入設定
from app.core.languages import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE_CODE, DEFAULT_LANGUAGE_LABEL  # 匯入語言設定
from app.db.session import SessionLocal  # 匯入資料庫 Session
from app.repositories.user_repository import get_user_by_line_id, create_user, update_user_language  # 匯入使用者存取
from app.repositories.group_repository import (
    get_group,
    create_group,
    bind_group_inviter,
    set_group_inviter,
    get_group_languages,
)  # 匯入群組存取
from app.services.id_service import generate_member_code  # 匯入編號服務
from app.services.translation_service import translate_text  # 匯入翻譯服務
from app.services.permission_service import can_manage_group  # 匯入權限服務
from app.ui.menu_cards import build_main_menu_card, build_language_setting_card  # 匯入新版 Flex 小卡
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

即時翻譯狀態: dict[str, bool] = {}  # 依使用情境保存即時翻譯開關
自動偵測狀態: dict[str, bool] = {}  # 依使用情境保存自動偵測開關


def _狀態鍵(source_type: str, user_id: str | None, group_id: str | None) -> str:
    if source_type == "group" and group_id:
        return f"group:{group_id}"  # 群組模式鍵
    return f"user:{user_id or 'anonymous'}"  # 個人模式鍵


def _目前開關狀態(state_key: str, default_auto_detect: bool) -> tuple[bool, bool]:
    translation_enabled = 即時翻譯狀態.get(state_key, True)  # 預設開啟即時翻譯
    auto_detect_enabled = 自動偵測狀態.get(state_key, default_auto_detect)  # 預設依語言狀態決定
    return translation_enabled, auto_detect_enabled


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


def _標準化指令文字(text: str) -> str:
    normalized = text.strip()  # 清理首尾空白
    while normalized.startswith(("/", "／")):
        normalized = normalized[1:].strip()  # 移除開頭斜線
    return normalized  # 回傳正規化後指令


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
    ]  # 基礎說明

    if source_type == "group":
        lines.extend(
            [
                "6. 綁定邀請者",
                "   由群組第一位綁定者成為邀請者代表。",
                "7. 設定語言 中文、泰文",
                "   群組可複選語言，之後每句都會翻譯成多語。",
                "8. 重設翻譯設定",
                "   把群組翻譯語言重設成中文。",
                "9. 查看群組設定",
                "   查看本群翻譯語言與邀請者代表。",
                "10. 重設邀請者",
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

    message = (
        "歡迎加入翻翻君 VIP！\n"
        f"你的會員編號：{user.member_code}\n"
        f"預設翻譯語言：{DEFAULT_LANGUAGE_LABEL}\n"
        "預設翻譯通道：DeepL\n\n"
        "快速上手：\n"
        "1. 直接傳訊息，我會即時翻譯\n"
        "2. 輸入 /選單 或 /menu 開啟功能選單\n"
        "3. 輸入 語言設定 可切換常用語言\n"
        "4. 輸入 指令說明 查看完整教學"
    )  # 組合歡迎與教學訊息
    _reply_messages(
        reply_token,
        [
            TextMessage(text=message, quickReply=None, quoteToken=None),
            build_main_menu_card(source_type="user", is_group_manager=False, current_language_code=DEFAULT_LANGUAGE_CODE),
        ],
    )  # 回覆歡迎訊息與主選單小卡


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
                text="翻翻君已加入群組！\n請先輸入 /選單 或 /menu 開啟功能選單。\n若要管理群組語言，請邀請者再輸入：綁定邀請者。",
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

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id) if user_id else None  # 查詢使用者資料
        if user_id and not user:
            member_code = generate_member_code(db)  # 產生新編號
            user = create_user(db, user_id, member_code, DEFAULT_LANGUAGE_CODE)  # 自動補建使用者

        current_group = get_group(db, group_id) if group_id else None  # 先讀取群組資料供說明與權限判斷使用
        is_group_manager = bool(current_group and can_manage_group(current_group, user, user_id))  # 是否具備群組管理權限

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
                default_auto_detect=(source_type != "group" and (selected_codes[0] if selected_codes else DEFAULT_LANGUAGE_CODE) == DEFAULT_LANGUAGE_CODE),
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
                    ),
                ],
            )  # 顯示主選單小卡
            return

        if text_for_command in 說明指令:
            selected_codes = get_group_languages(db, group_id) if group_id else [user.target_language] if user else [DEFAULT_LANGUAGE_CODE]
            state_key = _狀態鍵(source_type, user_id, group_id)
            translation_enabled, auto_detect_enabled = _目前開關狀態(
                state_key,
                default_auto_detect=(source_type != "group" and (selected_codes[0] if selected_codes else DEFAULT_LANGUAGE_CODE) == DEFAULT_LANGUAGE_CODE),
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
                    ),
                ],
            )  # 顯示指令說明與主選單小卡
            return

        state_key = _狀態鍵(source_type, user_id, group_id)

        if text_for_command in 即時翻譯啟用指令:
            即時翻譯狀態[state_key] = True
            _reply_text(reply_token, "✅ 即時翻譯功能已開啟")
            return

        if text_for_command in 即時翻譯關閉指令:
            即時翻譯狀態[state_key] = False
            _reply_text(reply_token, "⛔ 即時翻譯功能已關閉")
            return

        if text_for_command in 自動偵測啟用指令:
            if user:
                update_user_language(db, user, DEFAULT_LANGUAGE_CODE)  # 自動偵測模式預設翻成中文
            自動偵測狀態[state_key] = True
            _reply_text(
                reply_token,
                "✅ 已啟用自動偵測模式\n現在會優先偵測語言，遇到非中文訊息會翻譯成中文。",
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

            if source_type == "group" and group_id:
                group = current_group or ensure_group_exists(db, group_id)  # 取得群組設定
                if not can_manage_group(group, user, user_id):
                    _reply_text(reply_token, "你沒有群組設定權限，僅邀請者代表/管理員/所有者可設定。")  # 權限不足
                    return
                updated_codes = toggle_or_set_languages(
                    db,
                    group_id,
                    selected_codes,
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
            default_auto_detect=(source_type != "group" and (user.target_language if user else DEFAULT_LANGUAGE_CODE) == DEFAULT_LANGUAGE_CODE),
        )

        if not translation_enabled:
            _reply_text(reply_token, "⛔ 目前即時翻譯功能為關閉中\n可點選主選單中的開啟按鈕恢復翻譯。")
            return

        target_code = DEFAULT_LANGUAGE_CODE  # 預設語言
        if source_type == "group" and group_id:
            group = current_group or create_group(db, group_id)  # 取得群組設定
            target_codes = get_group_languages(db, group_id)  # 採用群組多語設定
            translated_text = format_translation_results(text, target_codes, translate_text)  # 使用舊版核心輸出格式
            _reply_text(reply_token, translated_text)  # 回覆多語翻譯
            return
        elif user:
            target_code = user.target_language  # 採用個人語言

        if auto_detect_enabled and target_code == DEFAULT_LANGUAGE_CODE:
            source_code = detect_source_language(text, [DEFAULT_LANGUAGE_CODE])  # 判斷是否已是中文
            if source_code == DEFAULT_LANGUAGE_CODE:
                _reply_text(reply_token, f"翻譯結果：\n{text}")  # 中文原文直接回傳
                return

        translated = translate_text(text, target_code)  # 執行翻譯
        _reply_text(reply_token, f"翻譯結果：\n{translated}")  # 回覆翻譯結果


def verify_signature(body: str, signature: str) -> None:
    try:
        line_handler.handle(body, signature)  # 驗證並分派事件
    except InvalidSignatureError as exc:
        raise ValueError("Invalid LINE signature") from exc  # 包裝簽章錯誤
