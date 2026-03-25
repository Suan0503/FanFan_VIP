from linebot.v3.messaging import (  # 匯入 Flex 元件
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexMessage,
    FlexText,
    MessageAction,
)

from app.fanfan_core.language_profile import LEGACY_LANGUAGE_MENU_ITEMS, summarize_language_codes  # 匯入舊版語言選單


def build_legacy_language_setting_card(selected_codes: list[str], source_type: str, can_manage_group: bool) -> FlexMessage:
    title = "群組翻譯設定" if source_type == "group" else "個人翻譯設定"  # 標題
    subtitle = "請加上 / 取消要翻譯成的語言，可複選。" if source_type == "group" else "請選擇要翻譯成的語言。"  # 副標
    selected_text = summarize_language_codes(selected_codes)  # 已選摘要
    hint = "點擊下方語言按鈕即可切換勾選狀態。" if (source_type != "group" or can_manage_group) else "你目前沒有設定權限（需邀請者代表 / 管理員 / 所有者）。"  # 提示

    buttons: list[FlexButton] = []  # 語言按鈕集合
    for tag, pretty_name, command_name, code in LEGACY_LANGUAGE_MENU_ITEMS:
        selected = code in selected_codes  # 是否已勾選
        label = f"✅ {tag} {pretty_name}" if selected else f"{tag} {pretty_name}"  # 按鈕文字
        buttons.append(
            FlexButton(
                style="primary",
                color="#D9144E" if selected else "#FF6B57",
                action=MessageAction(label=label, text=f"設定語言 {command_name}"),
                margin="sm",
                height="sm",
            )
        )  # 加入語言按鈕

    buttons.append(
        FlexButton(
            style="secondary",
            action=MessageAction(label="🔁 重設翻譯設定", text="重設翻譯設定"),
            margin="md",
            height="sm",
        )
    )  # 加入重設按鈕

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
        body=FlexBox(layout="vertical", paddingAll="14px", spacing="sm", contents=buttons),
        footer=FlexBox(
            layout="vertical",
            paddingAll="12px",
            contents=[FlexText(text=f"✅ {hint}", size="xs", color="#6F6B6B", wrap=True)],
        ),
    )  # 舊版風格語言設定卡

    return FlexMessage(altText="翻翻君語言設定", contents=bubble, quickReply=None)  # 回傳語言卡
