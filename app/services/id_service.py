from sqlalchemy.orm import Session  # 匯入 Session

from app.repositories.user_repository import count_users, get_user_by_member_code  # 匯入資料操作


def generate_member_code(db: Session) -> str:
    base_number = count_users(db) + 1  # 從目前總數往後編號
    while True:
        code = f"FAN{base_number:06d}"  # 產生 FAN000001 格式
        if not get_user_by_member_code(db, code):
            return code  # 找到未使用編號就回傳
        base_number += 1  # 若碰撞則遞增
