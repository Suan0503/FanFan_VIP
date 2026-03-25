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
    update_group_language,
    bind_group_inviter,
    set_group_inviter,
)  # 匯入群組存取
from app.services.id_service import generate_member_code  # 匯入編號服務
from app.services.translation_service import translate_text  # 匯入翻譯服務
from app.services.permission_service import can_manage_group  # 匯入權限服務
from app.ui.language_menu import build_language_menu_quick_reply  # 匯入語言選單
from app.ui.menu_cards import build_main_menu_card  # 匯入主選單小卡


configuration = Configuration(access_token=settings.line_channel_access_token)  # 建立 LINE API 設定
line_handler = WebhookHandler(settings.line_channel_secret)  # 建立 webhook handler

語言選單指令 = {"語言設定", "語言選單", "選單"}  # 中文語言選單指令
主選單指令 = {"主選單", "功能選單", "選單小卡"}  # 中文主選單小卡指令
綁定邀請者指令 = "綁定邀請者"  # 綁定邀請者代表指令
管理員白名單指令 = {"查看群組設定", "重設邀請者"}  # 僅管理者可用的群組指令
說明指令 = {"指令說明", "使用說明", "幫助"}  # 顯示說明指令


def _語言代碼轉名稱(language_code: str) -> str:
    for language_name, code in SUPPORTED_LANGUAGES.items():
        if code == language_code:
            return language_name  # 找到對應語言名稱
    return f"未知語言({language_code})"  # 找不到時保留代碼


def _建立說明文字(source_type: str, is_group_manager: bool) -> str:
    lines = [
        "翻翻君指令說明：",
        "1. 語言設定 / 語言選單 / 選單",
        "   開啟語言快速選單。",
        "2. 設定語言 中文",
        "   可改成英文、泰文、越南文、緬甸文、韓文、印尼文、日文、俄文。",
        "3. 指令說明 / 使用說明 / 幫助",
        "   顯示這份說明。",
    ]  # 基礎說明

    if source_type == "group":
        lines.extend(
            [
                "4. 綁定邀請者",
                "   由群組第一位綁定者成為邀請者代表。",
                "5. 查看群組設定",
                "   查看本群翻譯語言與邀請者代表。",
                "6. 重設邀請者",
                "   把邀請者代表改成目前發送指令的人。",
            ]
        )  # 群組指令
        if not is_group_manager:
            lines.append("※ 查看群組設定 / 重設邀請者 僅限邀請者代表、管理員、所有者使用。")  # 權限說明

    return "\n".join(lines)  # 組合說明文字


def _reply_text(reply_token: str, message: str, with_language_menu: bool = False) -> None:
    quick_reply = build_language_menu_quick_reply() if with_language_menu else None  # 依需求加上語言選單
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
        f"感謝使用翻翻君！\n您的個人編號：{user.member_code}\n"
        f"目前翻譯語言：{DEFAULT_LANGUAGE_LABEL}\n"
        "可直接傳送文字，我會自動翻譯。\n"
        "你也可以點下方主選單小卡快速操作。"
    )  # 組合歡迎訊息
    _reply_messages(
        reply_token,
        [
            TextMessage(text=message, quickReply=build_language_menu_quick_reply(), quoteToken=None),
            build_main_menu_card(source_type="user", is_group_manager=False),
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
                text="翻翻君已加入群組！\n請邀請者輸入：綁定邀請者\n完成後僅邀請者代表、管理員、所有者可修改群組翻譯設定。",
                quickReply=None,
                quoteToken=None,
            ),
            build_main_menu_card(source_type="group", is_group_manager=False),
        ],
    )  # 回覆群組初始化提示與主選單小卡


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent) -> None:
    reply_token = event.reply_token  # 取得回覆 token
    if not reply_token:
        return  # 無法回覆就跳過

    text = getattr(event.message, "text", "").strip()  # 取得文字內容
    source_type = getattr(event.source, "type", "")  # 來源型別
    user_id = getattr(event.source, "user_id", None)  # 來源使用者
    group_id = getattr(event.source, "group_id", None) if source_type == "group" else None  # 來源群組

    with SessionLocal() as db:
        user = get_user_by_line_id(db, user_id) if user_id else None  # 查詢使用者資料
        if user_id and not user:
            member_code = generate_member_code(db)  # 產生新編號
            user = create_user(db, user_id, member_code, DEFAULT_LANGUAGE_CODE)  # 自動補建使用者

        if text in 語言選單指令:
            _reply_text(
                reply_token,
                "請選擇翻譯目標語言：",
                with_language_menu=True,
            )  # 顯示語言選單
            return

        current_group = get_group(db, group_id) if group_id else None  # 先讀取群組資料供說明與權限判斷使用
        is_group_manager = bool(current_group and can_manage_group(current_group, user, user_id))  # 是否具備群組管理權限

        if text in 主選單指令:
            _reply_messages(
                reply_token,
                [
                    TextMessage(text="這是翻翻君主選單，請直接點擊小卡按鈕操作。", quickReply=None, quoteToken=None),
                    build_main_menu_card(source_type=source_type, is_group_manager=is_group_manager),
                ],
            )  # 顯示主選單小卡
            return

        if text in 說明指令:
            _reply_messages(
                reply_token,
                [
                    TextMessage(
                        text=_建立說明文字(source_type, is_group_manager),
                        quickReply=build_language_menu_quick_reply(),
                        quoteToken=None,
                    ),
                    build_main_menu_card(source_type=source_type, is_group_manager=is_group_manager),
                ],
            )  # 顯示指令說明與主選單小卡
            return

        if text.startswith("設定語言 "):
            selected_label = text.replace("設定語言 ", "", 1).strip()  # 取出語言名稱
            if selected_label not in SUPPORTED_LANGUAGES:
                _reply_text(reply_token, "語言不支援，請重新選擇。", with_language_menu=True)  # 語言不存在
                return
            selected_code = SUPPORTED_LANGUAGES[selected_label]  # 取得語言代碼

            if source_type == "group" and group_id:
                group = current_group or create_group(db, group_id)  # 取得群組設定
                if not can_manage_group(group, user, user_id):
                    _reply_text(reply_token, "你沒有群組設定權限，僅邀請者代表/管理員/所有者可設定。")  # 權限不足
                    return
                update_group_language(db, group, selected_code)  # 更新群組語言
                _reply_text(reply_token, f"群組翻譯語言已設定為：{selected_label}")  # 回覆成功
                return

            if user:
                update_user_language(db, user, selected_code)  # 更新個人語言
            _reply_text(reply_token, f"個人翻譯語言已設定為：{selected_label}")  # 回覆成功
            return

        if source_type == "group" and group_id and text in 管理員白名單指令:
            group = current_group or create_group(db, group_id)  # 取得群組資料
            if not can_manage_group(group, user, user_id):
                _reply_text(reply_token, "此指令僅限邀請者代表/管理員/所有者使用。")  # 白名單權限不足
                return

            if text == "查看群組設定":
                inviter_text = group.inviter_user_id if group.inviter_user_id else "尚未綁定"  # 邀請者代表資訊
                language_label = _語言代碼轉名稱(group.target_language)  # 轉換語言名稱
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

        target_code = DEFAULT_LANGUAGE_CODE  # 預設語言
        if source_type == "group" and group_id:
            group = current_group or create_group(db, group_id)  # 取得群組設定
            target_code = group.target_language  # 採用群組語言
        elif user:
            target_code = user.target_language  # 採用個人語言

        translated = translate_text(text, target_code)  # 執行翻譯
        _reply_text(reply_token, f"翻譯結果：\n{translated}")  # 回覆翻譯結果


def verify_signature(body: str, signature: str) -> None:
    try:
        line_handler.handle(body, signature)  # 驗證並分派事件
    except InvalidSignatureError as exc:
        raise ValueError("Invalid LINE signature") from exc  # 包裝簽章錯誤
