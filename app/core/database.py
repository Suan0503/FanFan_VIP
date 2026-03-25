from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse  # 匯入 URL 解析工具


def normalize_database_url(raw_url: str) -> str:
    db_url = (raw_url or "").strip()  # 清理空白
    if not db_url:
        return "sqlite:///./translator.db"  # 預設回退 SQLite

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)  # 相容 Railway 舊格式

    if db_url.startswith("postgresql://") and "+" not in db_url.split("://", 1)[0]:
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)  # 指定 psycopg2 driver

    parsed = urlparse(db_url)  # 解析 URL
    if parsed.scheme.startswith("postgresql"):
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))  # 轉 query 參數
        if "sslmode" not in query_params:
            query_params["sslmode"] = "require"  # Railway 建議使用 SSL
        db_url = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(query_params),
                parsed.fragment,
            )
        )  # 重組 URL

    return db_url  # 回傳處理後 URL
