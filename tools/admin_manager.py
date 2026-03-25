import argparse  # 匯入命令列參數工具
import sys  # 匯入系統模組
from pathlib import Path  # 匯入路徑工具

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # 取得專案根目錄
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))  # 將專案根目錄加入模組搜尋路徑

from app.core.languages import DEFAULT_LANGUAGE_CODE  # 匯入預設語言
from app.db.session import SessionLocal, init_db  # 匯入資料庫工具
from app.repositories.user_repository import (  # 匯入使用者資料操作
    create_user,
    get_user_by_line_id,
    get_user_by_member_code,
    list_admin_users,
    update_user_admin_flag,
)
from app.services.id_service import generate_member_code  # 匯入編號產生器


def _find_user(line_user_id: str | None, member_code: str | None):
    with SessionLocal() as db:
        if line_user_id:
            return get_user_by_line_id(db, line_user_id)  # 依 LINE ID 查詢
        if member_code:
            return get_user_by_member_code(db, member_code)  # 依 FAN 編號查詢
    return None  # 無條件時回傳 None


def _resolve_or_create_user(line_user_id: str | None, member_code: str | None, auto_create: bool):
    with SessionLocal() as db:
        user = None  # 初始化 user
        if line_user_id:
            user = get_user_by_line_id(db, line_user_id)  # 先用 LINE ID 查詢
            if not user and auto_create:
                new_member_code = generate_member_code(db)  # 產生新編號
                user = create_user(db, line_user_id, new_member_code, DEFAULT_LANGUAGE_CODE)  # 自動建使用者
        elif member_code:
            user = get_user_by_member_code(db, member_code)  # 用 FAN 編號查詢
        return user  # 回傳查詢結果


def promote_or_demote(line_user_id: str | None, member_code: str | None, is_admin: bool, auto_create: bool) -> int:
    user = _resolve_or_create_user(line_user_id, member_code, auto_create)  # 取得或建立使用者
    if not user:
        print("找不到使用者，請確認 LINE User ID 或 FAN 編號。")  # 提示找不到
        return 1  # 回傳失敗

    with SessionLocal() as db:
        db_user = get_user_by_line_id(db, user.line_user_id)  # 重新讀取資料
        if not db_user:
            print("找不到使用者，請稍後重試。")  # 防禦性處理
            return 1  # 回傳失敗
        updated = update_user_admin_flag(db, db_user, is_admin)  # 更新管理員旗標

    status = "管理員" if updated.is_admin else "一般使用者"  # 決定狀態文字
    print(f"更新完成：{updated.member_code} ({updated.line_user_id}) -> {status}")  # 輸出結果
    return 0  # 回傳成功


def list_admins() -> int:
    with SessionLocal() as db:
        admins = list_admin_users(db)  # 取得管理員列表
    if not admins:
        print("目前沒有管理員。")  # 無管理員提示
        return 0  # 正常結束

    print("目前管理員清單：")  # 顯示標題
    for user in admins:
        print(f"- {user.member_code} | {user.line_user_id}")  # 逐筆輸出
    return 0  # 正常結束


def show_user(line_user_id: str | None, member_code: str | None) -> int:
    user = _find_user(line_user_id, member_code)  # 查詢使用者
    if not user:
        print("找不到使用者。")  # 無資料提示
        return 1  # 回傳失敗

    role = "管理員" if user.is_admin else "一般使用者"  # 角色文字
    print(f"{user.member_code} | {user.line_user_id} | {role} | 語言:{user.target_language}")  # 顯示資料
    return 0  # 回傳成功


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FanFan 管理員初始化工具")  # 建立 parser
    sub = parser.add_subparsers(dest="command", required=True)  # 建立子命令

    promote_parser = sub.add_parser("升級管理員", aliases=["promote"], help="設定為管理員")  # 升權命令
    promote_parser.add_argument("--使用者ID", "--line-user-id", dest="line_user_id", help="LINE User ID")  # LINE ID 參數
    promote_parser.add_argument("--編號", "--member-code", dest="member_code", help="FAN 編號，例如 FAN000001")  # FAN 編號參數
    promote_parser.add_argument("--自動建立", "--auto-create", dest="auto_create", action="store_true", help="若 LINE ID 不存在則自動建立")  # 自動建立

    demote_parser = sub.add_parser("取消管理員", aliases=["demote"], help="取消管理員")  # 降權命令
    demote_parser.add_argument("--使用者ID", "--line-user-id", dest="line_user_id", help="LINE User ID")  # LINE ID 參數
    demote_parser.add_argument("--編號", "--member-code", dest="member_code", help="FAN 編號，例如 FAN000001")  # FAN 編號參數

    show_parser = sub.add_parser("查詢使用者", aliases=["show"], help="查看使用者資料")  # 查詢命令
    show_parser.add_argument("--使用者ID", "--line-user-id", dest="line_user_id", help="LINE User ID")  # LINE ID 參數
    show_parser.add_argument("--編號", "--member-code", dest="member_code", help="FAN 編號，例如 FAN000001")  # FAN 編號參數

    sub.add_parser("列出管理員", aliases=["list-admins"], help="列出所有管理員")  # 列表命令
    return parser  # 回傳 parser


def validate_identifier(args: argparse.Namespace) -> bool:
    if args.command in {"列出管理員", "list-admins"}:
        return True  # 列表不需要指定對象
    if args.line_user_id or args.member_code:
        return True  # 有任何一個識別值即可
    print("請至少提供 --line-user-id 或 --member-code")  # 顯示參數錯誤
    return False  # 驗證失敗


def main() -> int:
    init_db()  # 確保資料表已建立
    parser = build_parser()  # 建立 parser
    args = parser.parse_args()  # 解析參數

    if not validate_identifier(args):
        return 1  # 參數不足

    if args.command in {"升級管理員", "promote"}:
        return promote_or_demote(args.line_user_id, args.member_code, True, args.auto_create)  # 升權處理
    if args.command in {"取消管理員", "demote"}:
        return promote_or_demote(args.line_user_id, args.member_code, False, False)  # 降權處理
    if args.command in {"查詢使用者", "show"}:
        return show_user(args.line_user_id, args.member_code)  # 查詢處理
    if args.command in {"列出管理員", "list-admins"}:
        return list_admins()  # 列表處理

    print("不支援的命令")  # 防禦性分支
    return 1  # 回傳失敗


if __name__ == "__main__":
    raise SystemExit(main())  # 以退出碼結束
