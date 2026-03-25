from sqlalchemy.orm import Session  # 匯入 Session

from app.db.models import GroupSetting, GroupLanguageSelection  # 匯入群組模型
from app.core.languages import DEFAULT_LANGUAGE_CODE  # 匯入預設語言


def get_group(db: Session, line_group_id: str) -> GroupSetting | None:
    return db.query(GroupSetting).filter(GroupSetting.line_group_id == line_group_id).one_or_none()  # 讀取群組設定


def create_group(db: Session, line_group_id: str) -> GroupSetting:
    group = GroupSetting(line_group_id=line_group_id)  # 建立群組設定
    db.add(group)  # 新增
    db.commit()  # 提交
    db.refresh(group)  # 重新讀取
    return group  # 回傳


def update_group_language(db: Session, group: GroupSetting, target_language: str) -> GroupSetting:
    group.target_language = target_language  # 更新群組語言
    db.commit()  # 提交
    db.refresh(group)  # 重新讀取
    return group  # 回傳


def bind_group_inviter(db: Session, group: GroupSetting, inviter_user_id: str) -> GroupSetting:
    if not group.inviter_user_id:
        group.inviter_user_id = inviter_user_id  # 首次綁定邀請者代表
        db.commit()  # 提交
        db.refresh(group)  # 重新讀取
    return group  # 回傳


def set_group_inviter(db: Session, group: GroupSetting, inviter_user_id: str) -> GroupSetting:
    group.inviter_user_id = inviter_user_id  # 直接覆寫邀請者代表
    db.commit()  # 提交
    db.refresh(group)  # 重新讀取
    return group  # 回傳


def get_group_languages(db: Session, line_group_id: str) -> list[str]:
    rows = (
        db.query(GroupLanguageSelection)
        .filter(GroupLanguageSelection.line_group_id == line_group_id)
        .order_by(GroupLanguageSelection.id.asc())
        .all()
    )  # 讀取群組多語設定
    if rows:
        return [row.language_code for row in rows]  # 回傳多語清單

    group = get_group(db, line_group_id)  # 退回舊欄位
    if group and group.target_language:
        return [group.target_language]  # 沒有多語資料時沿用舊欄位
    return [DEFAULT_LANGUAGE_CODE]  # 最終回退預設語言


def set_group_languages(db: Session, line_group_id: str, language_codes: list[str]) -> list[str]:
    unique_codes: list[str] = []  # 去重後語言
    for code in language_codes:
        if code not in unique_codes:
            unique_codes.append(code)  # 保留原順序去重

    final_codes = unique_codes if unique_codes else [DEFAULT_LANGUAGE_CODE]  # 至少保留一個語言
    db.query(GroupLanguageSelection).filter(GroupLanguageSelection.line_group_id == line_group_id).delete()  # 清掉舊多語
    for code in final_codes:
        db.add(GroupLanguageSelection(line_group_id=line_group_id, language_code=code))  # 逐筆寫入

    group = get_group(db, line_group_id) or create_group(db, line_group_id)  # 取得群組資料
    group.target_language = final_codes[0]  # 維持舊欄位相容
    db.commit()  # 提交變更
    return final_codes  # 回傳更新後清單


def add_group_language(db: Session, line_group_id: str, language_code: str) -> list[str]:
    current = get_group_languages(db, line_group_id)  # 讀取目前設定
    if language_code not in current:
        current.append(language_code)  # 新增語言
    return set_group_languages(db, line_group_id, current)  # 寫回設定


def remove_group_language(db: Session, line_group_id: str, language_code: str) -> list[str]:
    current = get_group_languages(db, line_group_id)  # 讀取目前設定
    next_codes = [code for code in current if code != language_code]  # 移除指定語言
    return set_group_languages(db, line_group_id, next_codes)  # 寫回設定


def reset_group_languages(db: Session, line_group_id: str) -> list[str]:
    return set_group_languages(db, line_group_id, [DEFAULT_LANGUAGE_CODE])  # 重設成預設語言
