from sqlalchemy import create_engine  # 匯入引擎
from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker  # 匯入 Session 工廠

from app.core.config import settings  # 匯入設定
from app.core.database import normalize_database_url  # 匯入資料庫 URL 處理
from app.db.base import Base  # 匯入 Base
from app.db import models  # noqa: F401  # 載入模型以建立資料表


engine = create_engine(normalize_database_url(settings.database_url), pool_pre_ping=True, future=True)  # 建立引擎
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)  # 建立 Session


def init_db() -> None:
    Base.metadata.create_all(bind=engine)  # 建立所有資料表
    _ensure_group_name_cache_columns()  # 補齊舊版資料庫缺少欄位


def _ensure_group_name_cache_columns() -> None:
    inspector = inspect(engine)
    dialect_name = engine.dialect.name.lower()
    table_names = set(inspector.get_table_names())
    if "group_settings" not in table_names:
        return

    columns = {col["name"] for col in inspector.get_columns("group_settings")}
    statements: list[str] = []
    if "group_name" not in columns:
        statements.append("ALTER TABLE group_settings ADD COLUMN group_name VARCHAR(255)")
    if "group_name_synced_at" not in columns:
        if dialect_name == "postgresql":
            statements.append("ALTER TABLE group_settings ADD COLUMN group_name_synced_at TIMESTAMP")
        else:
            statements.append("ALTER TABLE group_settings ADD COLUMN group_name_synced_at DATETIME")

    if not statements:
        return

    with engine.begin() as conn:
        for sql in statements:
            conn.execute(text(sql))
