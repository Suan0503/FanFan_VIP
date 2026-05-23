from app.fanfan_core.language_profile import get_language_display  # 匯入語言顯示工具


def _looks_like_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)  # 漢字範圍


def _looks_like_thai(text: str) -> bool:
    return any("\u0e00" <= ch <= "\u0e7f" for ch in text)  # 泰文範圍


def _looks_like_japanese(text: str) -> bool:
    return any(("\u3040" <= ch <= "\u30ff") or ("\u31f0" <= ch <= "\u31ff") for ch in text)  # 日文假名


def _looks_like_korean(text: str) -> bool:
    return any("\uac00" <= ch <= "\ud7af" for ch in text)  # 韓文範圍


def _looks_like_myanmar(text: str) -> bool:
    return any("\u1000" <= ch <= "\u109f" for ch in text)  # 緬文範圍


def _looks_like_russian(text: str) -> bool:
    return any(("\u0400" <= ch <= "\u04ff") or ch in "Ёё" for ch in text)  # 西里爾字母範圍


def _looks_like_vietnamese(text: str) -> bool:
    markers = "ăâđêôơưÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬáàảãạắằẳẵặấầẩẫậÉÈẺẼẸÊẾỀỂỄỆéèẻẽẹếềểễệÍÌỈĨỊíìỉĩịÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢóòỏõọốồổỗộớờởỡợÚÙỦŨỤƯỨỪỬỮỰúùủũụứừửữựÝỲỶỸỴýỳỷỹỵ"
    return any(ch in markers for ch in text)  # 越文常用重音字元


def detect_source_language(text: str, candidate_codes: list[str]) -> str | None:
    clean = (text or "").strip()
    if not clean:
        return None  # 空字串不偵測

    checks: list[tuple[str, bool]] = [
        ("th", _looks_like_thai(clean)),
        ("ja", _looks_like_japanese(clean)),
        ("ko", _looks_like_korean(clean)),
        ("my", _looks_like_myanmar(clean)),
        ("ru", _looks_like_russian(clean)),
        ("vi", _looks_like_vietnamese(clean)),
        ("zh-TW", _looks_like_chinese(clean)),
    ]
    for code, matched in checks:
        if matched and code in candidate_codes:
            return code  # 命中候選語言

    return None  # 其餘語言交給預設路由


def format_language_updated(language_codes: list[str]) -> str:
    lines = ["✅ 已更新翻譯語言！", "", "目前設定語言："]  # 標題
    for code in language_codes:
        flag, name = get_language_display(code)  # 取語言顯示
        lines.append(f"{flag} {name} ({code})")  # 增加一行語言設定
    return "\n".join(lines)  # 回傳完整訊息


def format_translation_results(text: str, language_codes: list[str], translate_func) -> str:
    source_code = detect_source_language(text, language_codes)  # 偵測原文語言
    target_codes = [code for code in language_codes if code != source_code] if source_code else list(language_codes)  # 原文語言不重翻
    if not target_codes:
        return text  # 單一語言且原文已匹配時回原文

    rows: list[str] = []  # 翻譯結果行
    for code in target_codes:
        try:
            translated = translate_func(text, code)  # 執行翻譯
        except Exception:
            translated = text  # 單語失敗時回原文
        rows.append(f"[{code}] {translated}")  # 舊版格式
    return "\n".join(rows)  # 回傳多語結果
