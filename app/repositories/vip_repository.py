from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import VIPSerialCode, VIPSubscription, VIPUsageLog


def get_vip_subscription(db: Session, line_user_id: str) -> VIPSubscription | None:
    return db.query(VIPSubscription).filter(VIPSubscription.line_user_id == line_user_id).one_or_none()


def upsert_vip_subscription(
    db: Session,
    line_user_id: str,
    member_code: str,
    started_at: datetime,
    expires_at: datetime,
    current_plan: str,
    remaining_chars: int,
) -> VIPSubscription:
    row = get_vip_subscription(db, line_user_id)
    if row:
        row.member_code = member_code
        row.started_at = started_at
        row.expires_at = expires_at
        row.current_plan = current_plan
        row.remaining_chars = remaining_chars
        row.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(row)
        return row

    row = VIPSubscription(
        line_user_id=line_user_id,
        member_code=member_code,
        started_at=started_at,
        expires_at=expires_at,
        current_plan=current_plan,
        remaining_chars=remaining_chars,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_vip_serial_by_code(db: Session, serial_code: str) -> VIPSerialCode | None:
    return db.query(VIPSerialCode).filter(VIPSerialCode.serial_code == serial_code).one_or_none()


def create_vip_serial(
    db: Session,
    serial_code: str,
    created_by_user_id: str,
    created_by_name: str,
    created_by_member_code: str | None,
    base_days: int,
    extra_days: int,
    total_days: int,
) -> VIPSerialCode:
    row = VIPSerialCode(
        serial_code=serial_code,
        created_by_user_id=created_by_user_id,
        created_by_name=created_by_name,
        created_by_member_code=created_by_member_code,
        base_days=base_days,
        extra_days=extra_days,
        total_days=total_days,
        is_used=False,
        created_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def mark_vip_serial_used(
    db: Session,
    serial: VIPSerialCode,
    used_by_user_id: str,
    used_by_member_code: str,
) -> VIPSerialCode:
    serial.is_used = True
    serial.used_by_user_id = used_by_user_id
    serial.used_by_member_code = used_by_member_code
    serial.used_at = datetime.utcnow()
    db.commit()
    db.refresh(serial)
    return serial


def consume_vip_quota(db: Session, line_user_id: str, amount: int) -> VIPSubscription | None:
    if amount <= 0:
        return get_vip_subscription(db, line_user_id)

    row = get_vip_subscription(db, line_user_id)
    if not row:
        return None

    row.remaining_chars = max(0, row.remaining_chars - amount)
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return row


def add_vip_usage_log(
    db: Session,
    line_user_id: str,
    source_type: str,
    source_id: str,
    consumed_chars: int,
) -> VIPUsageLog:
    row = VIPUsageLog(
        line_user_id=line_user_id,
        source_type=source_type,
        source_id=source_id,
        consumed_chars=max(consumed_chars, 0),
        created_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_today_vip_consumed_chars(db: Session, line_user_id: str, day_start: datetime, day_end: datetime) -> int:
    value = (
        db.query(func.coalesce(func.sum(VIPUsageLog.consumed_chars), 0))
        .filter(VIPUsageLog.line_user_id == line_user_id)
        .filter(VIPUsageLog.created_at >= day_start)
        .filter(VIPUsageLog.created_at < day_end)
        .scalar()
    )
    return int(value or 0)
