from datetime import datetime, timedelta
import random
import string

from sqlalchemy.orm import Session

from app.repositories.group_repository import get_group
from app.repositories.vip_repository import (
    add_vip_usage_log,
    consume_vip_quota,
    create_vip_serial,
    get_vip_serial_by_code,
    get_vip_subscription,
    get_today_vip_consumed_chars,
    mark_vip_serial_used,
    upsert_vip_subscription,
)

VIP_SERIAL_PREFIX = "FANVIP"
VIP_SERIAL_TOTAL_LENGTH = 16
VIP_DEFAULT_REMAINING_CHARS = 100000
VIP_CHAR_BONUS_PER_ACTIVATION = 100000


def _build_serial_candidate() -> str:
    suffix_len = VIP_SERIAL_TOTAL_LENGTH - len(VIP_SERIAL_PREFIX)
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=suffix_len))
    return f"{VIP_SERIAL_PREFIX}{suffix}"


def generate_unique_vip_serial(
    db: Session,
    created_by_user_id: str,
    created_by_name: str,
    created_by_member_code: str | None,
):
    while True:
        serial_code = _build_serial_candidate()
        if not get_vip_serial_by_code(db, serial_code):
            return create_vip_serial(
                db=db,
                serial_code=serial_code,
                created_by_user_id=created_by_user_id,
                created_by_name=created_by_name,
                created_by_member_code=created_by_member_code,
                base_days=0,
                extra_days=0,
                total_days=0,
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
    expires_at = now + timedelta(days=3650)  # 字元制方案，時間僅作狀態欄位用途
    remaining_chars = VIP_DEFAULT_REMAINING_CHARS
    if current:
        remaining_chars = max(current.remaining_chars, 0) + VIP_CHAR_BONUS_PER_ACTIVATION

    plan_name = "VIP-AZURE-100K"
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

    is_active = row.remaining_chars > 0
    return {
        "is_active": is_active,
        "owner_user_id": row.line_user_id,
        "started_at": row.started_at,
        "expires_at": row.expires_at,
        "current_plan": row.current_plan,
        "remaining_chars": row.remaining_chars,
    }


def resolve_vip_status_for_context(
    db: Session,
    source_type: str,
    user_id: str | None,
    group_id: str | None,
):
    if source_type == "group" and group_id:
        group = get_group(db, group_id)
        inviter_user_id = group.inviter_user_id if group else None
        if not inviter_user_id:
            return None
        inviter_status = get_vip_status(db, inviter_user_id)
        if not inviter_status:
            return None
        return inviter_status

    if not user_id:
        return None
    return get_vip_status(db, user_id)


def consume_vip_chars(
    db: Session,
    owner_user_id: str,
    source_type: str,
    source_id: str,
    consumed_chars: int,
) -> dict:
    next_subscription = consume_vip_quota(db, owner_user_id, consumed_chars)
    if consumed_chars > 0:
        add_vip_usage_log(db, owner_user_id, source_type, source_id, consumed_chars)

    status = get_vip_status(db, owner_user_id)
    return {
        "subscription": next_subscription,
        "status": status,
    }


def get_today_consumed_chars(db: Session, owner_user_id: str) -> int:
    now = datetime.utcnow()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    return get_today_vip_consumed_chars(db, owner_user_id, day_start, day_end)
