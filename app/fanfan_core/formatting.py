from app.fanfan_core.language_profile import get_language_display  # 匯入語言顯示工具


def format_language_updated(language_codes: list[str]) -> str:
    lines = ["✅ 已更新翻譯語言！", "", "目前設定語言："]  # 標題
    for code in language_codes:
        flag, name = get_language_display(code)  # 取語言顯示
        lines.append(f"{flag} {name} ({code})")  # 增加一行語言設定
    return "\n".join(lines)  # 回傳完整訊息


def format_translation_results(text: str, language_codes: list[str], translate_func) -> str:
    rows: list[str] = []  # 翻譯結果行
    for code in language_codes:
        try:
            translated = translate_func(text, code)  # 執行翻譯
        except Exception:
            translated = text  # 單語失敗時回原文
        rows.append(f"[{code}] {translated}")  # 舊版格式
    return "\n".join(rows)  # 回傳多語結果
