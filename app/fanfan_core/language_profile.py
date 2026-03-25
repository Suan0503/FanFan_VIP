from app.core.languages import SUPPORTED_LANGUAGES, LANGUAGE_DISPLAY, DEFAULT_LANGUAGE_CODE  # 匯入語言設定


LEGACY_LANGUAGE_MENU_ITEMS = [
    ("TW", "中文(台灣)", "中文", "zh-TW"),
    ("US", "英文", "英文", "en"),
    ("TH", "泰文", "泰文", "th"),
    ("VN", "越南文", "越南文", "vi"),
    ("MM", "緬甸文", "緬甸文", "my"),
    ("KR", "韓文", "韓文", "ko"),
    ("ID", "印尼文", "印尼文", "id"),
    ("JP", "日文", "日文", "ja"),
    ("RU", "俄文", "俄文", "ru"),
]  # 舊版語言按鈕顯示順序


def resolve_language_code(language_label: str) -> str | None:
    return SUPPORTED_LANGUAGES.get(language_label)  # 由中文名稱取語言代碼


def parse_language_labels(raw_text: str) -> list[str]:
    normalized = raw_text.replace("、", ",").replace("，", ",")  # 統一分隔符號
    return [part.strip() for part in normalized.split(",") if part.strip()]  # 分割並清理


def get_language_display(language_code: str) -> tuple[str, str]:
    return LANGUAGE_DISPLAY.get(language_code, ("🏳️", language_code))  # 回傳旗幟與名稱


def summarize_language_codes(language_codes: list[str]) -> str:
    if not language_codes:
        return "(無)"  # 防禦性回傳
    names: list[str] = []  # 語言名稱清單
    for code in language_codes:
        _, name = get_language_display(code)  # 取顯示名稱
        names.append(name)
    return "、".join(names)  # 回傳摘要


def ensure_non_empty_codes(language_codes: list[str]) -> list[str]:
    return language_codes if language_codes else [DEFAULT_LANGUAGE_CODE]  # 確保至少一個語言
