from linebot.v3.messaging import (
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexMessage,
    FlexFiller,
    FlexSeparator,
    FlexText,
    MessageAction,
)

from app.core.languages import SUPPORTED_LANGUAGES
from app.ui.menu_registry import get_menu_i18n
from app.ui.menu_schema import MenuI18n


BRAND_NAME = "FanFan VIP"
THEME_BG_DARK = "#0B1220"
THEME_BG_DEEP = "#14213D"
THEME_GOLD = "#D4AF37"
THEME_MUTED = "#94A3B8"
THEME_WHITE = "#F8FAFC"
THEME_SUCCESS = "#22C55E"
THEME_DANGER = "#64748B"
THEME_PERSONAL = "#1E3A8A"
THEME_PERSONAL_LIGHT = "#1D4ED8"
THEME_GROUP = "#14213D"
LINE_ACTION_LABEL_MAX = 40


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
]

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
]


def _language_label_by_code(language_code: str) -> str:
    for code, display_label, _ in QUICK_LANGUAGE_ITEMS:
        if code == language_code:
            return display_label

    for language_name, code in SUPPORTED_LANGUAGES.items():
        if code == language_code:
            return language_name

    return "未設定"


def _build_auto_detect_copy(i18n: MenuI18n, enabled: bool) -> tuple[str, str]:
    target_label = i18n["auto_detect_target_name"]
    status = i18n["auto_detect_status_on"] if enabled else i18n["auto_detect_status_off"]
    button_text = i18n["auto_detect_button_template"].format(status=status, target=target_label)
    tutorial_text = i18n["tutorial_2_template"].format(target=target_label)
    return button_text, tutorial_text


def _build_feature_button(label: str, command_text: str, button_color: str) -> FlexButton:
    return FlexButton(
        style="primary",
        color=button_color,
        action=MessageAction(label=_safe_action_label(label), text=command_text),
        cornerRadius="14px",
        height="sm",
        margin="md",
    )


def _safe_action_label(label: str) -> str:
    value = (label or "").strip()
    if len(value) <= LINE_ACTION_LABEL_MAX:
        return value
    return f"{value[: LINE_ACTION_LABEL_MAX - 3]}..."


def _build_language_chip(
    language_code: str,
    label: str,
    command_text: str,
    current_language_code: str,
) -> FlexButton:
    selected = language_code == current_language_code

    return FlexButton(
        style="primary",
        color=THEME_GOLD if selected else THEME_BG_DARK,
        action=MessageAction(
            label=_safe_action_label(f"✅ {label}" if selected else label),
            text=command_text,
        ),
        cornerRadius="18px",
        margin="sm",
        height="sm",
    )


def _build_status_toggle_row(
    label: str,
    enabled: bool,
    on_command: str,
    off_command: str,
    on_label: str,
    off_label: str,
    on_text: str,
    off_text: str,
) -> FlexBox:
    toggle_label = off_label if enabled else on_label
    toggle_command = off_command if enabled else on_command
    toggle_color = "#334155" if enabled else THEME_SUCCESS

    return FlexBox(
        layout="horizontal",
        spacing="sm",
        margin="sm",
        alignItems="center",
        contents=[
            FlexText(
                text=f"{label} - {on_text if enabled else off_text}",
                size="xs",
                color=THEME_SUCCESS if enabled else THEME_DANGER,
                weight="bold",
                flex=8,
                wrap=False,
            ),
            FlexButton(
                style="primary",
                color=toggle_color,
                action=MessageAction(
                    label=_safe_action_label(toggle_label),
                    text=toggle_command,
                ),
                cornerRadius="12px",
                height="sm",
                flex=2,
            ),
        ],
    )


def _build_quick_language_section(
    current_language_code: str,
    mode_button_color: str,
    auto_detect_enabled: bool,
    i18n: MenuI18n,
) -> list[FlexBox | FlexText | FlexSeparator | FlexButton]:
    auto_detect_text, _ = _build_auto_detect_copy(i18n, auto_detect_enabled)
    row_top = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[0][0],
                QUICK_LANGUAGE_ITEMS[0][1],
                QUICK_LANGUAGE_ITEMS[0][2],
                current_language_code,
            ),
        ],
    )

    row_one = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[1][0],
                QUICK_LANGUAGE_ITEMS[1][1],
                QUICK_LANGUAGE_ITEMS[1][2],
                current_language_code,
            ),
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[2][0],
                QUICK_LANGUAGE_ITEMS[2][1],
                QUICK_LANGUAGE_ITEMS[2][2],
                current_language_code,
            ),
        ],
    )

    row_two = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[3][0],
                QUICK_LANGUAGE_ITEMS[3][1],
                QUICK_LANGUAGE_ITEMS[3][2],
                current_language_code,
            ),
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[4][0],
                QUICK_LANGUAGE_ITEMS[4][1],
                QUICK_LANGUAGE_ITEMS[4][2],
                current_language_code,
            ),
        ],
    )

    row_three = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[5][0],
                QUICK_LANGUAGE_ITEMS[5][1],
                QUICK_LANGUAGE_ITEMS[5][2],
                current_language_code,
            ),
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[6][0],
                QUICK_LANGUAGE_ITEMS[6][1],
                QUICK_LANGUAGE_ITEMS[6][2],
                current_language_code,
            ),
        ],
    )

    row_four = FlexBox(
        layout="horizontal",
        spacing="sm",
        contents=[
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[7][0],
                QUICK_LANGUAGE_ITEMS[7][1],
                QUICK_LANGUAGE_ITEMS[7][2],
                current_language_code,
            ),
            _build_language_chip(
                QUICK_LANGUAGE_ITEMS[8][0],
                QUICK_LANGUAGE_ITEMS[8][1],
                QUICK_LANGUAGE_ITEMS[8][2],
                current_language_code,
            ),
        ],
    )

    return [
        FlexSeparator(margin="xl"),
        FlexText(
            text=i18n["quick_switch"],
            size="sm",
            color=THEME_WHITE,
            weight="bold",
            margin="xl",
        ),
        _build_feature_button(
            auto_detect_text,
            "關閉自動偵測" if auto_detect_enabled else "啟用自動偵測",
            mode_button_color,
        ),
        row_top,
        row_one,
        row_two,
        row_three,
        row_four,
    ]


def build_main_menu_card(
    source_type: str,
    is_group_manager: bool,
    current_language_code: str = "zh-TW",
    translation_enabled: bool = True,
    auto_detect_enabled: bool = False,
    vip_enabled: bool = False,
    vip_started_at_text: str = "-",
    vip_plan: str = "VIP-DEEPL-PRO-100K",
    vip_remaining_chars: int = 0,
    show_vip_actions: bool = False,
) -> FlexMessage:
    is_group_mode = source_type == "group"
    i18n = get_menu_i18n(current_language_code)
    _, tutorial_auto_detect = _build_auto_detect_copy(i18n, auto_detect_enabled)
    mode_name = i18n["mode_group"] if is_group_mode else i18n["mode_personal"]
    mode_banner_color = THEME_GROUP if is_group_mode else THEME_PERSONAL_LIGHT
    mode_button_color = THEME_GROUP if is_group_mode else THEME_PERSONAL
    header_title = "翻翻君 - V1.0正式版"
    version_text = i18n["version"]

    if vip_enabled:
        mode_banner_color = "#121212"
        mode_button_color = "#2A1E0B"
        header_title = "翻翻君 - VIP尊榮版"
        version_text = "當前版本 - V1.0.0 VIP版"

    group_tip = i18n["group_tip_group"]
    group_action = "查看群組設定"
    group_label = i18n["btn_group_manage"]
    vip_command = "VIP主選單" if vip_enabled else "vip開通"

    if source_type != "group":
        group_tip = i18n["group_tip_personal"]
        group_action = "指令說明"
        group_label = i18n["btn_group_intro"]
    elif not is_group_manager:
        group_tip = i18n["group_tip_bind"]
        group_action = "綁定邀請者"
        group_label = i18n["btn_group_bind"]

    main_actions: list[FlexBox | FlexText | FlexSeparator | FlexButton] = []
    main_actions.extend(
        _build_quick_language_section(
            current_language_code,
            mode_button_color,
            auto_detect_enabled,
            i18n,
        )
    )

    footer_actions: list[FlexButton] = [
        _build_feature_button(
            i18n["btn_help"],
            "指令說明",
            mode_button_color,
        ),
        _build_feature_button(
            i18n["btn_vip"],
            vip_command,
            mode_button_color,
        ),
    ]

    if vip_enabled and show_vip_actions:
        footer_actions.extend(
            [
                _build_feature_button(
                    "高級功能1：查看群組",
                    "查看群組",
                    mode_button_color,
                ),
                _build_feature_button(
                    "高級功能2：查看當日消耗額度",
                    "查看當日消耗額度",
                    mode_button_color,
                ),
                _build_feature_button(
                    "高級功能3：離開群組",
                    "離開群組",
                    mode_button_color,
                ),
            ]
        )

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor=mode_banner_color,
            contents=[
                FlexText(
                    text=header_title,
                    size="sm",
                    color=THEME_GOLD,
                    weight="bold",
                ),
                FlexText(
                    text=i18n["control_center"],
                    size="xxl",
                    weight="bold",
                    color=THEME_WHITE,
                    margin="sm",
                ),
                _build_status_toggle_row(
                    i18n["status_translation"],
                    translation_enabled,
                    "開啟即時翻譯",
                    "關閉即時翻譯",
                    i18n["toggle_on"],
                    i18n["toggle_off"],
                    i18n["status_on"],
                    i18n["status_off"],
                ),
                _build_status_toggle_row(
                    i18n["status_auto_detect"],
                    auto_detect_enabled,
                    "啟用自動偵測",
                    "關閉自動偵測",
                    i18n["toggle_on"],
                    i18n["toggle_off"],
                    i18n["status_on"],
                    i18n["status_off"],
                ),
                FlexText(
                    text=version_text,
                    size="xs",
                    color=THEME_WHITE,
                    margin="md",
                ),
                FlexText(
                    text=f"開通時間 - {vip_started_at_text}" if vip_enabled else "",
                    size="xs",
                    color="#E7D3A1",
                    margin="sm",
                    wrap=True,
                ),
                FlexText(
                    text=f"當前方案 - {vip_plan}" if vip_enabled else "",
                    size="xs",
                    color="#E7D3A1",
                    margin="sm",
                    wrap=True,
                ),
                FlexText(
                    text=f"剩餘字數 - {vip_remaining_chars}" if vip_enabled else "",
                    size="xs",
                    color="#E7D3A1",
                    margin="sm",
                    wrap=True,
                ),
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
                FlexText(
                    text=f"{i18n['mode_prefix']}{mode_name}",
                    size="sm",
                    color=THEME_GOLD,
                    weight="bold",
                ),
                FlexText(
                    text=group_tip,
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="sm",
                ),
                FlexText(
                    text=i18n["tutorial_title"],
                    size="xs",
                    color=THEME_WHITE,
                    weight="bold",
                    margin="md",
                ),
                FlexText(
                    text=i18n["tutorial_1"],
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="xs",
                ),
                FlexText(
                    text=tutorial_auto_detect,
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="xs",
                ),
                FlexText(
                    text=i18n["tutorial_3"],
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="xs",
                ),
                FlexText(
                    text=i18n["tutorial_4"],
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="xs",
                ),
                *footer_actions,
            ],
        ),
    )

    return FlexMessage(
        altText="翻翻君主選單",
        contents=bubble,
        quickReply=None,
    )


def build_vip_main_menu_card(
    started_at_text: str,
    current_plan: str,
    remaining_chars: int,
) -> FlexMessage:
    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor="#111111",
            contents=[
                FlexText(
                    text="FanFan VIP",
                    size="sm",
                    color="#F0C24B",
                    weight="bold",
                ),
                FlexText(
                    text="VIP 主選單",
                    size="xxl",
                    weight="bold",
                    color="#FFF8E1",
                    margin="sm",
                ),
                FlexText(
                    text="暗金尊榮方案",
                    size="xs",
                    color="#D6B46C",
                    margin="md",
                ),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            spacing="md",
            paddingAll="16px",
            backgroundColor="#1A1A1A",
            contents=[
                FlexText(text=f"開通時間：{started_at_text}", size="sm", color="#FFF8E1", wrap=True),
                FlexText(text=f"當前方案：{current_plan}", size="sm", color="#FFF8E1", wrap=True),
                FlexText(text=f"剩餘字數：{remaining_chars}", size="sm", color="#FFF8E1", wrap=True),
                FlexSeparator(margin="md"),
                FlexButton(
                    style="primary",
                    color="#8B6B2D",
                    action=MessageAction(label=_safe_action_label("序號開通"), text="vip開通"),
                    cornerRadius="14px",
                    height="sm",
                    margin="md",
                ),
                FlexButton(
                    style="secondary",
                    action=MessageAction(label=_safe_action_label("回主選單"), text="/menu"),
                    height="sm",
                    margin="md",
                ),
            ],
        ),
    )

    return FlexMessage(
        altText="FanFan VIP 主選單",
        contents=bubble,
        quickReply=None,
    )


def build_language_setting_card(
    selected_codes: list[str],
    source_type: str,
    can_manage_group: bool,
    is_paid_member: bool = False,
    today_translated_chars: int = 0,
    translation_limit: int = 3000,
) -> FlexMessage:
    title = "🌐 群組翻譯設定" if source_type == "group" else "🌐 個人翻譯設定"
    subtitle = (
        "請加上 / 取消要翻譯成的語言，可複選。"
        if source_type == "group"
        else "請選擇要翻譯成的語言。"
    )

    selected_labels = [
        name for name, code in SUPPORTED_LANGUAGES.items() if code in selected_codes
    ]
    selected_text = "、".join(selected_labels) if selected_labels else "尚未設定"
    current_code = selected_codes[0] if selected_codes else "zh-TW"
    current_label = _language_label_by_code(current_code)

    if source_type == "group" and not can_manage_group:
        permission_hint = "你目前沒有設定權限（需邀請者代表 / 管理員 / 所有者）。"
    else:
        permission_hint = "點擊下方語言按鈕即可切換勾選狀態。"

    button_contents = []

    for tag, pretty_name, command_name, language_code in LANGUAGE_MENU_ITEMS:
        is_selected = language_code in selected_codes
        label_text = f"✅ {tag} {pretty_name}" if is_selected else f"{tag} {pretty_name}"
        action_text = f"設定語言 {command_name}"

        button_contents.append(
            FlexButton(
                style="primary",
                color=THEME_GOLD if is_selected else THEME_BG_DEEP,
                action=MessageAction(label=_safe_action_label(label_text), text=action_text),
                cornerRadius="14px",
                height="sm",
                margin="sm",
            )
        )

    button_contents.append(
        FlexButton(
            style="secondary",
            action=MessageAction(label=_safe_action_label("🔁 重設翻譯設定"), text="重設翻譯設定"),
            margin="md",
            height="sm",
        )
    )

    button_contents.append(
        FlexButton(
            style="secondary",
            action=MessageAction(label=_safe_action_label("🏠 回主選單"), text="/menu"),
            margin="md",
            height="sm",
        )
    )

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor=THEME_BG_DARK,
            contents=[
                FlexText(text=title, weight="bold", size="xl", color=THEME_GOLD),
                FlexText(
                    text=subtitle,
                    size="sm",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="sm",
                ),
                FlexSeparator(margin="md"),
                FlexText(
                    text=f"目前翻譯語言 : {current_label}",
                    size="sm",
                    color=THEME_WHITE,
                    wrap=True,
                    margin="md",
                ),
                FlexText(
                    text=f"版本狀態 : {'付費版會員' if is_paid_member else '免費版'}",
                    size="sm",
                    color=THEME_WHITE,
                    margin="sm",
                ),
                FlexText(
                    text=f"今日翻譯字數 : {today_translated_chars}",
                    size="sm",
                    color=THEME_WHITE,
                    margin="sm",
                ),
                FlexText(
                    text=f"版本翻譯上限 : {translation_limit}",
                    size="sm",
                    color=THEME_WHITE,
                    margin="sm",
                ),
                FlexFiller(),
                FlexText(
                    text=f"目前勾選：{selected_text}",
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                    margin="md",
                ),
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
                FlexText(
                    text=f"✅ {permission_hint}",
                    size="xs",
                    color=THEME_MUTED,
                    wrap=True,
                ),
            ],
        ),
    )

    return FlexMessage(
        altText="翻翻君語言設定",
        contents=bubble,
        quickReply=None,
    )


def build_main_menu_json(
    source_type: str,
    is_group_manager: bool,
    current_language_code: str = "zh-TW",
) -> dict:
    menu_message = build_main_menu_card(
        source_type,
        is_group_manager,
        current_language_code,
    )

    if hasattr(menu_message, "to_dict"):
        return menu_message.to_dict()

    return {"altText": menu_message.alt_text, "contents": {}}

