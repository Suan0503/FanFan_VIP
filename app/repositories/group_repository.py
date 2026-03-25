from sqlalchemy.orm import Session  # 匯入 Session

from app.db.models import GroupSetting  # 匯入群組模型


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
