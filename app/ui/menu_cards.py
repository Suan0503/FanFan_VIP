from linebot.v3.messaging import (  # 匯入 Flex 訊息元件
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexCarousel,
    FlexMessage,
    FlexText,
    MessageAction,
)

from app.core.languages import SUPPORTED_LANGUAGES  # 匯入語言設定
from app.ui.language_menu import build_language_menu_quick_reply  # 匯入語言快速選單


def _build_menu_bubble(title: str, subtitle: str, description: str, primary_label: str, primary_text: str, secondary_label: str | None = None, secondary_text: str | None = None, accent_color: str = "#5B6CFF") -> FlexBubble:
    footer_contents = [
        FlexButton(
            style="primary",
            color=accent_color,
            action=MessageAction(label=primary_label, text=primary_text),
            height="sm",
        )
    ]  # 主要按鈕

    if secondary_label and secondary_text:
        footer_contents.append(
            FlexButton(
                style="secondary",
                action=MessageAction(label=secondary_label, text=secondary_text),
                height="sm",
                margin="md",
            )
        )  # 次要按鈕

    return FlexBubble(
        size="mega",
        header=FlexBox(
            layout="vertical",
            paddingAll="20px",
            backgroundColor=accent_color,
            contents=[
                FlexText(text=subtitle, color="#FFFFFFCC", size="sm", weight="bold"),
                FlexText(text=title, color="#FFFFFF", size="xl", weight="bold", margin="sm", wrap=True),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            paddingAll="20px",
            spacing="md",
            contents=[
                FlexText(text=description, wrap=True, color="#333333", size="sm"),
            ],
        ),
        footer=FlexBox(
            layout="vertical",
            spacing="sm",
            paddingAll="16px",
            contents=footer_contents,
        ),
    )  # 建立單張選單卡


def build_main_menu_card(source_type: str, is_group_manager: bool) -> FlexMessage:
    group_description = "可綁定邀請者、查看本群設定。"  # 預設群組描述
    group_secondary_label = "查看群組設定"  # 預設群組次按鈕
    group_secondary_text = "查看群組設定"  # 預設群組次動作

    if source_type != "group":
        group_description = "群組功能需把翻翻君加入 LINE 群組後才能使用。"  # 個人聊天提示
        group_secondary_label = "指令說明"  # 個人聊天改成說明
        group_secondary_text = "指令說明"  # 個人聊天改成說明
    elif not is_group_manager:
        group_description = "先輸入綁定邀請者；之後僅邀請者代表、管理員、所有者可管理。"  # 未授權群組提示
        group_secondary_label = "綁定邀請者"  # 未授權時提供綁定入口
        group_secondary_text = "綁定邀請者"  # 未授權時提供綁定入口

    carousel = FlexCarousel(
        contents=[
            _build_menu_bubble(
                title="語言設定",
                subtitle="翻譯功能",
                description="快速選擇中文、英文、泰文、越南文、緬甸文、韓文、印尼文、日文、俄文。",
                primary_label="開啟語言",
                primary_text="語言設定",
                secondary_label="設為英文",
                secondary_text="設定語言 英文",
                accent_color="#5B6CFF",
            ),
            _build_menu_bubble(
                title="使用說明",
                subtitle="功能導覽",
                description="查看全部中文指令、操作方式與群組權限規則。",
                primary_label="查看說明",
                primary_text="指令說明",
                secondary_label="開啟主選單",
                secondary_text="主選單",
                accent_color="#00A889",
            ),
            _build_menu_bubble(
                title="群組管理",
                subtitle="權限設定",
                description=group_description,
                primary_label="群組功能",
                primary_text="綁定邀請者" if source_type == "group" else "指令說明",
                secondary_label=group_secondary_label,
                secondary_text=group_secondary_text,
                accent_color="#FF8A3D",
            ),
        ]
    )  # 建立輪播小卡

    return FlexMessage(
        altText="翻翻君主選單",
        contents=carousel,
        quickReply=build_language_menu_quick_reply(),
    )  # 回傳 Flex 主選單


def build_language_setting_card(selected_codes: list[str], source_type: str, can_manage_group: bool) -> FlexMessage:
    title = "群組翻譯設定" if source_type == "group" else "個人翻譯設定"  # 卡片標題
    subtitle = "請加上 / 取消翻譯語言，可複選。" if source_type == "group" else "請選擇要翻譯成的語言。"  # 卡片副標

    selected_labels = [name for name, code in SUPPORTED_LANGUAGES.items() if code in selected_codes]  # 已選語言名稱
    selected_text = "、".join(selected_labels) if selected_labels else "尚未設定"  # 已選語言摘要

    if source_type == "group" and not can_manage_group:
        permission_hint = "你目前沒有設定權限（需邀請者代表 / 管理員 / 所有者）。"  # 權限提示
    else:
        permission_hint = "點擊下方語言按鈕即可切換勾選狀態。"  # 操作提示

    button_contents = []  # 語言按鈕列表
    for language_name, language_code in SUPPORTED_LANGUAGES.items():
        is_selected = language_code in selected_codes  # 是否已勾選
        label_prefix = "✅ " if is_selected else "☐ "  # 勾選狀態圖示
        action_text = f"設定語言 {language_name}"  # 點擊送出的指令
        button_contents.append(
            FlexButton(
                style="primary" if is_selected else "secondary",
                color="#D9144E" if is_selected else "#FF6B57",
                action=MessageAction(label=f"{label_prefix}{language_name}", text=action_text),
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
            backgroundColor="#F6EEF1",
            contents=[
                FlexText(text=f"🎎 {title}", weight="bold", size="xl", color="#D9144E"),
                FlexText(text=subtitle, size="sm", color="#564A4A", wrap=True, margin="sm"),
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
                FlexText(text=permission_hint, size="xs", color="#6F6B6B", wrap=True),
            ],
        ),
    )  # 建立語言設定卡片

    return FlexMessage(
        altText="翻翻君語言設定",
        contents=bubble,
        quickReply=build_language_menu_quick_reply(),
    )  # 回傳語言設定卡片
