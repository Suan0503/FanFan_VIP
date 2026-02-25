"""
Configuration module - 統一管理所有設定和常數
"""
import os
from dotenv import load_dotenv

# 載入 .env 檔
load_dotenv()

# ============== Flask 設定 ==============
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
HOST = '0.0.0.0'
PORT = int(os.getenv('PORT', 5000))

# ============== 資料庫設定 ==============
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ============== LINE Bot 設定 ==============
# support both old and new env var names for convenience
_channel_token = os.getenv('CHANNEL_ACCESS_TOKEN') or os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_ACCESS_TOKEN = _channel_token or ''
_channel_secret = os.getenv('CHANNEL_SECRET') or os.getenv('LINE_CHANNEL_SECRET')
CHANNEL_SECRET = (_channel_secret or '').encode('utf-8')

# runtime check for missing credentials
if not CHANNEL_ACCESS_TOKEN:
    print('WARNING: CHANNEL_ACCESS_TOKEN is not set. Bot replies will fail.')
if not CHANNEL_SECRET:
    print('WARNING: CHANNEL_SECRET is not set. Webhook signature validation may fail.')

# ============== 翻譯服務設定 ==============
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY', '')
DEEPL_API_BASE_URL = os.getenv('DEEPL_API_BASE_URL', 'https://api-free.deepl.com')
GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

# Google 翻譯 timeout 設定 (connect_timeout, read_timeout) [已優化]
GOOGLE_TIMEOUT = (1.5, 3)
# DeepL 翻譯 timeout 設定 (connect_timeout, read_timeout) [已優化]
DEEPL_TIMEOUT = (2, 5)
# 翻譯重試次數
MAX_TRANSLATION_RETRIES = 1  # 單次嘗試，快速失敗以支援 fallback

# ============== 翻譯執行緒限制 ==============
MAX_CONCURRENT_TRANSLATIONS = 4

# ============== 檔案存儲 ==============
MASTER_USER_FILE = "master_user_ids.json"
DATA_FILE = "data.json"

# ============== 預設主人列表 ==============
DEFAULT_MASTER_USER_IDS = {
    'U5ce6c382d12eaea28d98f2d48673b4b8',
    'U2bcd63000805da076721eb62872bc39f',
    'Uea1646aa1a57861c85270d846aaee0eb',
    'U8f3cc921a9dd18d3e257008a34dd07c1'
}

# ============== 語言映射 ==============
LANGUAGE_MAP = {
    '🇹🇼 中文(台灣)': 'zh-TW',
    '🇺🇸 英文': 'en',
    '🇹🇭 泰文': 'th',
    '🇻🇳 越南文': 'vi',
    '🇲🇲 緬甸文': 'my',
    '🇰🇷 韓文': 'ko',
    '🇮🇩 印尼文': 'id',
    '🇯🇵 日文': 'ja',
    '🇷🇺 俄文': 'ru'
}

# 預設翻譯語言
DEFAULT_LANGUAGES = {'zh-TW'}

# ============== 系統設定 ==============
INACTIVE_GROUP_DAYS = 20  # 超過多少天未使用的群組會自動退出
KEEP_ALIVE_INTERVAL = 300  # Keep-alive 檢查間隔（秒）
AUTO_RESTART_INTERVAL = 10800  # 自動重啟間隔（秒）

# ============== 快取設定 ==============
TRANSLATION_CACHE_TTL = 3600  # 翻譯結果快取時間 (秒)
TRANSLATION_CACHE_SIZE = 1000  # 翻譯結果快取大小 (記錄數)
GROUP_LANGS_CACHE_TTL = 300  # 群組語言設定快取時間 (秒)

# ============== 日誌設定 ==============
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
