from app.core.config import settings  # 匯入設定
from app.db.models import UserProfile, GroupSetting  # 匯入模型


def is_owner(user_id: str | None) -> bool:
    if not user_id:
        return False  # 無使用者 ID 不可能是所有者
    return user_id in settings.owner_user_ids  # 判斷是否為所有者


def can_manage_group(group: GroupSetting, user: UserProfile | None, user_id: str | None) -> bool:
    if is_owner(user_id):
        return True  # 所有者可管理
    if user and user.is_admin:
        return True  # 全域管理員可管理
    if group.inviter_user_id and user_id and group.inviter_user_id == user_id:
        return True  # 群組邀請者代表可管理
    return False  # 其他人不可管理
