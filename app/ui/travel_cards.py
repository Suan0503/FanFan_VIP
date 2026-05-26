from linebot.v3.messaging import FlexBox, FlexBubble, FlexButton, FlexMessage, FlexText, MessageAction

from app.ui.travel_i18n import get_travel_i18n


LINE_ACTION_LABEL_MAX = 40


def _safe_action_label(label: str) -> str:
    value = (label or "").strip()
    if len(value) <= LINE_ACTION_LABEL_MAX:
        return value
    return f"{value[: LINE_ACTION_LABEL_MAX - 3]}..."


def build_travel_mode_card(current_language_code: str) -> FlexMessage:
    i18n = get_travel_i18n(current_language_code)

    bubble = FlexBubble(
        size="mega",
        header=FlexBox(
            layout="vertical",
            backgroundColor="#0F172A",
            paddingAll="16px",
            contents=[
                FlexText(text=i18n["title"], size="xl", weight="bold", color="#F8FAFC"),
                FlexText(text=i18n["subtitle"], size="sm", color="#93C5FD", margin="sm"),
            ],
        ),
        body=FlexBox(
            layout="vertical",
            backgroundColor="#1E293B",
            paddingAll="16px",
            spacing="md",
            contents=[
                FlexText(text=i18n["description"], size="sm", color="#E2E8F0", wrap=True),
                FlexButton(
                    style="primary",
                    color="#22C55E",
                    height="sm",
                    action=MessageAction(
                        label=_safe_action_label(i18n["agree_button"]),
                        text=i18n["confirm_command"],
                    ),
                ),
                FlexButton(
                    style="secondary",
                    height="sm",
                    action=MessageAction(
                        label=_safe_action_label(i18n["back_button"]),
                        text=i18n["back_command"],
                    ),
                ),
            ],
        ),
    )

    return FlexMessage(altText=i18n["title"], contents=bubble, quickReply=None)
