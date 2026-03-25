from linebot.v3.messaging import (  # 匯入 Flex 訊息元件
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexMessage,
    FlexSeparator,
    FlexText,
    MessageAction,
)

from app.core.languages import SUPPORTED_LANGUAGES  # 匯入語言設定


LANGUAGE_MENU_ITEMS = [
    ("TW", "中文(台灣)", "中文", "zh-TW"),
    ("US", "英文", "英文", "en"),
    ("TH", "泰文", "泰文", "th"),
    ("VN", "越南文", "越南文", "vi"),
    ("MM", "緬甸文", "緬甸文", "my"),
    ("KR", "韓文", "韓文", "ko"),
    ("ID", "印尼文", "印尼文", "id"),
    ("JP", "日文", "日文", "ja"),
    ("RU", "俄文", "俄文", "ru"),
]  # 語言按鈕顯示設定


def _build_feature_button(label: str, command_text: str, color: str = "#4D62F4") -> FlexButton:
    return FlexButton(
        style="primary",
        color=color,
        action=MessageAction(label=label, text=command_text),
        height="sm",
        margin="sm",
    )  # 建立主選單按鈕


def build_main_menu_card(source_type: str, is_group_manager: bool) -> FlexMessage:
    group_tip = "群組中可複選語言，之後每句都會固定翻譯。"  # 群組功能描述
    group_action = "查看群組設定"  # 群組按鈕預設動作
    group_label = "👥 查看群組設定"  # 群組按鈕預設文字

    if source_type != "group":
        group_tip = "把翻翻君加入群組後，可開啟群組多語翻譯。"  # 個人聊天提示
        group_action = "指令說明"  # 個人聊天無群組設定
        group_label = "👥 群組功能說明"  # 個人聊天按鈕文字
    elif not is_group_manager:
        group_tip = "尚未取得群組設定權限，請先輸入：綁定邀請者"  # 權限不足提示
        group_action = "綁定邀請者"  # 直接提供綁定入口
        group_label = "🔐 綁定邀請者"  # 權限不足按鈕

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor="#F3F6FF",
            contents=[
                FlexText(text="翻翻君 VIP 功能選單", size="xl", weight="bold", color="#344054"),
                FlexText(text="翻譯、語言設定、群組管理一鍵操作", size="sm", color="#667085", margin="sm", wrap=True),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            spacing="sm",
            paddingAll="16px",
            contents=[
                _build_feature_button("🎯 語言翻譯設定", "語言設定", "#5569F5"),
                _build_feature_button("📘 指令使用說明", "指令說明", "#17B26A"),
                _build_feature_button(group_label, group_action, "#F79009"),
                _build_feature_button("🔄 重設翻譯設定", "重設翻譯設定", "#98A2B3") if source_type == "group" else _build_feature_button("🧭 開啟主選單", "主選單", "#98A2B3"),
            ],
        ),
        footer=FlexBox(
            layout="vertical",
            paddingAll="12px",
            contents=[
                FlexSeparator(margin="none"),
                FlexText(text=group_tip, size="xs", color="#667085", wrap=True, margin="md"),
            ],
        ),
    )  # 建立主選單卡片

    return FlexMessage(
        altText="翻翻君主選單",
        contents=bubble,
        quickReply=None,
    )  # 回傳 Flex 主選單


def build_language_setting_card(selected_codes: list[str], source_type: str, can_manage_group: bool) -> FlexMessage:
    title = "群組翻譯設定" if source_type == "group" else "個人翻譯設定"  # 卡片標題
    subtitle = "請加上 / 取消要翻譯成的語言，可複選。" if source_type == "group" else "請選擇要翻譯成的語言。"  # 卡片副標

    selected_labels = [name for name, code in SUPPORTED_LANGUAGES.items() if code in selected_codes]  # 已選語言名稱
    selected_text = "、".join(selected_labels) if selected_labels else "尚未設定"  # 已選語言摘要

    if source_type == "group" and not can_manage_group:
        permission_hint = "你目前沒有設定權限（需邀請者代表 / 管理員 / 所有者）。"  # 權限提示
    else:
        permission_hint = "點擊下方語言按鈕即可切換勾選狀態。"  # 操作提示

    button_contents = []  # 語言按鈕列表
    for tag, pretty_name, command_name, language_code in LANGUAGE_MENU_ITEMS:
        is_selected = language_code in selected_codes  # 是否已勾選
        label_text = f"✅ {tag} {pretty_name}" if is_selected else f"{tag} {pretty_name}"  # 文字樣式
        action_text = f"設定語言 {command_name}"  # 點擊送出的指令
        button_contents.append(
            FlexButton(
                style="primary",
                color="#D9144E" if is_selected else "#FF6B57",
                action=MessageAction(label=label_text, text=action_text),
                height="sm",
                margin="sm",
            )
        )  # 建立語言按鈕

    button_contents.append(
        FlexButton(
            style="secondary",
            action=MessageAction(label="🔁 重設翻譯設定", text="重設翻譯設定"),
            margin="md",
            height="sm",
        )
    )  # 建立重設按鈕

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor="#F8F3F5",
            contents=[
                FlexText(text=f"🎎 {title}", weight="bold", size="xl", color="#D9144E"),
                FlexText(text=subtitle, size="sm", color="#5B4F57", wrap=True, margin="sm"),
                FlexText(text="🎉 新年快樂 🎉", size="sm", color="#D9A300", align="center", margin="sm"),
                FlexText(text=f"目前勾選：{selected_text}", size="sm", color="#D9144E", wrap=True, margin="md"),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            paddingAll="14px",
            spacing="sm",
            contents=button_contents,
        ),
        footer=FlexBox(
            layout="vertical",
            paddingAll="12px",
            contents=[
                FlexText(text=f"✅ {permission_hint}", size="xs", color="#6F6B6B", wrap=True),
            ],
        ),
    )  # 建立語言設定卡片

    return FlexMessage(
        altText="翻翻君語言設定",
        contents=bubble,
        quickReply=None,
    )  # 回傳語言設定卡片
