import requests  # 匯入 HTTP 請求工具

from app.core.config import settings  # 匯入設定


DEEPL_LANGUAGE_MAP = {
    "zh-TW": "ZH-HANT",
    "en": "EN",
    "th": "TH",
    "vi": "VI",
    "ko": "KO",
    "id": "ID",
    "ja": "JA",
    "ru": "RU",
}  # DeepL 支援的語言映射


google_session = requests.Session()  # Google 翻譯共用連線


def _translate_with_deepl(text: str, target_language_code: str) -> str | None:
    api_key = settings.deepl_api_key.strip()  # 讀取 DeepL 金鑰
    deepl_target = DEEPL_LANGUAGE_MAP.get(target_language_code)  # 轉換 DeepL 語言代碼
    if not api_key or not deepl_target:
        return None  # 無金鑰或語言不支援時回傳 None

    endpoint = "https://api-free.deepl.com/v2/translate" if api_key.endswith(":fx") else "https://api.deepl.com/v2/translate"  # 選擇 Free/Pro 端點
    try:
        response = requests.post(
            endpoint,
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
            data={
                "text": text,
                "target_lang": deepl_target,
            },
            timeout=20,
        )  # 呼叫 DeepL API
        if response.status_code != 200:
            return None  # DeepL 失敗時交給備援
        payload = response.json()  # 解析回應
        translations = payload.get("translations", [])  # 讀取翻譯結果
        if not translations:
            return None  # 無翻譯結果
        return translations[0].get("text")  # 回傳第一筆翻譯
    except Exception:
        return None  # DeepL 例外時交給備援


def _translate_with_fallback(text: str, target_language_code: str) -> str:
    url = "https://translate.googleapis.com/translate_a/single"  # Google 非官方翻譯端點
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_language_code,
        "dt": "t",
        "q": text,
    }  # 參數設定
    response = google_session.get(url, params=params, timeout=20)  # 呼叫 Google 翻譯
    response.raise_for_status()  # 檢查 HTTP 狀態
    payload = response.json()  # 解析 JSON
    return payload[0][0][0]  # 取回翻譯結果


def _is_non_translatable(text: str) -> bool:
    compact = text.replace(" ", "").replace(".", "").replace(",", "").replace("/", "")  # 清理常見符號
    if not compact:
        return True  # 空內容不翻譯
    return compact.isdigit()  # 純數字不翻譯


def translate_text(text: str, target_language_code: str) -> str:
    clean_text = text.strip()  # 清理空白
    if not clean_text:
        return ""  # 空字串直接回傳
    if _is_non_translatable(clean_text):
        return clean_text  # 數字/代碼類內容直接回傳

    try:
        deepl_result = _translate_with_deepl(clean_text, target_language_code)  # 優先使用 DeepL
        if deepl_result:
            return deepl_result  # DeepL 成功時直接回傳
    except Exception:
        pass  # DeepL 發生任何錯誤時繼續走備援

    try:
        return _translate_with_fallback(clean_text, target_language_code)  # 不支援語言時改用備援
    except Exception:
        return clean_text  # 若翻譯失敗則回傳原文
