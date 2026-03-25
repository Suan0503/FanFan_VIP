from datetime import datetime  # 匯入時間型別

from sqlalchemy import String, DateTime, Boolean, UniqueConstraint  # 匯入欄位型別
from sqlalchemy.orm import Mapped, mapped_column  # 匯入欄位映射

from app.db.base import Base  # 匯入 Base


class UserProfile(Base):
    __tablename__ = "user_profiles"  # 使用者資料表

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    line_user_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)  # LINE ID
    member_code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)  # FAN 編號
    target_language: Mapped[str] = mapped_column(String(16), nullable=False, default="zh-TW")  # 目標語言
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # 管理員旗標
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間


class GroupSetting(Base):
    __tablename__ = "group_settings"  # 群組設定表
    __table_args__ = (UniqueConstraint("line_group_id", name="uq_group_id"),)  # 群組唯一約束

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    line_group_id: Mapped[str] = mapped_column(String(64), nullable=False)  # 群組 ID
    inviter_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)  # 邀請者代表 ID
    target_language: Mapped[str] = mapped_column(String(16), nullable=False, default="zh-TW")  # 群組語言
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間
