from fastapi import FastAPI, Request, HTTPException  # 匯入 FastAPI 與請求型別

from app.core.config import settings  # 匯入設定
from app.db.session import init_db  # 匯入資料庫初始化
from app.bot.handlers import line_handler  # 匯入 LINE 事件處理器


app = FastAPI(title="FanFan Translator Bot")  # 建立 FastAPI 應用


@app.on_event("startup")
def startup_event() -> None:
    init_db()  # 啟動時建立資料表


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "FanFan Translator"}  # 健康檢查


@app.post("/webhook/line")
async def line_webhook(request: Request) -> dict[str, str]:
    signature = request.headers.get("X-Line-Signature", "")  # 取得簽章
    body = (await request.body()).decode("utf-8")  # 讀取 body
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")  # 缺少簽章
    line_handler.handle(body, signature)  # 交給 LINE SDK 驗證與分派
    return {"message": "ok"}  # 回傳成功


@app.get("/config")
def show_config() -> dict[str, str]:
    return {
        "project": settings.project_name,
        "env": settings.environment,
    }  # 方便確認部署設定
