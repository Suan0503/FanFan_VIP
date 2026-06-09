from datetime import datetime  # 匯入時間型別

from sqlalchemy import String, DateTime, Boolean, UniqueConstraint, ForeignKey  # 匯入欄位型別
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
    group_name: Mapped[str | None] = mapped_column(String(255), nullable=True)  # 群組名稱快取
    group_name_synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # 群組名稱最後同步時間
    inviter_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)  # 邀請者代表 ID
    target_language: Mapped[str] = mapped_column(String(16), nullable=False, default="zh-TW")  # 群組語言
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間


class GroupLanguageSelection(Base):
    __tablename__ = "group_language_selections"  # 群組多語設定表
    __table_args__ = (
        UniqueConstraint("line_group_id", "language_code", name="uq_group_language_pair"),
    )  # 群組與語言唯一

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    line_group_id: Mapped[str] = mapped_column(String(64), ForeignKey("group_settings.line_group_id"), nullable=False)  # 群組 ID
    language_code: Mapped[str] = mapped_column(String(16), nullable=False)  # 語言代碼
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間


class VIPSerialCode(Base):
    __tablename__ = "vip_serial_codes"  # VIP 序號資料表
    __table_args__ = (
        UniqueConstraint("serial_code", name="uq_vip_serial_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    serial_code: Mapped[str] = mapped_column(String(32), nullable=False)  # 序號
    created_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # 產生者 LINE ID
    created_by_name: Mapped[str] = mapped_column(String(128), nullable=False)  # 產生者顯示名稱
    created_by_member_code: Mapped[str | None] = mapped_column(String(16), nullable=True)  # 產生者會員編號
    base_days: Mapped[int] = mapped_column(nullable=False, default=30)  # 基礎天數
    extra_days: Mapped[int] = mapped_column(nullable=False, default=0)  # 額外天數
    total_days: Mapped[int] = mapped_column(nullable=False, default=30)  # 實際總天數
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # 是否已使用
    used_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)  # 使用者 LINE ID
    used_by_member_code: Mapped[str | None] = mapped_column(String(16), nullable=True)  # 使用者會員編號
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # 使用時間
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間


class VIPSubscription(Base):
    __tablename__ = "vip_subscriptions"  # VIP 會員資料表
    __table_args__ = (
        UniqueConstraint("line_user_id", name="uq_vip_line_user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    line_user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # 會員 LINE ID
    member_code: Mapped[str] = mapped_column(String(16), nullable=False)  # 會員編號
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 本次方案起始時間
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 方案到期時間
    current_plan: Mapped[str] = mapped_column(String(64), nullable=False, default="VIP-AZURE-100K")  # 目前方案
    remaining_chars: Mapped[int] = mapped_column(nullable=False, default=100000)  # 剩餘字數
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 更新時間


class VIPUsageLog(Base):
    __tablename__ = "vip_usage_logs"  # VIP 使用量紀錄表

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 主鍵
    line_user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # 額度擁有者 LINE ID
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)  # 來源類型 user/group
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)  # 來源 ID
    consumed_chars: Mapped[int] = mapped_column(nullable=False, default=0)  # 消耗字數
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  # 建立時間
