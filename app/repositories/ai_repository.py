from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.db.models import AIConversation, AIMessage, AIUsageLog


def create_conversation(
    db: Session,
    line_user_id: str,
    is_group: bool = False,
    group_id: Optional[str] = None,
    title: Optional[str] = None,
) -> AIConversation:
    """建立新對話"""
    import uuid
    conversation_id = f"conv_{uuid.uuid4().hex[:12]}"

    # 7天後過期
    expires_at = datetime.utcnow() + timedelta(days=7)

    conversation = AIConversation(
        line_user_id=line_user_id,
        conversation_id=conversation_id,
        title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        is_group=is_group,
        group_id=group_id,
        expires_at=expires_at,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: str) -> Optional[AIConversation]:
    """取得對話"""
    return db.query(AIConversation).filter(
        AIConversation.conversation_id == conversation_id
    ).first()


def get_user_conversations(
    db: Session, line_user_id: str, limit: int = 10
) -> List[AIConversation]:
    """取得用戶最近的對話"""
    return db.query(AIConversation).filter(
        AIConversation.line_user_id == line_user_id,
        AIConversation.expires_at > datetime.utcnow()
    ).order_by(desc(AIConversation.last_message_at)).limit(limit).all()


def add_message_to_conversation(
    db: Session,
    conversation_id: str,
    role: str,
    content: str,
    tokens_used: Optional[int] = None,
) -> AIMessage:
    """添加消息到對話"""
    message = AIMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tokens_used=tokens_used,
    )
    db.add(message)

    # 更新對話的消息計數和最後消息時間
    conversation = get_conversation(db, conversation_id)
    if conversation:
        conversation.message_count += 1
        conversation.last_message_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message


def get_conversation_history(
    db: Session,
    conversation_id: str,
    limit: int = 10,
) -> List[AIMessage]:
    """取得對話歷史（用於上下文）"""
    return db.query(AIMessage).filter(
        AIMessage.conversation_id == conversation_id
    ).order_by(AIMessage.created_at).limit(limit).all()


def create_usage_log(
    db: Session,
    line_user_id: str,
    conversation_id: str,
    query: str,
    response: str,
    is_vip: bool = False,
    tokens_input: Optional[int] = None,
    tokens_output: Optional[int] = None,
) -> AIUsageLog:
    """建立使用日誌"""
    log = AIUsageLog(
        line_user_id=line_user_id,
        conversation_id=conversation_id,
        query=query,
        response=response,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        is_vip=is_vip,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_today_conversation_count(
    db: Session, line_user_id: str
) -> int:
    """取得用戶今日對話次數"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    return db.query(AIUsageLog).filter(
        and_(
            AIUsageLog.line_user_id == line_user_id,
            AIUsageLog.created_at >= today_start,
            AIUsageLog.created_at < today_end,
        )
    ).count()


def delete_expired_conversations(db: Session) -> int:
    """刪除過期的對話（和相關消息）"""
    expired = db.query(AIConversation).filter(
        AIConversation.expires_at <= datetime.utcnow()
    ).all()

    count = 0
    for conversation in expired:
        # 刪除相關消息
        db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation.conversation_id
        ).delete()

        # 刪除對話
        db.delete(conversation)
        count += 1

    db.commit()
    return count


def get_ai_usage_stats(db: Session, line_user_id: str, days: int = 7) -> dict:
    """取得用戶 AI 使用統計"""
    start_date = datetime.utcnow() - timedelta(days=days)

    logs = db.query(AIUsageLog).filter(
        and_(
            AIUsageLog.line_user_id == line_user_id,
            AIUsageLog.created_at >= start_date,
        )
    ).all()

    total_queries = len(logs)
    total_responses = len([l for l in logs if l.response])

    return {
        "period_days": days,
        "total_queries": total_queries,
        "total_responses": total_responses,
        "vip_queries": len([l for l in logs if l.is_vip]),
        "free_queries": total_queries - len([l for l in logs if l.is_vip]),
    }
