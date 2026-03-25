SUPPORTED_LANGUAGES = {
    "中文": "zh-TW",
    "英文": "en",
    "泰文": "th",
    "越南文": "vi",
    "印尼文": "id",
    "日文": "ja",
    "俄文": "ru",
}  # 可選語言映射

LANGUAGE_DISPLAY = {
    "zh-TW": ("🇹🇼", "中文(台灣)"),
    "en": ("🇺🇸", "英文"),
    "th": ("🇹🇭", "泰文"),
    "vi": ("🇻🇳", "越南文"),
    "id": ("🇮🇩", "印尼文"),
    "ja": ("🇯🇵", "日文"),
    "ru": ("🇷🇺", "俄文"),
}  # 語言顯示資訊（旗幟, 名稱）

DEFAULT_LANGUAGE_LABEL = "中文"  # 預設語言名稱
DEFAULT_LANGUAGE_CODE = SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_LABEL]  # 預設語言代碼
