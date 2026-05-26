from typing import TypedDict


class TravelI18n(TypedDict):
    menu_button: str
    entry_command: str
    title: str
    subtitle: str
    description: str
    agree_button: str
    back_button: str
    confirm_command: str
    back_command: str
    location_prompt: str
    location_quick_reply_label: str
    not_enabled_yet: str
    loading: str
    audio_need_location: str
    audio_transcribing: str
    audio_transcribe_failed: str
    temporary_unavailable: str


TRAVEL_I18N: dict[str, TravelI18n] = {
    "zh-TW": {
        "menu_button": "🧭 旅遊模式",
        "entry_command": "旅遊模式",
        "title": "🧭 旅遊模式",
        "subtitle": "探索附近地標與餐廳",
        "description": "說明:旅遊模式會自動獲取當下位置，使用翻翻君AI助理幫你探索附近的地標或是餐廳。",
        "agree_button": "確定",
        "back_button": "返回",
        "confirm_command": "旅遊模式確認",
        "back_command": "旅遊模式返回",
        "location_prompt": "請按下方按鈕分享目前位置，翻翻君會開始探索附近景點與餐廳。",
        "location_quick_reply_label": "分享目前位置",
        "not_enabled_yet": "尚未啟用旅遊模式。請先從主選單進入旅遊模式並按確定。",
        "loading": "正在探索附近地標與餐廳，請稍候...",
        "audio_need_location": "請先在旅遊模式分享一次位置，再傳語音需求。",
        "audio_transcribing": "正在使用 Whisper 解析語音，請稍候...",
        "audio_transcribe_failed": "語音辨識失敗，請再說一次或改用文字輸入。",
        "temporary_unavailable": "目前暫時無法取得附近資料，請稍後再試。",
    },
    "en": {
        "menu_button": "🧭 Travel Mode",
        "entry_command": "travel mode",
        "title": "🧭 Travel Mode",
        "subtitle": "Explore nearby landmarks and food",
        "description": "Travel mode uses your current location and FanFan AI assistant to explore nearby landmarks and restaurants.",
        "agree_button": "Confirm",
        "back_button": "Back",
        "confirm_command": "travel mode confirm",
        "back_command": "travel mode back",
        "location_prompt": "Tap the button below to share your location. FanFan will explore nearby spots and restaurants.",
        "location_quick_reply_label": "Share location",
        "not_enabled_yet": "Travel mode is not enabled yet. Please enter Travel Mode from the main menu and tap Confirm.",
        "loading": "Exploring nearby places, please wait...",
        "audio_need_location": "Please share your location once in Travel Mode before sending a voice request.",
        "audio_transcribing": "Transcribing voice with Whisper, please wait...",
        "audio_transcribe_failed": "Voice transcription failed. Please try again or type your request.",
        "temporary_unavailable": "Nearby data is temporarily unavailable. Please try again later.",
    },
    "ja": {
        "menu_button": "🧭 旅行モード",
        "entry_command": "旅行モード",
        "title": "🧭 旅行モード",
        "subtitle": "近くの名所とレストランを探索",
        "description": "旅行モードは現在地を取得し、FanFan AIが近くの名所やレストランを案内します。",
        "agree_button": "確認",
        "back_button": "戻る",
        "confirm_command": "旅行モード確認",
        "back_command": "旅行モード戻る",
        "location_prompt": "下のボタンを押して現在地を共有してください。近くの観光地と飲食店を探します。",
        "location_quick_reply_label": "現在地を共有",
        "not_enabled_yet": "旅行モードが有効ではありません。先にメニューから旅行モードで確認を押してください。",
        "loading": "周辺スポットを検索中です。しばらくお待ちください...",
        "audio_need_location": "先に旅行モードで位置情報を1回共有してから音声を送信してください。",
        "audio_transcribing": "Whisperで音声を解析中です。少々お待ちください...",
        "audio_transcribe_failed": "音声認識に失敗しました。もう一度話すかテキストで入力してください。",
        "temporary_unavailable": "現在、周辺情報を取得できません。後でもう一度お試しください。",
    },
    "th": {
        "menu_button": "🧭 โหมดท่องเที่ยว",
        "entry_command": "โหมดท่องเที่ยว",
        "title": "🧭 โหมดท่องเที่ยว",
        "subtitle": "สำรวจสถานที่และร้านอาหารใกล้เคียง",
        "description": "โหมดท่องเที่ยวจะใช้ตำแหน่งปัจจุบัน และให้ผู้ช่วย AI ของ FanFan ช่วยสำรวจสถานที่และร้านอาหารใกล้คุณ",
        "agree_button": "ยืนยัน",
        "back_button": "กลับ",
        "confirm_command": "ยืนยันโหมดท่องเที่ยว",
        "back_command": "กลับโหมดท่องเที่ยว",
        "location_prompt": "กรุณากดปุ่มด้านล่างเพื่อแชร์ตำแหน่งปัจจุบัน แล้ว FanFan จะสำรวจสถานที่ใกล้คุณ",
        "location_quick_reply_label": "แชร์ตำแหน่งปัจจุบัน",
        "not_enabled_yet": "ยังไม่ได้เปิดโหมดท่องเที่ยว โปรดเข้าโหมดท่องเที่ยวและกดยืนยันก่อน",
        "loading": "กำลังสำรวจสถานที่ใกล้เคียง กรุณารอสักครู่...",
        "audio_need_location": "กรุณาแชร์ตำแหน่งในโหมดท่องเที่ยวก่อน แล้วค่อยส่งเสียง",
        "audio_transcribing": "กำลังถอดเสียงด้วย Whisper กรุณารอสักครู่...",
        "audio_transcribe_failed": "ถอดเสียงไม่สำเร็จ กรุณาลองใหม่หรือพิมพ์ข้อความ",
        "temporary_unavailable": "ยังไม่สามารถดึงข้อมูลใกล้เคียงได้ในขณะนี้ โปรดลองใหม่ภายหลัง",
    },
    "vi": {
        "menu_button": "🧭 Chế độ du lịch",
        "entry_command": "che do du lich",
        "title": "🧭 Chế độ du lịch",
        "subtitle": "Khám phá địa danh và quán ăn gần bạn",
        "description": "Chế độ du lịch sẽ dùng vị trí hiện tại để FanFan AI gợi ý địa danh và nhà hàng xung quanh.",
        "agree_button": "Xác nhận",
        "back_button": "Quay lại",
        "confirm_command": "xac nhan che do du lich",
        "back_command": "quay lai che do du lich",
        "location_prompt": "Vui lòng bấm nút bên dưới để chia sẻ vị trí hiện tại, FanFan sẽ bắt đầu khám phá khu vực gần bạn.",
        "location_quick_reply_label": "Chia sẻ vị trí",
        "not_enabled_yet": "Bạn chưa bật chế độ du lịch. Hãy vào chế độ du lịch và nhấn xác nhận trước.",
        "loading": "Đang khám phá địa điểm gần bạn, vui lòng chờ...",
        "audio_need_location": "Hãy chia sẻ vị trí một lần trong chế độ du lịch trước khi gửi giọng nói.",
        "audio_transcribing": "Đang dùng Whisper để nhận dạng giọng nói, vui lòng chờ...",
        "audio_transcribe_failed": "Nhận dạng giọng nói thất bại. Vui lòng thử lại hoặc nhập văn bản.",
        "temporary_unavailable": "Tạm thời không lấy được dữ liệu xung quanh. Vui lòng thử lại sau.",
    },
    "ko": {
        "menu_button": "🧭 여행 모드",
        "entry_command": "여행 모드",
        "title": "🧭 여행 모드",
        "subtitle": "근처 명소와 맛집 탐색",
        "description": "여행 모드는 현재 위치를 기반으로 FanFan AI가 주변 명소와 식당을 추천합니다.",
        "agree_button": "확인",
        "back_button": "뒤로",
        "confirm_command": "여행 모드 확인",
        "back_command": "여행 모드 뒤로",
        "location_prompt": "아래 버튼으로 현재 위치를 공유해 주세요. 주변 명소와 식당을 탐색합니다.",
        "location_quick_reply_label": "현재 위치 공유",
        "not_enabled_yet": "여행 모드가 아직 활성화되지 않았습니다. 먼저 여행 모드에서 확인을 눌러 주세요.",
        "loading": "주변 장소를 탐색 중입니다. 잠시만 기다려 주세요...",
        "audio_need_location": "여행 모드에서 위치를 먼저 한 번 공유한 후 음성을 보내 주세요.",
        "audio_transcribing": "Whisper로 음성을 변환 중입니다. 잠시만 기다려 주세요...",
        "audio_transcribe_failed": "음성 인식에 실패했습니다. 다시 시도하거나 텍스트로 입력해 주세요.",
        "temporary_unavailable": "현재 주변 데이터를 불러올 수 없습니다. 잠시 후 다시 시도해 주세요.",
    },
    "id": {
        "menu_button": "🧭 Mode Wisata",
        "entry_command": "mode wisata",
        "title": "🧭 Mode Wisata",
        "subtitle": "Jelajahi tempat dan kuliner sekitar",
        "description": "Mode wisata menggunakan lokasi saat ini, lalu asisten AI FanFan membantu mencari landmark dan restoran terdekat.",
        "agree_button": "Konfirmasi",
        "back_button": "Kembali",
        "confirm_command": "konfirmasi mode wisata",
        "back_command": "kembali mode wisata",
        "location_prompt": "Tekan tombol di bawah untuk membagikan lokasi saat ini. FanFan akan mulai menjelajah area sekitarmu.",
        "location_quick_reply_label": "Bagikan lokasi",
        "not_enabled_yet": "Mode wisata belum aktif. Masuk ke Mode Wisata dan tekan Konfirmasi dulu.",
        "loading": "Sedang menjelajahi tempat sekitar, mohon tunggu...",
        "audio_need_location": "Bagikan lokasi sekali di Mode Wisata sebelum mengirim suara.",
        "audio_transcribing": "Sedang mentranskripsi suara dengan Whisper, mohon tunggu...",
        "audio_transcribe_failed": "Transkripsi suara gagal. Coba lagi atau kirim teks.",
        "temporary_unavailable": "Data sekitar sedang tidak tersedia. Silakan coba lagi nanti.",
    },
    "my": {
        "menu_button": "🧭 ခရီးသွားမုဒ်",
        "entry_command": "ခရီးသွားမုဒ်",
        "title": "🧭 ခရီးသွားမုဒ်",
        "subtitle": "အနီးအနားနေရာများနှင့်စားသောက်ဆိုင်များရှာဖွေရန်",
        "description": "ခရီးသွားမုဒ်သည် လက်ရှိတည်နေရာကိုအသုံးပြုပြီး FanFan AI က အနီးအနားနေရာများနှင့်စားသောက်ဆိုင်များကိုရှာပေးသည်။",
        "agree_button": "အတည်ပြု",
        "back_button": "နောက်သို့",
        "confirm_command": "ခရီးသွားမုဒ်အတည်ပြု",
        "back_command": "ခရီးသွားမုဒ်နောက်သို့",
        "location_prompt": "အောက်ပါခလုတ်ကိုနှိပ်ပြီး လက်ရှိတည်နေရာကိုမျှဝေပါ။ FanFan က အနီးအနားနေရာများကို စတင်ရှာပေးမည်။",
        "location_quick_reply_label": "တည်နေရာမျှဝေမည်",
        "not_enabled_yet": "ခရီးသွားမုဒ် မဖွင့်ရသေးပါ။ မူလမီနူးမှ ဝင်ပြီး အတည်ပြုကိုနှိပ်ပါ။",
        "loading": "အနီးအနားနေရာများ ရှာဖွေနေသည်၊ ကျေးဇူးပြု၍ ခဏစောင့်ပါ...",
        "audio_need_location": "အသံမပို့မီ ခရီးသွားမုဒ်တွင် တည်နေရာကို တစ်ကြိမ် မျှဝေပေးပါ။",
        "audio_transcribing": "Whisper ဖြင့် အသံကို စာသားသို့ပြောင်းနေသည်၊ ခဏစောင့်ပါ...",
        "audio_transcribe_failed": "အသံမှတ်တမ်း မအောင်မြင်ပါ။ ထပ်မံပြောပါ သို့မဟုတ် စာဖြင့်ပို့ပါ။",
        "temporary_unavailable": "လက်ရှိအချိန်တွင် အနီးအနားဒေတာမရနိုင်ပါ။ နောက်မှပြန်စမ်းပါ။",
    },
    "ru": {
        "menu_button": "🧭 Режим путешествий",
        "entry_command": "режим путешествий",
        "title": "🧭 Режим путешествий",
        "subtitle": "Поиск достопримечательностей и ресторанов рядом",
        "description": "Режим путешествий использует ваше местоположение, а AI-помощник FanFan подсказывает ближайшие места и рестораны.",
        "agree_button": "Подтвердить",
        "back_button": "Назад",
        "confirm_command": "подтвердить режим путешествий",
        "back_command": "назад режим путешествий",
        "location_prompt": "Нажмите кнопку ниже и отправьте текущее местоположение. FanFan начнет поиск рядом с вами.",
        "location_quick_reply_label": "Отправить локацию",
        "not_enabled_yet": "Режим путешествий еще не включен. Откройте режим и нажмите Подтвердить.",
        "loading": "Идет поиск мест рядом, пожалуйста подождите...",
        "audio_need_location": "Сначала отправьте локацию в режиме путешествий, затем отправьте голосовой запрос.",
        "audio_transcribing": "Распознаю голос через Whisper, пожалуйста подождите...",
        "audio_transcribe_failed": "Не удалось распознать голос. Повторите или отправьте текст.",
        "temporary_unavailable": "Сейчас не удалось получить данные поблизости. Попробуйте позже.",
    },
}


def get_travel_i18n(language_code: str) -> TravelI18n:
    return TRAVEL_I18N.get(language_code, TRAVEL_I18N["zh-TW"])


def _normalize_command(value: str) -> str:
    return value.strip().lower()


def get_travel_entry_commands() -> set[str]:
    return {_normalize_command(item["entry_command"]) for item in TRAVEL_I18N.values()}


def get_travel_confirm_commands() -> set[str]:
    return {_normalize_command(item["confirm_command"]) for item in TRAVEL_I18N.values()}


def get_travel_back_commands() -> set[str]:
    return {_normalize_command(item["back_command"]) for item in TRAVEL_I18N.values()}
