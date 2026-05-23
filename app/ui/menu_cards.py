from linebot.v3.messaging import (  # 匯入 Flex 訊息元件
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexMessage,
    FlexFiller,
    FlexSeparator,
    FlexText,
    MessageAction,
)

from app.core.languages import SUPPORTED_LANGUAGES  # 匯入語言設定


BRAND_NAME = "FanFan VIP"  # 品牌名稱
THEME_BG_DARK = "#0B1220"  # 主底色
THEME_BG_DEEP = "#14213D"  # 主要區塊深藍
THEME_GOLD = "#D4AF37"  # 強調金色
THEME_MUTED = "#94A3B8"  # 輔助灰
THEME_WHITE = "#F8FAFC"  # 文字亮色
THEME_SUCCESS = "#22C55E"  # 啟用綠色
THEME_DANGER = "#EF4444"  # 關閉紅色
THEME_PERSONAL = "#1E3A8A"  # 個人模式主色
THEME_PERSONAL_LIGHT = "#1D4ED8"  # 個人模式標題色（加深提升可讀性）
THEME_GROUP = "#14213D"  # 群組模式深藍


LANGUAGE_MENU_ITEMS = [
    ("TW", "中文(台灣)", "中文", "zh-TW"),
    ("US", "英文", "英文", "en"),
    ("JP", "日文", "日文", "ja"),
    ("TH", "泰文", "泰文", "th"),
    ("VN", "越南文", "越南文", "vi"),
    ("MM", "緬甸文", "緬甸文", "my"),
    ("KR", "韓文", "韓文", "ko"),
    ("ID", "印尼文", "印尼文", "id"),
    ("RU", "俄文", "俄文", "ru"),
]  # 語言按鈕顯示設定

QUICK_LANGUAGE_ITEMS = [
    ("zh-TW", "TW中文", "設定語言 中文"),
    ("en", "US英文", "設定語言 英文"),
    ("th", "TH泰文", "設定語言 泰文"),
    ("ja", "JP日文", "設定語言 日文"),
    ("vi", "VN越南文", "設定語言 越南文"),
    ("ko", "KR韓文", "設定語言 韓文"),
    ("id", "ID印尼文", "設定語言 印尼文"),
    ("my", "MM緬甸文", "設定語言 緬甸文"),
    ("ru", "RU俄文", "設定語言 俄文"),
]  # 快速切換語言（雙欄）


def _language_label_by_code(language_code: str) -> str:
    for code, display_label, _ in QUICK_LANGUAGE_ITEMS:
        if code == language_code:
            return display_label  # 轉成卡片顯示語言
    for language_name, code in SUPPORTED_LANGUAGES.items():
        if code == language_code:
            return language_name  # 回退一般語言名稱
    return "未設定"  # 防禦性回傳


def _build_feature_button(label: str, command_text: str, button_color: str) -> FlexButton:
    return FlexButton(
        style="primary",
        color=button_color,
        action=MessageAction(label=label, text=command_text),
        cornerRadius="14px",
        height="sm",
        margin="md",
    )  # 建立主選單按鈕


def _build_language_chip(language_code: str, label: str, command_text: str, current_language_code: str) -> FlexButton:
    selected = language_code == current_language_code
    return FlexButton(
        style="primary",
        color=THEME_GOLD if selected else THEME_BG_DARK,
        action=MessageAction(label=f"✅ {label}" if selected else label, text=command_text),
        cornerRadius="18px",
        margin="sm",
        height="sm",
    )  # 建立熱門語言雙欄卡片


def _build_status_text(label: str, enabled: bool) -> FlexText:
    return FlexText(
        text=f"{label} - {'啟用中' if enabled else '關閉中'}",
        size="xs",
        color=THEME_SUCCESS if enabled else THEME_DANGER,
        margin="sm",
        weight="bold",
    )  # 建立狀態文字


def _build_status_toggle_row(label: str, enabled: bool, on_command: str, off_command: str) -> FlexBox:
    toggle_label = "關" if enabled else "開"
    toggle_command = off_command if enabled else on_command
    toggle_color = THEME_DANGER if enabled else THEME_SUCCESS
    return FlexBox(
        layout="horizontal",
        spacing="sm",
        margin="sm",
        contents=[
            FlexBox(
                layout="vertical",
                flex=7,
                contents=[_build_status_text(label, enabled)],
            ),
            FlexBox(
                layout="vertical",
                flex=3,
                justifyContent="center",
                contents=[
                    FlexButton(
                        style="primary",
                        color=toggle_color,
                        action=MessageAction(label=toggle_label, text=toggle_command),
                        cornerRadius="8px",
                        height="sm",
                    )
                ],
            ),
        ],
    )  # 建立狀態列與切換按鈕


def _build_quick_language_section(
    current_language_code: str,
    mode_button_color: str,
    auto_detect_enabled: bool,
) -> list[FlexBox | FlexText | FlexSeparator | FlexButton]:
    row_top = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(QUICK_LANGUAGE_ITEMS[0][0], QUICK_LANGUAGE_ITEMS[0][1], QUICK_LANGUAGE_ITEMS[0][2], current_language_code),
        ],
    )
    row_one = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(QUICK_LANGUAGE_ITEMS[1][0], QUICK_LANGUAGE_ITEMS[1][1], QUICK_LANGUAGE_ITEMS[1][2], current_language_code),
            _build_language_chip(QUICK_LANGUAGE_ITEMS[2][0], QUICK_LANGUAGE_ITEMS[2][1], QUICK_LANGUAGE_ITEMS[2][2], current_language_code),
        ],
    )
    row_two = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(QUICK_LANGUAGE_ITEMS[3][0], QUICK_LANGUAGE_ITEMS[3][1], QUICK_LANGUAGE_ITEMS[3][2], current_language_code),
            _build_language_chip(QUICK_LANGUAGE_ITEMS[4][0], QUICK_LANGUAGE_ITEMS[4][1], QUICK_LANGUAGE_ITEMS[4][2], current_language_code),
        ],
    )
    row_three = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(QUICK_LANGUAGE_ITEMS[5][0], QUICK_LANGUAGE_ITEMS[5][1], QUICK_LANGUAGE_ITEMS[5][2], current_language_code),
            _build_language_chip(QUICK_LANGUAGE_ITEMS[6][0], QUICK_LANGUAGE_ITEMS[6][1], QUICK_LANGUAGE_ITEMS[6][2], current_language_code),
        ],
    )
    row_four = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(QUICK_LANGUAGE_ITEMS[7][0], QUICK_LANGUAGE_ITEMS[7][1], QUICK_LANGUAGE_ITEMS[7][2], current_language_code),
            _build_language_chip(QUICK_LANGUAGE_ITEMS[8][0], QUICK_LANGUAGE_ITEMS[8][1], QUICK_LANGUAGE_ITEMS[8][2], current_language_code),
        ],
    )

    return [
        FlexSeparator(margin="xl"),
        FlexText(text="🌏 快速切換語言", size="sm", color=THEME_WHITE, weight="bold", margin="xl"),
        _build_feature_button(
            f"🧠 {'開啟中' if auto_detect_enabled else '關閉中'} 自動偵測模式（非中文訊息 -> 中文）",
            "關閉自動偵測" if auto_detect_enabled else "啟用自動偵測",
            mode_button_color,
        ),
        row_top,
        row_one,
        row_two,
        row_three,
        row_four,
    ]  # 建立語言雙欄區


def build_main_menu_card(
    source_type: str,
    is_group_manager: bool,
    current_language_code: str = "zh-TW",
    translation_enabled: bool = True,
    auto_detect_enabled: bool = False,
) -> FlexMessage:
    is_group_mode = source_type == "group"  # 判斷目前模式
    mode_name = "群組翻譯模式" if is_group_mode else "個人模式"  # 模式名稱
    mode_banner_color = THEME_GROUP if is_group_mode else THEME_PERSONAL_LIGHT  # 模式色系
    mode_button_color = THEME_GROUP if is_group_mode else THEME_PERSONAL  # 模式按鈕主色
    group_tip = "群組中可複選語言，之後每句都會固定翻譯。"  # 群組功能描述
    group_action = "查看群組設定"  # 群組按鈕預設動作
    group_label = "👥【群組翻譯】群組語言管理"  # 群組按鈕預設文字

    if source_type != "group":
        group_tip = "把翻翻君加入群組後，可開啟群組多語翻譯。"  # 個人聊天提示
        group_action = "指令說明"  # 個人聊天無群組設定
        group_label = "👥【群組翻譯】群組功能說明"  # 個人聊天按鈕文字
    elif not is_group_manager:
        group_tip = "尚未取得群組設定權限，請先輸入：綁定邀請者"  # 權限不足提示
        group_action = "綁定邀請者"  # 直接提供綁定入口
        group_label = "👥【群組翻譯】綁定邀請者"  # 權限不足按鈕

    main_actions: list[FlexBox | FlexText | FlexSeparator | FlexButton] = []
    main_actions.extend(_build_quick_language_section(current_language_code, mode_button_color, auto_detect_enabled))

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor=mode_banner_color,
            contents=[
                FlexText(text="翻翻君 - V1.0正式版", size="sm", color=THEME_GOLD, weight="bold"),
                FlexText(text="選單控制中心", size="xxl", weight="bold", color=THEME_WHITE, margin="sm"),
                _build_status_toggle_row("即時翻譯功能", translation_enabled, "開啟即時翻譯", "關閉即時翻譯"),
                _build_status_toggle_row("自動偵測文字", auto_detect_enabled, "啟用自動偵測", "關閉自動偵測"),
                FlexText(text="當前版本 - V1.0.0 免費版", size="xs", color=THEME_WHITE, margin="md"),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            spacing="sm",
            paddingAll="16px",
            backgroundColor=mode_button_color,
            contents=main_actions,
        ),
        footer=FlexBox(
            layout="vertical",
            paddingAll="12px",
            backgroundColor=THEME_BG_DARK,
            contents=[
                FlexText(text=f"當前使用模式 - {mode_name}", size="sm", color=THEME_GOLD, weight="bold"),
                FlexText(text=group_tip, size="xs", color=THEME_MUTED, wrap=True, margin="sm"),
                FlexText(text="使用教學:", size="xs", color=THEME_WHITE, weight="bold", margin="md"),
                FlexText(text="1. 先用上方語言按鈕設定可翻譯語言", size="xs", color=THEME_MUTED, wrap=True, margin="xs"),
                FlexText(text="2. 點擊自動偵測可啟用非中文 -> 中文翻譯", size="xs", color=THEME_MUTED, wrap=True, margin="xs"),
                FlexText(text="3. 群組模式可複選語言並自動互譯", size="xs", color=THEME_MUTED, wrap=True, margin="xs"),
                FlexText(text="4. 輸入 /menu 或 /選單 可隨時重開控制中心", size="xs", color=THEME_MUTED, wrap=True, margin="xs"),
                _build_feature_button("📘【教學中心】快速上手與完整教學", "指令說明", mode_button_color),
                _build_feature_button(group_label, group_action, mode_button_color),
                _build_feature_button("⭐【VIP 功能】DeepL Pro｜高階翻譯能力", "指令說明", mode_button_color),
            ],
        ),
    )  # 建立主選單卡片

    return FlexMessage(
        altText="翻翻君主選單",
        contents=bubble,
        quickReply=None,
    )  # 回傳 Flex 主選單


def build_language_setting_card(
    selected_codes: list[str],
    source_type: str,
    can_manage_group: bool,
    is_paid_member: bool = False,
    today_translated_chars: int = 0,
    translation_limit: int = 3000,
) -> FlexMessage:
    title = "🌐 群組翻譯設定" if source_type == "group" else "🌐 個人翻譯設定"  # 卡片標題
    subtitle = "請加上 / 取消要翻譯成的語言，可複選。" if source_type == "group" else "請選擇要翻譯成的語言。"  # 卡片副標

    selected_labels = [name for name, code in SUPPORTED_LANGUAGES.items() if code in selected_codes]  # 已選語言名稱
    selected_text = "、".join(selected_labels) if selected_labels else "尚未設定"  # 已選語言摘要
    current_code = selected_codes[0] if selected_codes else "zh-TW"  # 個人模式目前語言
    current_label = _language_label_by_code(current_code)  # 個人模式語言顯示文字

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
                color=THEME_GOLD if is_selected else THEME_BG_DEEP,
                action=MessageAction(label=label_text, text=action_text),
                cornerRadius="14px",
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

    button_contents.append(
        FlexButton(
            style="secondary",
            action=MessageAction(label="🏠 回主選單", text="/menu"),
            margin="md",
            height="sm",
        )
    )  # 回主選單按鈕

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor=THEME_BG_DARK,
            contents=[
                FlexText(text=title, weight="bold", size="xl", color=THEME_GOLD),
                FlexText(text=subtitle, size="sm", color=THEME_MUTED, wrap=True, margin="sm"),
                FlexSeparator(margin="md"),
                FlexText(text=f"目前翻譯語言 : {current_label}", size="sm", color=THEME_WHITE, wrap=True, margin="md"),
                FlexText(text=f"版本狀態 : {'付費版會員' if is_paid_member else '免費版'}", size="sm", color=THEME_WHITE, margin="sm"),
                FlexText(text=f"今日翻譯字數 : {today_translated_chars}", size="sm", color=THEME_WHITE, margin="sm"),
                FlexText(text=f"版本翻譯上限 : {translation_limit}", size="sm", color=THEME_WHITE, margin="sm"),
                FlexFiller(),
                FlexText(text=f"目前勾選：{selected_text}", size="xs", color=THEME_MUTED, wrap=True, margin="md"),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            paddingAll="14px",
            spacing="sm",
            backgroundColor=THEME_BG_DEEP,
            contents=button_contents,
        ),
        footer=FlexBox(
            layout="vertical",
            paddingAll="12px",
            backgroundColor=THEME_BG_DARK,
            contents=[
                FlexText(text=f"✅ {permission_hint}", size="xs", color=THEME_MUTED, wrap=True),
            ],
        ),
    )  # 建立語言設定卡片

    return FlexMessage(
        altText="翻翻君語言設定",
        contents=bubble,
        quickReply=None,
    )  # 回傳語言設定卡片


def build_main_menu_json(source_type: str, is_group_manager: bool, current_language_code: str = "zh-TW") -> dict:
    menu_message = build_main_menu_card(source_type, is_group_manager, current_language_code)  # 產生主選單
    if hasattr(menu_message, "to_dict"):
        return menu_message.to_dict()  # 轉為完整 Flex Message JSON
    return {"altText": menu_message.alt_text, "contents": {}}  # 防禦性回傳
