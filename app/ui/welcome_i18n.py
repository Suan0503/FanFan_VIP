from typing import TypedDict


class WelcomeI18n(TypedDict):
    title: str
    started: str
    account_id: str
    system_status: str
    running: str
    smart_region: str
    auto_detected: str
    auto_config_done: str
    language_mode: str
    service_node: str


WELCOME_I18N: dict[str, WelcomeI18n] = {
    "zh-TW": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "智慧翻譯系統已啟動",
        "account_id": "🆔 帳號編號",
        "system_status": "🟢 系統狀態",
        "running": "正常運作中",
        "smart_region": "🌏 智慧地區配置",
        "auto_detected": "已自動偵測：{region}",
        "auto_config_done": "⚙ 自動配置完成",
        "language_mode": "語言模式：{mode}",
        "service_node": "服務節點：{node}",
    },
    "en": {
        "title": "🌏 FanFan VIP | FanFan V1.0",
        "started": "Smart translation system is online",
        "account_id": "🆔 Account ID",
        "system_status": "🟢 System Status",
        "running": "Running normally",
        "smart_region": "🌏 Smart Region Setup",
        "auto_detected": "Auto-detected: {region}",
        "auto_config_done": "⚙ Auto Setup Completed",
        "language_mode": "Language Mode: {mode}",
        "service_node": "Service Node: {node}",
    },
    "ja": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "スマート翻訳システムを起動しました",
        "account_id": "🆔 アカウントID",
        "system_status": "🟢 システム状態",
        "running": "正常に稼働中",
        "smart_region": "🌏 スマート地域設定",
        "auto_detected": "自動検出：{region}",
        "auto_config_done": "⚙ 自動設定完了",
        "language_mode": "言語モード：{mode}",
        "service_node": "サービスノード：{node}",
    },
    "th": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "ระบบแปลอัจฉริยะพร้อมใช้งานแล้ว",
        "account_id": "🆔 รหัสบัญชี",
        "system_status": "🟢 สถานะระบบ",
        "running": "ระบบทำงานปกติ",
        "smart_region": "🌏 การตั้งค่าภูมิภาคอัจฉริยะ",
        "auto_detected": "ตรวจพบอัตโนมัติ: {region}",
        "auto_config_done": "⚙ ตั้งค่าอัตโนมัติเรียบร้อย",
        "language_mode": "โหมดภาษา: {mode}",
        "service_node": "โหนดบริการ: {node}",
    },
    "vi": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "Hệ thống dịch thông minh đã khởi động",
        "account_id": "🆔 Mã tài khoản",
        "system_status": "🟢 Trạng thái hệ thống",
        "running": "Đang hoạt động bình thường",
        "smart_region": "🌏 Cấu hình khu vực thông minh",
        "auto_detected": "Đã tự động nhận diện: {region}",
        "auto_config_done": "⚙ Hoàn tất cấu hình tự động",
        "language_mode": "Chế độ ngôn ngữ: {mode}",
        "service_node": "Nút dịch vụ: {node}",
    },
    "ko": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "스마트 번역 시스템이 시작되었습니다",
        "account_id": "🆔 계정 번호",
        "system_status": "🟢 시스템 상태",
        "running": "정상 작동 중",
        "smart_region": "🌏 스마트 지역 설정",
        "auto_detected": "자동 감지: {region}",
        "auto_config_done": "⚙ 자동 설정 완료",
        "language_mode": "언어 모드: {mode}",
        "service_node": "서비스 노드: {node}",
    },
    "id": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "Sistem terjemahan pintar telah aktif",
        "account_id": "🆔 ID Akun",
        "system_status": "🟢 Status Sistem",
        "running": "Berjalan normal",
        "smart_region": "🌏 Konfigurasi wilayah pintar",
        "auto_detected": "Terdeteksi otomatis: {region}",
        "auto_config_done": "⚙ Konfigurasi otomatis selesai",
        "language_mode": "Mode bahasa: {mode}",
        "service_node": "Node layanan: {node}",
    },
    "my": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "စမတ်ဘာသာပြန်စနစ် စတင်ပြီးပါပြီ",
        "account_id": "🆔 အကောင့်နံပါတ်",
        "system_status": "🟢 စနစ်အခြေအနေ",
        "running": "ပုံမှန်လည်ပတ်နေသည်",
        "smart_region": "🌏 စမတ်ဒေသ ပြင်ဆင်မှု",
        "auto_detected": "အလိုအလျောက် ရှာဖွေတွေ့ရှိသည်: {region}",
        "auto_config_done": "⚙ အလိုအလျောက် ပြင်ဆင်မှု ပြီးဆုံး",
        "language_mode": "ဘာသာစကားမုဒ်: {mode}",
        "service_node": "ဝန်ဆောင်မှု node: {node}",
    },
    "ru": {
        "title": "🌏 FanFan VIP｜翻翻君 V1.0",
        "started": "Умная система перевода запущена",
        "account_id": "🆔 Номер аккаунта",
        "system_status": "🟢 Состояние системы",
        "running": "Работает нормально",
        "smart_region": "🌏 Умная региональная настройка",
        "auto_detected": "Автоопределено: {region}",
        "auto_config_done": "⚙ Автонастройка завершена",
        "language_mode": "Языковой режим: {mode}",
        "service_node": "Сервисный узел: {node}",
    },
}


def get_welcome_i18n(language_code: str) -> WelcomeI18n:
    return WELCOME_I18N.get(language_code, WELCOME_I18N["zh-TW"])
