from flask import Flask, request, jsonify
import os
import json
import random
import string
import re
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
if not DATABASE_URL:
    os.makedirs(app.instance_path, exist_ok=True)
    DATABASE_URL = f"sqlite:///{os.path.join(app.instance_path, 'fanfan_vip.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64))
    status = db.Column(db.String(16), default='inactive')
    expire_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LicenseCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    days = db.Column(db.Integer, default=30)
    used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def generate_code():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"FANVIP{suffix}"


# Master user helpers
MASTER_USER_FILE = "master_user_ids.json"

def load_master_users():
    if os.path.exists(MASTER_USER_FILE):
        try:
            with open(MASTER_USER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data)
        except Exception:
            return set()
    return set()

MASTER_USER_IDS = load_master_users()


# LINE client
LINE_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', '') or os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
if not LINE_TOKEN:
    print('⚠️ WARNING: CHANNEL_ACCESS_TOKEN not set, bot will not reply to messages')

line_bot_api = None
if LINE_TOKEN:
    line_bot_api = LineBotApi(LINE_TOKEN)


def build_main_menu():
    return (
        "【FANVIP 會員中心】\n"
        "請輸入以下任一指令：\n"
        "1. /主選單：顯示這份指令清單\n"
        "2. /我的會員：查看會員狀態與到期時間\n"
        "3. /兌換序號 FANVIPXXXXXXXXXX：啟用或續期\n"
        "4. 直接貼上序號也可以兌換"
    )


def build_member_info(user_id):
    member = db.session.query(Member).filter_by(line_user_id=user_id).first()
    if not member:
        return "目前尚未啟用會員。\n請使用 /兌換序號 FANVIPXXXXXXXXXX 進行啟用。"

    now = datetime.utcnow()
    status_text = "有效" if member.status == 'active' and member.expire_at and member.expire_at > now else "未啟用"
    expire_text = member.expire_at.strftime("%Y-%m-%d %H:%M:%S") if member.expire_at else "尚未設定"
    return (
        "【會員資料】\n"
        f"狀態：{status_text}\n"
        f"到期時間：{expire_text}\n"
        "需要續期請輸入：/兌換序號 FANVIPXXXXXXXXXX"
    )


def parse_days(value):
    digits = re.sub(r'[^0-9]', '', value or '')
    if not digits:
        return 30
    return int(digits)


def check_member_expiry():
    now = datetime.utcnow()
    expired = db.session.query(Member).filter(Member.expire_at != None, Member.expire_at < now, Member.status == 'active').all()
    count = 0
    for m in expired:
        m.status = 'inactive'
        count += 1
    if count:
        db.session.commit()
    return count


@app.route('/admin/generate_codes', methods=['POST'])
def admin_generate_codes():
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '')
    token = request.headers.get('X-Admin-Token', '')
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        return jsonify({'error': 'unauthorized'}), 401
    body = request.get_json() or {}
    try:
        count = int(body.get('count', 1))
        days = int(body.get('days', 30))
    except Exception:
        return jsonify({'error': 'invalid request'}), 400
    if count < 1 or count > 500:
        return jsonify({'error': 'count out of range (1-500)'}), 400
    codes = []
    for _ in range(count):
        for _ in range(5):
            c = generate_code()
            if not db.session.query(LicenseCode).filter_by(code=c).first():
                lc = LicenseCode()
                lc.code = c
                lc.days = days
                db.session.add(lc)
                db.session.commit()
                codes.append(c)
                break
    return jsonify({'codes': codes, 'days': days}), 200


@app.route('/admin/codes', methods=['GET'])
def admin_list_codes():
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '')
    token = request.headers.get('X-Admin-Token', '')
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        return jsonify({'error': 'unauthorized'}), 401
    limit = int(request.args.get('limit', 500))
    q = db.session.query(LicenseCode).order_by(LicenseCode.created_at.desc()).limit(limit).all()
    out = []
    for lc in q:
        out.append({'code': lc.code, 'days': lc.days, 'used': bool(lc.used), 'used_by': lc.used_by, 'used_at': lc.used_at.isoformat() if lc.used_at else None, 'created_at': lc.created_at.isoformat()})
    return jsonify({'codes': out}), 200


@app.route('/admin/export_codes', methods=['GET'])
def admin_export_codes():
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '')
    token = request.headers.get('X-Admin-Token', '')
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        return 'unauthorized', 401
    limit = int(request.args.get('limit', 10000))
    q = db.session.query(LicenseCode).order_by(LicenseCode.created_at.desc()).limit(limit).all()
    rows = ['code,days,used,used_by,used_at,created_at']
    for lc in q:
        rows.append(','.join([lc.code, str(lc.days), str(int(bool(lc.used))), str(lc.used_by) if lc.used_by else '', lc.used_at.isoformat() if lc.used_at else '', lc.created_at.isoformat()]))
    return '\n'.join(rows), 200, {'Content-Type': 'text/csv; charset=utf-8'}


@app.route('/admin/run_expiry_check', methods=['POST'])
def admin_run_expiry_check():
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '')
    token = request.headers.get('X-Admin-Token', '')
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        return jsonify({'error': 'unauthorized'}), 401
    count = check_member_expiry()
    return jsonify({'expired_count': count}), 200


CODE_RE = re.compile(r'^(FANVIP[A-Z0-9]{10})$', re.I)


@app.route('/', methods=['GET'])
def index():
    return 'FANVIP 服務正常運作', 200


# support both /callback and /webhook for backward compatibility
@app.route('/webhook', methods=['POST'])
def webhook():
    # simply forward to callback logic
    return callback()

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    try:
        data = json.loads(body)
    except Exception:
        return 'ok', 200

    events = data.get('events', [])
    for ev in events:
        t = ev.get('type')
        if t == 'follow':
            reply_token = ev.get('replyToken')
            text = "感謝加入 FANVIP！\n請輸入 /主選單 查看可用功能。"
            if line_bot_api and reply_token:
                try:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
                except Exception:
                    pass
        elif t == 'message' and ev.get('message', {}).get('type') == 'text':
            text = ev['message']['text'].strip()
            reply_token = ev.get('replyToken')
            user_id = ev.get('source', {}).get('userId')
            normalized = text.lower()

            if normalized in {'/主選單', '主選單', '/會員中心', '會員中心', '/說明', '說明', '/help', 'help', '1'}:
                msg = build_main_menu()
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            if normalized in {'/我的會員', '我的會員', '/會員資料', '會員資料', '/我的資訊', '我的資訊', '2'}:
                msg = build_member_info(user_id)
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            if user_id in MASTER_USER_IDS and (text.startswith('/序號') or text.startswith('/產生序號')):
                parts = text.split()
                try:
                    if len(parts) == 2:
                        count = int(parts[1])
                        days = 30
                    elif len(parts) >= 3:
                        count = int(parts[1])
                        days = parse_days(parts[2])
                    else:
                        raise ValueError()
                except Exception:
                    msg = '格式錯誤。範例：/產生序號 5 30天'
                    if line_bot_api and reply_token:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                    continue
                codes = []
                for _ in range(count):
                    for _ in range(5):
                        c = generate_code()
                        if not db.session.query(LicenseCode).filter_by(code=c).first():
                            lc = LicenseCode()
                            lc.code = c
                            lc.days = days
                            db.session.add(lc)
                            db.session.commit()
                            codes.append(c)
                            break
                msg = '已建立啟用序號：\n' + '\n'.join(codes)
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            redeem_code = None
            if text.startswith('/兌換序號'):
                parts = text.split(maxsplit=1)
                if len(parts) == 2:
                    redeem_code = parts[1].strip().upper()
            elif CODE_RE.match(text):
                redeem_code = text.upper()

            if redeem_code:
                m = CODE_RE.match(redeem_code)
                if not m:
                    msg = '序號格式不正確，請輸入：/兌換序號 FANVIPXXXXXXXXXX'
                    if line_bot_api and reply_token:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                    continue
                code = m.group(1).upper()
                lc = db.session.query(LicenseCode).filter_by(code=code).first()
                if not lc:
                    msg = '查無此序號，請確認後再試。'
                elif lc.used:
                    msg = '這組序號已使用過。'
                else:
                    member = db.session.query(Member).filter_by(line_user_id=user_id).first()
                    if not member:
                        member = Member()
                        member.line_user_id = user_id
                        member.status = 'active'
                        member.expire_at = datetime.utcnow() + timedelta(days=lc.days)
                        db.session.add(member)
                        db.session.flush()
                    else:
                        if member.expire_at and member.expire_at > datetime.utcnow():
                            member.expire_at = member.expire_at + timedelta(days=lc.days)
                        else:
                            member.expire_at = datetime.utcnow() + timedelta(days=lc.days)
                        member.status = 'active'
                    lc.used = True
                    lc.used_by = member.id
                    lc.used_at = datetime.utcnow()
                    db.session.commit()
                    msg = f'兌換成功！已延長 {lc.days} 天。\n到期時間：{member.expire_at.strftime("%Y-%m-%d %H:%M:%S")}'
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            if line_bot_api and reply_token:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text='看不懂這個指令。\n請輸入 /主選單 查看完整功能。')
                )

    return 'OK', 200


if __name__ == '__main__':
    try:
        with app.app_context():
            check_member_expiry()
    except Exception:
        pass
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))