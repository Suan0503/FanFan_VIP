from sqlalchemy import create_engine  # 匯入引擎
from sqlalchemy.orm import sessionmaker  # 匯入 Session 工廠

from app.core.config import settings  # 匯入設定
from app.core.database import normalize_database_url  # 匯入資料庫 URL 處理
from app.db.base import Base  # 匯入 Base
from app.db import models  # noqa: F401  # 載入模型以建立資料表


engine = create_engine(normalize_database_url(settings.database_url), pool_pre_ping=True, future=True)  # 建立引擎
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)  # 建立 Session


def init_db() -> None:
    Base.metadata.create_all(bind=engine)  # 建立所有資料表
