from pydantic import AliasChoices, Field  # 匯入欄位別名工具
from pydantic_settings import BaseSettings, SettingsConfigDict  # 匯入設定基底


class Settings(BaseSettings):
    project_name: str = "FanFan Translator"  # 專案名稱
    environment: str = "production"  # 執行環境
    line_channel_access_token: str = Field(default="", validation_alias=AliasChoices("LINE_CHANNEL_ACCESS_TOKEN", "CHANNEL_ACCESS_TOKEN"))  # LINE Token
    line_channel_secret: str = Field(default="", validation_alias=AliasChoices("LINE_CHANNEL_SECRET", "CHANNEL_SECRET"))  # LINE Secret
    azure_translator_endpoint: str = Field(default="", validation_alias=AliasChoices("AZURE_TRANSLATOR_ENDPOINT"))  # Azure Translator Endpoint
    azure_translator_key: str = Field(default="", validation_alias=AliasChoices("AZURE_TRANSLATOR_KEY"))  # Azure Translator Key
    azure_translator_region: str = Field(default="", validation_alias=AliasChoices("AZURE_TRANSLATOR_REGION"))  # Azure Translator Region
    deepl_api_key: str = Field(default="", validation_alias=AliasChoices("DEEPL_API_KEY", "DEEPL_AUTH_KEY"))  # DeepL API Key
    groq_api_key: str = Field(default="", validation_alias=AliasChoices("GROQ_API_KEY"))  # Groq API Key
    google_ai_studio_api_key: str = Field(default="", validation_alias=AliasChoices("GOOGLE_AI_STUDIO_API_KEY", "GOOGLE_API_KEY"))  # Google AI Studio Key
    exchange_rate_api_key: str = Field(default="", validation_alias=AliasChoices("EXCHANGE_RATE_API_KEY"))  # ExchangeRate API Key
    translation_channel: str = Field(default="deepl", validation_alias=AliasChoices("TRANSLATION_CHANNEL"))  # 一般用戶翻譯預設通道
    app_owner_user_ids: str = Field(default="", validation_alias=AliasChoices("APP_OWNER_USER_IDS"))  # 所有者 ID 字串
    database_url: str = Field(default="sqlite:///./translator.db", validation_alias=AliasChoices("DATABASE_URL"))  # 資料庫連線

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")  # 指定 .env

    @property
    def owner_user_ids(self) -> set[str]:
        if not self.app_owner_user_ids.strip():
            return set()  # 無設定時回傳空集合
        return {user_id.strip() for user_id in self.app_owner_user_ids.split(",") if user_id.strip()}  # 解析所有者


settings = Settings()  # 產生全域設定
