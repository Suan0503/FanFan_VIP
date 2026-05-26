from typing import TypedDict


class TravelResultI18n(TypedDict):
    title: str
    region_label: str
    landmarks_label: str
    restaurants_label: str
    exchange_label: str
    no_data: str
    preference_label: str
    progress_title: str
    progress_region: str
    progress_places: str
    progress_ai: str


TRAVEL_RESULT_I18N: dict[str, TravelResultI18n] = {
    "zh-TW": {
        "title": "🧭 旅遊模式探索結果",
        "region_label": "📍 區域",
        "landmarks_label": "🏛 附近地標",
        "restaurants_label": "🍜 附近餐廳",
        "exchange_label": "💱 匯率參考",
        "no_data": "暫無資料",
        "preference_label": "🎯 偏好條件",
        "progress_title": "🧭 搜尋進度",
        "progress_region": "定位與區域分析",
        "progress_places": "附近地點搜尋",
        "progress_ai": "AI整理回覆",
    },
    "en": {
        "title": "🧭 Travel Mode Results",
        "region_label": "📍 Area",
        "landmarks_label": "🏛 Nearby Landmarks",
        "restaurants_label": "🍜 Nearby Restaurants",
        "exchange_label": "💱 Exchange Rate",
        "no_data": "No data",
        "preference_label": "🎯 Preferences",
        "progress_title": "🧭 Search Progress",
        "progress_region": "Location and area analysis",
        "progress_places": "Nearby place lookup",
        "progress_ai": "AI response drafting",
    },
    "ja": {
        "title": "🧭 旅行モード探索結果",
        "region_label": "📍 エリア",
        "landmarks_label": "🏛 周辺スポット",
        "restaurants_label": "🍜 周辺レストラン",
        "exchange_label": "💱 為替情報",
        "no_data": "データなし",
        "preference_label": "🎯 条件",
        "progress_title": "🧭 検索進捗",
        "progress_region": "位置とエリア解析",
        "progress_places": "周辺スポット検索",
        "progress_ai": "AI応答生成",
    },
    "th": {
        "title": "🧭 ผลลัพธ์โหมดท่องเที่ยว",
        "region_label": "📍 พื้นที่",
        "landmarks_label": "🏛 สถานที่ใกล้เคียง",
        "restaurants_label": "🍜 ร้านอาหารใกล้เคียง",
        "exchange_label": "💱 อัตราแลกเปลี่ยน",
        "no_data": "ไม่มีข้อมูล",
        "preference_label": "🎯 เงื่อนไข",
        "progress_title": "🧭 ความคืบหน้าการค้นหา",
        "progress_region": "ระบุตำแหน่งและวิเคราะห์พื้นที่",
        "progress_places": "ค้นหาสถานที่ใกล้เคียง",
        "progress_ai": "AI กำลังสรุปคำตอบ",
    },
    "vi": {
        "title": "🧭 Kết quả chế độ du lịch",
        "region_label": "📍 Khu vực",
        "landmarks_label": "🏛 Địa danh gần đây",
        "restaurants_label": "🍜 Nhà hàng gần đây",
        "exchange_label": "💱 Tỷ giá",
        "no_data": "Chưa có dữ liệu",
        "preference_label": "🎯 Tùy chọn",
        "progress_title": "🧭 Tiến trình tìm kiếm",
        "progress_region": "Định vị và phân tích khu vực",
        "progress_places": "Tìm địa điểm gần đây",
        "progress_ai": "AI tổng hợp phản hồi",
    },
    "ko": {
        "title": "🧭 여행 모드 탐색 결과",
        "region_label": "📍 지역",
        "landmarks_label": "🏛 주변 명소",
        "restaurants_label": "🍜 주변 식당",
        "exchange_label": "💱 환율 정보",
        "no_data": "데이터 없음",
        "preference_label": "🎯 선호 조건",
        "progress_title": "🧭 검색 진행도",
        "progress_region": "위치 및 지역 분석",
        "progress_places": "주변 장소 검색",
        "progress_ai": "AI 응답 정리",
    },
    "id": {
        "title": "🧭 Hasil Mode Wisata",
        "region_label": "📍 Area",
        "landmarks_label": "🏛 Landmark Terdekat",
        "restaurants_label": "🍜 Restoran Terdekat",
        "exchange_label": "💱 Kurs",
        "no_data": "Data belum tersedia",
        "preference_label": "🎯 Preferensi",
        "progress_title": "🧭 Progres pencarian",
        "progress_region": "Analisis lokasi dan area",
        "progress_places": "Mencari tempat terdekat",
        "progress_ai": "AI merangkum jawaban",
    },
    "my": {
        "title": "🧭 ခရီးသွားမုဒ် ရလဒ်",
        "region_label": "📍 ဧရိယာ",
        "landmarks_label": "🏛 အနီးအနားနေရာများ",
        "restaurants_label": "🍜 အနီးအနားစားသောက်ဆိုင်များ",
        "exchange_label": "💱 ငွေလဲနှုန်း",
        "no_data": "ဒေတာမရှိသေးပါ",
        "preference_label": "🎯 သတ်မှတ်ချက်",
        "progress_title": "🧭 ရှာဖွေမှုအခြေအနေ",
        "progress_region": "တည်နေရာနှင့်ဧရိယာခွဲခြမ်းစိတ်ဖြာမှု",
        "progress_places": "အနီးအနားနေရာရှာဖွေမှု",
        "progress_ai": "AI အဖြေပြင်ဆင်နေသည်",
    },
    "ru": {
        "title": "🧭 Результаты режима путешествий",
        "region_label": "📍 Район",
        "landmarks_label": "🏛 Достопримечательности рядом",
        "restaurants_label": "🍜 Рестораны рядом",
        "exchange_label": "💱 Курс валют",
        "no_data": "Нет данных",
        "preference_label": "🎯 Предпочтения",
        "progress_title": "🧭 Прогресс поиска",
        "progress_region": "Определение локации и района",
        "progress_places": "Поиск мест рядом",
        "progress_ai": "AI формирует ответ",
    },
}


def get_travel_result_i18n(language_code: str) -> TravelResultI18n:
    return TRAVEL_RESULT_I18N.get(language_code, TRAVEL_RESULT_I18N["zh-TW"])
