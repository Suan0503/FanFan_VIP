from sqlalchemy.orm import Session  # 匯入 Session

from app.core.languages import DEFAULT_LANGUAGE_CODE  # 匯入預設語言
from app.repositories.group_repository import (
    get_group,
    create_group,
    get_group_languages,
    set_group_languages,
    add_group_language,
    remove_group_language,
    reset_group_languages,
)  # 匯入群組資料存取


def ensure_group_exists(db: Session, group_id: str):
    return get_group(db, group_id) or create_group(db, group_id)  # 確保群組存在


def get_languages(db: Session, group_id: str) -> list[str]:
    return get_group_languages(db, group_id)  # 取得群組語言


def toggle_or_set_languages(db: Session, group_id: str, selected_codes: list[str], toggle_single: bool) -> list[str]:
    if toggle_single and len(selected_codes) == 1:
        code = selected_codes[0]  # 單一語言切換
        current = get_group_languages(db, group_id)  # 目前語言
        if code in current:
            return remove_group_language(db, group_id, code)  # 已存在則移除
        return add_group_language(db, group_id, code)  # 不存在則加入
    return set_group_languages(db, group_id, selected_codes)  # 多語直接覆蓋


def reset_languages(db: Session, group_id: str) -> list[str]:
    return reset_group_languages(db, group_id)  # 重設群組語言


def get_personal_or_default_language(user_language: str | None) -> str:
    return user_language or DEFAULT_LANGUAGE_CODE  # 個人語言或預設語言
