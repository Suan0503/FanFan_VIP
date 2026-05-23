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
THEME_BG_DEEP = "#14213D"  # 深藍背景
THEME_GOLD = "#D4AF37"  # 強調金色
THEME_MUTED = "#94A3B8"  # 輔助灰
THEME_WHITE = "#F8FAFC"  # 亮色文字
THEME_SUCCESS = "#22C55E"  # 啟用狀態色
THEME_DANGER = "#64748B"  # 關閉狀態色
THEME_PERSONAL = "#1E3A8A"  # 個人模式主色
THEME_PERSONAL_LIGHT = "#1D4ED8"  # 個人模式標題色
THEME_GROUP = "#14213D"  # 群組模式主色
LINE_ACTION_LABEL_MAX = 40  # LINE MessageAction label 長度上限


MENU_I18N = {
    "zh-TW": {
        "control_center": "選單控制中心",
        "status_translation": "即時翻譯功能",
        "status_auto_detect": "自動偵測文字",
        "status_on": "啟用中",
        "status_off": "關閉中",
        "toggle_on": "開啟",
        "toggle_off": "關閉",
        "version": "當前版本 - V1.0.0 免費版",
        "quick_switch": "🌏 快速切換語言",
        "auto_detect_on": "🧠 開啟中 自動偵測模式（非中文訊息 -> 中文）",
        "auto_detect_off": "🧠 關閉中 自動偵測模式（非中文訊息 -> 中文）",
        "mode_prefix": "當前使用模式 - ",
        "mode_personal": "個人模式",
        "mode_group": "群組翻譯模式",
        "group_tip_personal": "把翻翻君加入群組後，可開啟群組多語翻譯。",
        "group_tip_group": "群組中可複選語言，之後每句都會固定翻譯。",
        "group_tip_bind": "尚未取得群組設定權限，請先輸入：綁定邀請者",
        "tutorial_title": "使用教學:",
        "tutorial_1": "1. 先用上方語言按鈕設定可翻譯語言",
        "tutorial_2": "2. 點擊自動偵測可啟用非中文 -> 中文翻譯",
        "tutorial_3": "3. 群組模式可複選語言並自動互譯",
        "tutorial_4": "4. 輸入 /menu 或 /選單 可隨時重開控制中心",
        "btn_help": "📘【教學中心】快速上手與完整教學",
        "btn_group_manage": "👥【群組翻譯】群組語言管理",
        "btn_group_intro": "👥【群組翻譯】群組功能說明",
        "btn_group_bind": "👥【群組翻譯】綁定邀請者",
        "btn_vip": "⭐【VIP 功能】DeepL Pro｜高階翻譯能力",
    },
    "en": {
        "control_center": "Control Center",
        "status_translation": "Realtime Translation",
        "status_auto_detect": "Auto Detect Text",
        "status_on": "ON",
        "status_off": "OFF",
        "toggle_on": "On",
        "toggle_off": "Off",
        "version": "Version - V1.0.0 Free",
        "quick_switch": "🌏 Quick Language Switch",
        "auto_detect_on": "🧠 ON Auto Detect Mode (Non-Chinese -> Chinese)",
        "auto_detect_off": "🧠 OFF Auto Detect Mode (Non-Chinese -> Chinese)",
        "mode_prefix": "Current Mode - ",
        "mode_personal": "Personal",
        "mode_group": "Group Translation",
        "group_tip_personal": "Add FanFan to a group to enable multi-language translation.",
        "group_tip_group": "In groups, selected languages will be translated continuously.",
        "group_tip_bind": "No group permission yet, please bind inviter first.",
        "tutorial_title": "How to use:",
        "tutorial_1": "1. Set languages with the buttons above",
        "tutorial_2": "2. Enable auto detect for Non-Chinese -> Chinese",
        "tutorial_3": "3. Group mode supports multi-language mutual translation",
        "tutorial_4": "4. Type /menu anytime to reopen control center",
        "btn_help": "📘 Help & Guide",
        "btn_group_manage": "👥 Group Language Settings",
        "btn_group_intro": "👥 Group Feature Guide",
        "btn_group_bind": "👥 Bind Group Inviter",
        "btn_vip": "⭐ VIP Feature | DeepL Pro",
    },
    "ja": {
        "control_center": "メニュー管理センター",
        "status_translation": "リアルタイム翻訳",
        "status_auto_detect": "自動言語検出",
        "status_on": "有効",
        "status_off": "無効",
        "toggle_on": "オン",
        "toggle_off": "オフ",
        "version": "バージョン - V1.0.0 無料版",
        "quick_switch": "🌏 言語クイック切替",
        "auto_detect_on": "🧠 有効 自動検出モード（非中国語 -> 中国語）",
        "auto_detect_off": "🧠 無効 自動検出モード（非中国語 -> 中国語）",
        "mode_prefix": "現在のモード - ",
        "mode_personal": "個人モード",
        "mode_group": "グループ翻訳モード",
        "group_tip_personal": "FanFanをグループに追加すると多言語翻訳が使えます。",
        "group_tip_group": "グループでは選択言語に継続翻訳します。",
        "group_tip_bind": "権限がありません。まず招待者を紐付けてください。",
        "tutorial_title": "使い方:",
        "tutorial_1": "1. 上のボタンで翻訳言語を設定",
        "tutorial_2": "2. 自動検出で非中国語を中国語へ翻訳",
        "tutorial_3": "3. グループで複数言語の相互翻訳",
        "tutorial_4": "4. /menu でいつでも再表示",
        "btn_help": "📘 使い方ガイド",
        "btn_group_manage": "👥 グループ言語設定",
        "btn_group_intro": "👥 グループ機能説明",
        "btn_group_bind": "👥 招待者を紐付け",
        "btn_vip": "⭐ VIP機能 | DeepL Pro",
    },
    "th": {
        "control_center": "ศูนย์ควบคุมเมนู",
        "status_translation": "แปลแบบเรียลไทม์",
        "status_auto_detect": "ตรวจจับภาษาอัตโนมัติ",
        "status_on": "เปิด",
        "status_off": "ปิด",
        "toggle_on": "เปิด",
        "toggle_off": "ปิด",
        "version": "เวอร์ชัน - V1.0.0 ฟรี",
        "quick_switch": "🌏 สลับภาษาด่วน",
        "auto_detect_on": "🧠 เปิด โหมดตรวจจับอัตโนมัติ (ไม่ใช่จีน -> จีน)",
        "auto_detect_off": "🧠 ปิด โหมดตรวจจับอัตโนมัติ (ไม่ใช่จีน -> จีน)",
        "mode_prefix": "โหมดปัจจุบัน - ",
        "mode_personal": "โหมดส่วนตัว",
        "mode_group": "โหมดแปลกลุ่ม",
        "group_tip_personal": "เพิ่ม FanFan เข้ากลุ่มเพื่อเปิดใช้งานแปลหลายภาษา",
        "group_tip_group": "ในกลุ่มจะถูกแปลเป็นภาษาที่เลือกอย่างต่อเนื่อง",
        "group_tip_bind": "ยังไม่มีสิทธิ์กลุ่ม โปรดผูกผู้เชิญก่อน",
        "tutorial_title": "วิธีใช้:",
        "tutorial_1": "1. ตั้งภาษาที่ต้องการด้วยปุ่มด้านบน",
        "tutorial_2": "2. เปิดโหมดตรวจจับอัตโนมัติสำหรับไม่ใช่จีน -> จีน",
        "tutorial_3": "3. โหมดกลุ่มรองรับการแปลหลายภาษา",
        "tutorial_4": "4. พิมพ์ /menu เพื่อเปิดเมนูอีกครั้ง",
        "btn_help": "📘 คู่มือการใช้งาน",
        "btn_group_manage": "👥 ตั้งค่าภาษากลุ่ม",
        "btn_group_intro": "👥 แนะนำฟีเจอร์กลุ่ม",
        "btn_group_bind": "👥 ผูกผู้เชิญกลุ่ม",
        "btn_vip": "⭐ ฟีเจอร์ VIP | DeepL Pro",
    },
    "vi": {
        "control_center": "Trung tâm điều khiển menu",
        "status_translation": "Dịch thời gian thực",
        "status_auto_detect": "Tự động nhận diện",
        "status_on": "Bật",
        "status_off": "Tắt",
        "toggle_on": "Bật",
        "toggle_off": "Tắt",
        "version": "Phiên bản - V1.0.0 Miễn phí",
        "quick_switch": "🌏 Chuyển ngôn ngữ nhanh",
        "auto_detect_on": "🧠 Bật chế độ tự nhận diện (không phải tiếng Trung -> tiếng Trung)",
        "auto_detect_off": "🧠 Tắt chế độ tự nhận diện (không phải tiếng Trung -> tiếng Trung)",
        "mode_prefix": "Chế độ hiện tại - ",
        "mode_personal": "Cá nhân",
        "mode_group": "Dịch nhóm",
        "group_tip_personal": "Thêm FanFan vào nhóm để bật dịch đa ngôn ngữ.",
        "group_tip_group": "Trong nhóm, tin nhắn sẽ được dịch theo ngôn ngữ đã chọn.",
        "group_tip_bind": "Chưa có quyền nhóm, hãy liên kết người mời trước.",
        "tutorial_title": "Hướng dẫn:",
        "tutorial_1": "1. Chọn ngôn ngữ bằng các nút phía trên",
        "tutorial_2": "2. Bật tự nhận diện cho không phải tiếng Trung -> tiếng Trung",
        "tutorial_3": "3. Chế độ nhóm hỗ trợ dịch đa ngôn ngữ",
        "tutorial_4": "4. Gõ /menu để mở lại trung tâm",
        "btn_help": "📘 Hướng dẫn sử dụng",
        "btn_group_manage": "👥 Cài đặt ngôn ngữ nhóm",
        "btn_group_intro": "👥 Giới thiệu tính năng nhóm",
        "btn_group_bind": "👥 Liên kết người mời",
        "btn_vip": "⭐ Tính năng VIP | DeepL Pro",
    },
    "ko": {
        "control_center": "메뉴 제어 센터",
        "status_translation": "실시간 번역",
        "status_auto_detect": "자동 감지",
        "status_on": "켜짐",
        "status_off": "꺼짐",
        "toggle_on": "켜기",
        "toggle_off": "끄기",
        "version": "버전 - V1.0.0 무료",
        "quick_switch": "🌏 빠른 언어 전환",
        "auto_detect_on": "🧠 켜짐 자동 감지 모드 (비중국어 -> 중국어)",
        "auto_detect_off": "🧠 꺼짐 자동 감지 모드 (비중국어 -> 중국어)",
        "mode_prefix": "현재 모드 - ",
        "mode_personal": "개인 모드",
        "mode_group": "그룹 번역 모드",
        "group_tip_personal": "FanFan을 그룹에 추가하면 다국어 번역을 사용할 수 있습니다.",
        "group_tip_group": "그룹에서는 선택 언어로 지속 번역됩니다.",
        "group_tip_bind": "그룹 권한이 없습니다. 먼저 초대자 연결이 필요합니다.",
        "tutorial_title": "사용 방법:",
        "tutorial_1": "1. 상단 버튼으로 번역 언어 설정",
        "tutorial_2": "2. 자동 감지로 비중국어 -> 중국어 번역",
        "tutorial_3": "3. 그룹 모드는 다국어 상호 번역 지원",
        "tutorial_4": "4. /menu 입력으로 언제든 다시 열기",
        "btn_help": "📘 사용 가이드",
        "btn_group_manage": "👥 그룹 언어 설정",
        "btn_group_intro": "👥 그룹 기능 안내",
        "btn_group_bind": "👥 초대자 연결",
        "btn_vip": "⭐ VIP 기능 | DeepL Pro",
    },
    "id": {
        "control_center": "Pusat Kontrol Menu",
        "status_translation": "Terjemahan Real-time",
        "status_auto_detect": "Deteksi Otomatis",
        "status_on": "Aktif",
        "status_off": "Nonaktif",
        "toggle_on": "On",
        "toggle_off": "Off",
        "version": "Versi - V1.0.0 Gratis",
        "quick_switch": "🌏 Ganti Bahasa Cepat",
        "auto_detect_on": "🧠 Aktif Mode Deteksi Otomatis (Non-Cina -> Cina)",
        "auto_detect_off": "🧠 Nonaktif Mode Deteksi Otomatis (Non-Cina -> Cina)",
        "mode_prefix": "Mode Saat Ini - ",
        "mode_personal": "Mode Personal",
        "mode_group": "Mode Terjemahan Grup",
        "group_tip_personal": "Tambahkan FanFan ke grup untuk mengaktifkan terjemahan multi-bahasa.",
        "group_tip_group": "Di grup, pesan akan diterjemahkan sesuai bahasa terpilih.",
        "group_tip_bind": "Belum punya izin grup, silakan bind inviter dulu.",
        "tutorial_title": "Cara pakai:",
        "tutorial_1": "1. Atur bahasa dengan tombol di atas",
        "tutorial_2": "2. Aktifkan auto detect untuk Non-Cina -> Cina",
        "tutorial_3": "3. Mode grup mendukung terjemahan multi-bahasa",
        "tutorial_4": "4. Ketik /menu untuk membuka kembali pusat kontrol",
        "btn_help": "📘 Panduan",
        "btn_group_manage": "👥 Pengaturan Bahasa Grup",
        "btn_group_intro": "👥 Panduan Fitur Grup",
        "btn_group_bind": "👥 Bind Pengundang Grup",
        "btn_vip": "⭐ Fitur VIP | DeepL Pro",
    },
    "my": {
        "control_center": "မီနူးထိန်းချုပ်ရေးစင်တာ",
        "status_translation": "အချိန်နှင့်တပြေးညီ ဘာသာပြန်",
        "status_auto_detect": "အလိုအလျောက်ရှာဖွေမှု",
        "status_on": "ဖွင့်ထားသည်",
        "status_off": "ပိတ်ထားသည်",
        "toggle_on": "ဖွင့်",
        "toggle_off": "ပိတ်",
        "version": "ဗားရှင်း - V1.0.0 အခမဲ့",
        "quick_switch": "🌏 ဘာသာစကား အမြန်ပြောင်း",
        "auto_detect_on": "🧠 ဖွင့်ထားသည် အလိုအလျောက်ရှာဖွေမှု (တရုတ်မဟုတ် -> တရုတ်)",
        "auto_detect_off": "🧠 ပိတ်ထားသည် အလိုအလျောက်ရှာဖွေမှု (တရုတ်မဟုတ် -> တရုတ်)",
        "mode_prefix": "လက်ရှိမုဒ် - ",
        "mode_personal": "ကိုယ်ပိုင်မုဒ်",
        "mode_group": "အဖွဲ့ဘာသာပြန်မုဒ်",
        "group_tip_personal": "FanFan ကို group ထဲထည့်ပြီး ဘာသာစကားအများပြန်နိုင်သည်။",
        "group_tip_group": "Group ထဲတွင်ရွေးချယ်ထားသောဘာသာစကားများသို့ ဆက်တိုက်ဘာသာပြန်ပါမည်။",
        "group_tip_bind": "Group ခွင့်ပြုချက်မရှိသေးပါ၊ inviter ကို အရင်ချိတ်ပါ။",
        "tutorial_title": "အသုံးပြုပုံ:",
        "tutorial_1": "1. အပေါ်ဘက် button များဖြင့် ဘာသာစကားရွေးချယ်ပါ",
        "tutorial_2": "2. Auto detect ဖြင့် တရုတ်မဟုတ် -> တရုတ် ပြောင်းပါ",
        "tutorial_3": "3. Group mode တွင် ဘာသာစကားအများ ပြန်နိုင်သည်",
        "tutorial_4": "4. /menu ဖြင့် control center ကို ပြန်ဖွင့်ပါ",
        "btn_help": "📘 လမ်းညွှန်",
        "btn_group_manage": "👥 Group ဘာသာစကားဆက်တင်",
        "btn_group_intro": "👥 Group လုပ်ဆောင်ချက်လမ်းညွှန်",
        "btn_group_bind": "👥 Group Inviter ချိတ်ရန်",
        "btn_vip": "⭐ VIP လုပ်ဆောင်ချက် | DeepL Pro",
    },
    "ru": {
        "control_center": "Центр управления меню",
        "status_translation": "Мгновенный перевод",
        "status_auto_detect": "Автоопределение",
        "status_on": "Включено",
        "status_off": "Выключено",
        "toggle_on": "Вкл",
        "toggle_off": "Выкл",
        "version": "Версия - V1.0.0 Бесплатная",
        "quick_switch": "🌏 Быстрое переключение языка",
        "auto_detect_on": "🧠 ВКЛ Автоопределение (не китайский -> китайский)",
        "auto_detect_off": "🧠 ВЫКЛ Автоопределение (не китайский -> китайский)",
        "mode_prefix": "Текущий режим - ",
        "mode_personal": "Личный режим",
        "mode_group": "Групповой перевод",
        "group_tip_personal": "Добавьте FanFan в группу для многоязычного перевода.",
        "group_tip_group": "В группе сообщения переводятся на выбранные языки.",
        "group_tip_bind": "Нет прав группы, сначала привяжите пригласившего.",
        "tutorial_title": "Инструкция:",
        "tutorial_1": "1. Настройте язык кнопками выше",
        "tutorial_2": "2. Включите автоопределение для не-китайского -> китайский",
        "tutorial_3": "3. В группе доступен взаимный перевод на несколько языков",
        "tutorial_4": "4. Введите /menu для повторного открытия центра",
        "btn_help": "📘 Руководство",
        "btn_group_manage": "👥 Настройки языка группы",
        "btn_group_intro": "👥 О функциях группы",
        "btn_group_bind": "👥 Привязать пригласившего",
        "btn_vip": "⭐ VIP Функция | DeepL Pro",
    },
}


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
]  # 語言設定頁按鈕排序

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
]  # 主選單快速語言排序

AUTO_DETECT_TARGET_NAMES = {
    "zh-TW": "中文",
    "en": "English",
    "ja": "日本語",
    "th": "ไทย",
    "vi": "Tiếng Việt",
    "ko": "한국어",
    "id": "Bahasa Indonesia",
    "my": "မြန်မာ",
    "ru": "Русский",
}


def _language_label_by_code(language_code: str) -> str:
    for code, display_label, _ in QUICK_LANGUAGE_ITEMS:
        if code == language_code:
            return display_label  # 命中快速語言顯示名稱

    for language_name, code in SUPPORTED_LANGUAGES.items():
        if code == language_code:
            return language_name  # 回退一般語言名稱

    return "未設定"  # 防禦性回傳


def _auto_detect_target_label(language_code: str) -> str:
    return AUTO_DETECT_TARGET_NAMES.get(language_code, _language_label_by_code(language_code))  # 使用語言原生名稱


def _build_auto_detect_copy(language_code: str, enabled: bool) -> tuple[str, str]:
    target_label = _auto_detect_target_label(language_code)
    status_prefix = "開啟中" if enabled else "關閉中"
    button_text = f"🧠 {status_prefix} 自動偵測模式（非{target_label}訊息 -> {target_label}）"
    tutorial_text = f"2. 點擊自動偵測可啟用非{target_label} -> {target_label}翻譯"

    if language_code == "en":
        button_status = "ON" if enabled else "OFF"
        button_text = f"🧠 {button_status} Auto Detect Mode (Non-{target_label} -> {target_label})"
        tutorial_text = f"2. Enable auto detect for Non-{target_label} -> {target_label}"
    elif language_code == "ja":
        button_status = "有効" if enabled else "無効"
        button_text = f"🧠 {button_status} 自動検出モード（非{target_label} -> {target_label}）"
        tutorial_text = f"2. 自動検出で非{target_label}を{target_label}へ翻訳"
    elif language_code == "th":
        button_status = "เปิด" if enabled else "ปิด"
        button_text = f"🧠 {button_status} โหมดตรวจจับอัตโนมัติ ({target_label} อื่น -> {target_label})"
        tutorial_text = f"2. เปิดโหมดตรวจจับอัตโนมัติสำหรับภาษาที่ไม่ใช่ {target_label} -> {target_label}"
    elif language_code == "vi":
        button_status = "Bật" if enabled else "Tắt"
        button_text = f"🧠 {button_status} chế độ tự nhận diện (không phải {target_label} -> {target_label})"
        tutorial_text = f"2. Bật tự nhận diện cho ngôn ngữ không phải {target_label} -> {target_label}"
    elif language_code == "ko":
        button_status = "켜짐" if enabled else "꺼짐"
        button_text = f"🧠 {button_status} 자동 감지 모드 (비{target_label} -> {target_label})"
        tutorial_text = f"2. 자동 감지로 비{target_label} -> {target_label} 번역"
    elif language_code == "id":
        button_status = "Aktif" if enabled else "Nonaktif"
        button_text = f"🧠 {button_status} Mode Deteksi Otomatis (Non-{target_label} -> {target_label})"
        tutorial_text = f"2. Aktifkan auto detect untuk Non-{target_label} -> {target_label}"
    elif language_code == "my":
        button_status = "ဖွင့်ထားသည်" if enabled else "ပိတ်ထားသည်"
        button_text = f"🧠 {button_status} အလိုအလျောက်ရှာဖွေမှု ({target_label} မဟုတ် -> {target_label})"
        tutorial_text = f"2. Auto detect ဖြင့် {target_label} မဟုတ် -> {target_label} ပြောင်းပါ"
    elif language_code == "ru":
        button_status = "ВКЛ" if enabled else "ВЫКЛ"
        button_text = f"🧠 {button_status} Автоопределение (не {target_label} -> {target_label})"
        tutorial_text = f"2. Включите автоопределение для не-{target_label} -> {target_label}"

    return button_text, tutorial_text


def _build_feature_button(label: str, command_text: str, button_color: str) -> FlexButton:
    return FlexButton(
        style="primary",
        color=button_color,
        action=MessageAction(label=_safe_action_label(label), text=command_text),
        cornerRadius="14px",
        height="sm",
        margin="md",
    )  # 建立功能按鈕


def _safe_action_label(label: str) -> str:
    value = (label or "").strip()  # 清理空白
    if len(value) <= LINE_ACTION_LABEL_MAX:
        return value  # 未超長直接回傳
    return f"{value[: LINE_ACTION_LABEL_MAX - 3]}..."  # 超長裁切避免 LINE 400


def _build_language_chip(
    language_code: str,
    label: str,
    command_text: str,
    current_language_code: str,
) -> FlexButton:
    selected = language_code == current_language_code  # 是否為目前語言

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
    )  # 建立快速語言按鈕


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
    toggle_label = off_label if enabled else on_label  # 依狀態切換按鈕文字
    toggle_command = off_command if enabled else on_command  # 依狀態切換命令
    toggle_color = "#334155" if enabled else THEME_SUCCESS  # 關閉/開啟顏色

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
    )  # 建立狀態列與切換按鈕


def _build_quick_language_section(
    current_language_code: str,
    mode_button_color: str,
    auto_detect_enabled: bool,
    i18n: dict[str, str],
) -> list[FlexBox | FlexText | FlexSeparator | FlexButton]:
    auto_detect_text, _ = _build_auto_detect_copy(current_language_code, auto_detect_enabled)
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
    )  # 第一排單顆語言

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
    )  # 第二排雙語言

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
    )  # 第三排雙語言

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
    )  # 第四排雙語言

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
    )  # 第五排雙語言

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
    ]  # 回傳快速語言區


def build_main_menu_card(
    source_type: str,
    is_group_manager: bool,
    current_language_code: str = "zh-TW",
    translation_enabled: bool = True,
    auto_detect_enabled: bool = False,
) -> FlexMessage:
    is_group_mode = source_type == "group"  # 判斷是否群組模式
    i18n = MENU_I18N.get(current_language_code, MENU_I18N["zh-TW"])  # 依當前語言切換選單文案
    _, tutorial_auto_detect = _build_auto_detect_copy(current_language_code, auto_detect_enabled)
    mode_name = i18n["mode_group"] if is_group_mode else i18n["mode_personal"]  # 模式名稱
    mode_banner_color = THEME_GROUP if is_group_mode else THEME_PERSONAL_LIGHT  # 標題色
    mode_button_color = THEME_GROUP if is_group_mode else THEME_PERSONAL  # 內容色

    group_tip = i18n["group_tip_group"]  # 群組提示
    group_action = "查看群組設定"  # 群組功能預設命令
    group_label = i18n["btn_group_manage"]  # 群組功能按鈕文字

    if source_type != "group":
        group_tip = i18n["group_tip_personal"]  # 個人模式提示
        group_action = "指令說明"  # 個人模式顯示說明
        group_label = i18n["btn_group_intro"]  # 個人模式按鈕
    elif not is_group_manager:
        group_tip = i18n["group_tip_bind"]  # 權限不足提示
        group_action = "綁定邀請者"  # 權限不足導向命令
        group_label = i18n["btn_group_bind"]  # 權限不足按鈕

    main_actions: list[FlexBox | FlexText | FlexSeparator | FlexButton] = []  # 主內容元件
    main_actions.extend(
        _build_quick_language_section(
            current_language_code,
            mode_button_color,
            auto_detect_enabled,
            i18n,
        )
    )

    bubble = FlexBubble(
        size="giga",
        header=FlexBox(
            layout="vertical",
            paddingAll="18px",
            backgroundColor=mode_banner_color,
            contents=[
                FlexText(
                    text="翻翻君 - V1.0正式版",
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
                    text=i18n["version"],
                    size="xs",
                    color=THEME_WHITE,
                    margin="md",
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
                _build_feature_button(
                    i18n["btn_help"],
                    "指令說明",
                    mode_button_color,
                ),
                _build_feature_button(
                    group_label,
                    group_action,
                    mode_button_color,
                ),
                _build_feature_button(
                    i18n["btn_vip"],
                    "指令說明",
                    mode_button_color,
                ),
            ],
        ),
    )  # 建立主選單 Bubble

    return FlexMessage(
        altText="翻翻君主選單",
        contents=bubble,
        quickReply=None,
    )  # 回傳主選單訊息


def build_language_setting_card(
    selected_codes: list[str],
    source_type: str,
    can_manage_group: bool,
    is_paid_member: bool = False,
    today_translated_chars: int = 0,
    translation_limit: int = 3000,
) -> FlexMessage:
    title = "🌐 群組翻譯設定" if source_type == "group" else "🌐 個人翻譯設定"  # 標題
    subtitle = (
        "請加上 / 取消要翻譯成的語言，可複選。"
        if source_type == "group"
        else "請選擇要翻譯成的語言。"
    )

    selected_labels = [
        name for name, code in SUPPORTED_LANGUAGES.items() if code in selected_codes
    ]
    selected_text = "、".join(selected_labels) if selected_labels else "尚未設定"  # 已選語言摘要
    current_code = selected_codes[0] if selected_codes else "zh-TW"  # 目前語言代碼
    current_label = _language_label_by_code(current_code)  # 目前語言顯示名稱

    if source_type == "group" and not can_manage_group:
        permission_hint = "你目前沒有設定權限（需邀請者代表 / 管理員 / 所有者）。"  # 權限不足提示
    else:
        permission_hint = "點擊下方語言按鈕即可切換勾選狀態。"  # 操作提示

    button_contents = []  # 語言按鈕集合

    for tag, pretty_name, command_name, language_code in LANGUAGE_MENU_ITEMS:
        is_selected = language_code in selected_codes  # 是否已勾選
        label_text = f"✅ {tag} {pretty_name}" if is_selected else f"{tag} {pretty_name}"  # 顯示文字
        action_text = f"設定語言 {command_name}"  # 送出命令

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
    )  # 建立語言設定 Bubble

    return FlexMessage(
        altText="翻翻君語言設定",
        contents=bubble,
        quickReply=None,
    )  # 回傳語言設定訊息


def build_main_menu_json(
    source_type: str,
    is_group_manager: bool,
    current_language_code: str = "zh-TW",
) -> dict:
    menu_message = build_main_menu_card(
        source_type,
        is_group_manager,
        current_language_code,
    )  # 產生主選單

    if hasattr(menu_message, "to_dict"):
        return menu_message.to_dict()  # 轉為完整 JSON

    return {"altText": menu_message.alt_text, "contents": {}}  # 防禦性回傳