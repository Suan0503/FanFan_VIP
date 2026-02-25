from flask import Flask, request, jsonify
import os
import json
import random
import string
import re
import time
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database setup (optional)
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

db = None
if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)


if db:
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


def check_member_expiry():
    if not db:
        return 0
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
    if not db:
        return jsonify({'error': 'database not configured'}), 500
    for _ in range(count):
        for _ in range(5):
            c = generate_code()
            if not db.session.query(LicenseCode).filter_by(code=c).first():
                lc = LicenseCode(code=c, days=days)
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
    if not db:
        return jsonify({'error': 'database not configured'}), 500
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
    if not db:
        return 'database not configured', 500
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


# support both /callback and /webhook for backward compatibility
@app.route('/webhook', methods=['POST'])
def webhook():
    # simply forward to callback logic
    return callback()

@app.route('/callback', methods=['POST'])
def callback():
    # Basic LINE webhook handler: parse events and handle follow/text
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
            text = '感謝加入 FANVIP！請輸入「1」開啟會員中心，或貼上序號進行啟用。'
            if line_bot_api and reply_token:
                try:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
                except Exception:
                    pass
        elif t == 'message' and ev.get('message', {}).get('type') == 'text':
            text = ev['message']['text'].strip()
            reply_token = ev.get('replyToken')
            user_id = ev.get('source', {}).get('userId')

            # 管理員快速生成序號：/序號 5 30天  (只限 master users)
            if user_id in MASTER_USER_IDS and text.startswith('/序號'):
                parts = text.split()
                try:
                    if len(parts) == 2:
                        count = int(parts[1])
                        days = 30
                    elif len(parts) >= 3:
                        count = int(parts[1])
                        days = int(re.sub(r'[^0-9]', '', parts[2]))
                    else:
                        raise ValueError()
                except Exception:
                    msg = '格式錯誤。範例：/序號 5 30天'
                    if line_bot_api and reply_token:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                    continue
                # generate locally
                if not db:
                    if line_bot_api and reply_token:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text='伺服器未啟用資料庫，無法生產序號。'))
                    continue
                codes = []
                for _ in range(count):
                    for _ in range(5):
                        c = generate_code()
                        if not db.session.query(LicenseCode).filter_by(code=c).first():
                            lc = LicenseCode(code=c, days=days)
                            db.session.add(lc)
                            db.session.commit()
                            codes.append(c)
                            break
                msg = '已產生序號：\n' + '\n'.join(codes)
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            # 序號兌換
            m = CODE_RE.match(text)
            if m and db:
                code = m.group(1).upper()
                lc = db.session.query(LicenseCode).filter_by(code=code).first()
                if not lc:
                    msg = '序號不存在或已使用。'
                elif lc.used:
                    msg = f'序號已被使用。'
                else:
                    # find or create member
                    member = db.session.query(Member).filter_by(line_user_id=user_id).first()
                    if not member:
                        member = Member(line_user_id=user_id, status='active', expire_at=datetime.utcnow() + timedelta(days=lc.days))
                        db.session.add(member)
                    else:
                        # extend expiry if already active
                        if member.expire_at and member.expire_at > datetime.utcnow():
                            member.expire_at = member.expire_at + timedelta(days=lc.days)
                        else:
                            member.expire_at = datetime.utcnow() + timedelta(days=lc.days)
                        member.status = 'active'
                    lc.used = True
                    lc.used_by = member.id
                    lc.used_at = datetime.utcnow()
                    db.session.commit()
                    msg = f'兌換成功！已為您延長 {lc.days} 天，會員有效期到 {member.expire_at.strftime("%Y-%m-%d %H:%M:%S")}。'
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            # 簡單選單處理
            if text in ['1', '會員中心']:
                msg = '會員中心：\n1) 查看資訊\n2) 啟用/續期（貼上序號）\n3) 支援'
                if line_bot_api and reply_token:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
                continue

            # 未知文字回覆
            if line_bot_api and reply_token:
                line_bot_api.reply_message(reply_token, TextSendMessage(text='指令不明，請輸入「1」查看會員中心或貼上序號進行啟用。'))

    return 'OK', 200


if __name__ == '__main__':
    # 在啟動時檢查到期
    try:
        if db:
            with app.app_context():
                check_member_expiry()
    except Exception:
        pass
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))