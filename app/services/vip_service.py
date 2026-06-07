from datetime import datetime, timedelta
import random
import string

from sqlalchemy.orm import Session

from app.repositories.vip_repository import (
    create_vip_serial,
    get_vip_serial_by_code,
    get_vip_subscription,
    mark_vip_serial_used,
    upsert_vip_subscription,
)

VIP_SERIAL_PREFIX = "FANVIP"
VIP_SERIAL_TOTAL_LENGTH = 16
VIP_BASE_DAYS = 30
VIP_DEFAULT_REMAINING_CHARS = 300000
VIP_CHAR_BONUS_PER_ACTIVATION = 300000


def _build_serial_candidate() -> str:
    suffix_len = VIP_SERIAL_TOTAL_LENGTH - len(VIP_SERIAL_PREFIX)
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=suffix_len))
    return f"{VIP_SERIAL_PREFIX}{suffix}"


def generate_unique_vip_serial(
    db: Session,
    created_by_user_id: str,
    created_by_name: str,
    created_by_member_code: str | None,
    extra_days: int = 0,
):
    base_days = VIP_BASE_DAYS
    safe_extra_days = max(extra_days, 0)
    total_days = base_days + safe_extra_days

    while True:
        serial_code = _build_serial_candidate()
        if not get_vip_serial_by_code(db, serial_code):
            return create_vip_serial(
                db=db,
                serial_code=serial_code,
                created_by_user_id=created_by_user_id,
                created_by_name=created_by_name,
                created_by_member_code=created_by_member_code,
                base_days=base_days,
                extra_days=safe_extra_days,
                total_days=total_days,
            )


def activate_vip_by_serial(db: Session, line_user_id: str, member_code: str, serial_code: str):
    normalized = (serial_code or "").strip().upper()
    serial = get_vip_serial_by_code(db, normalized)
    if not serial:
        return None, "序號不存在，請重新輸入。"
    if serial.is_used:
        return None, "此序號已被使用。"

    now = datetime.utcnow()
    current = get_vip_subscription(db, line_user_id)
    activation_start = now
    if current and current.expires_at > now:
        activation_start = current.expires_at

    expires_at = activation_start + timedelta(days=serial.total_days)
    remaining_chars = VIP_DEFAULT_REMAINING_CHARS
    if current:
        remaining_chars = max(current.remaining_chars, 0) + VIP_CHAR_BONUS_PER_ACTIVATION

    plan_name = f"VIP-{serial.total_days}D"
    subscription = upsert_vip_subscription(
        db=db,
        line_user_id=line_user_id,
        member_code=member_code,
        started_at=activation_start,
        expires_at=expires_at,
        current_plan=plan_name,
        remaining_chars=remaining_chars,
    )
    mark_vip_serial_used(db, serial, line_user_id, member_code)
    return subscription, "ok"


def get_vip_status(db: Session, line_user_id: str):
    row = get_vip_subscription(db, line_user_id)
    if not row:
        return None

    now = datetime.utcnow()
    is_active = row.expires_at > now
    return {
        "is_active": is_active,
        "started_at": row.started_at,
        "expires_at": row.expires_at,
        "current_plan": row.current_plan,
        "remaining_chars": row.remaining_chars,
    }
