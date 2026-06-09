from sqlalchemy.orm import Session  # 匯入 Session

from app.repositories.user_repository import count_users, get_user_by_member_code  # 匯入資料操作


def generate_member_code(db: Session) -> str:
    base_number = count_users(db) + 1  # 從目前總數往後編號
    while True:
        code = f"FAN{base_number:03d}"  # 產生 FAN001 格式，超過 999 後自動為 FAN1000
        if not get_user_by_member_code(db, code):
            return code  # 找到未使用編號就回傳
        base_number += 1  # 若碰撞則遞增
