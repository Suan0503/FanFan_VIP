from sqlalchemy.orm import Session  # 匯入 Session

from app.db.models import UserProfile  # 匯入使用者模型


def get_user_by_line_id(db: Session, line_user_id: str) -> UserProfile | None:
    return db.query(UserProfile).filter(UserProfile.line_user_id == line_user_id).one_or_none()  # 查詢使用者


def get_user_by_member_code(db: Session, member_code: str) -> UserProfile | None:
    return db.query(UserProfile).filter(UserProfile.member_code == member_code).one_or_none()  # 查詢編號


def list_admin_users(db: Session) -> list[UserProfile]:
    return db.query(UserProfile).filter(UserProfile.is_admin.is_(True)).order_by(UserProfile.id.asc()).all()  # 查詢所有管理員


def count_users(db: Session) -> int:
    return db.query(UserProfile).count()  # 計算使用者數量


def create_user(db: Session, line_user_id: str, member_code: str, target_language: str) -> UserProfile:
    user = UserProfile(line_user_id=line_user_id, member_code=member_code, target_language=target_language)  # 建立物件
    db.add(user)  # 新增到 Session
    db.commit()  # 提交
    db.refresh(user)  # 重新讀取
    return user  # 回傳使用者


def update_user_language(db: Session, user: UserProfile, target_language: str) -> UserProfile:
    user.target_language = target_language  # 更新語言
    db.commit()  # 提交
    db.refresh(user)  # 重新讀取
    return user  # 回傳更新後資料


def update_user_admin_flag(db: Session, user: UserProfile, is_admin: bool) -> UserProfile:
    user.is_admin = is_admin  # 更新管理員旗標
    db.commit()  # 提交
    db.refresh(user)  # 重新讀取
    return user  # 回傳更新後資料
