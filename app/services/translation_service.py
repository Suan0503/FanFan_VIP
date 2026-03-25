from deep_translator import GoogleTranslator  # 匯入翻譯工具


def translate_text(text: str, target_language_code: str) -> str:
    clean_text = text.strip()  # 清理空白
    if not clean_text:
        return ""  # 空字串直接回傳
    try:
        translator = GoogleTranslator(source="auto", target=target_language_code)  # 設定自動偵測來源
        return translator.translate(clean_text)  # 執行翻譯
    except Exception:
        return clean_text  # 若翻譯失敗則回傳原文
