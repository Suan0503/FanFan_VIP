from linebot.v3.messaging import (  # 匯入 Flex 訊息元件
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexCarousel,
    FlexMessage,
    FlexText,
    MessageAction,
)

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
