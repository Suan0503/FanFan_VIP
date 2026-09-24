#!/usr/bin/env python3
"""
FanFan VIP - Google Gemini AI 集成測試腳本
用於驗證 Gemini API、數據庫和服務是否正常運作
"""

import sys
from pathlib import Path

# 添加項目目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """測試 1：檢查所有必要模塊是否已安裝"""
    print("\n🧪 測試 1: 檢查模塊導入...")

    try:
        import google.generativeai as genai
        print("  ✅ google-generativeai 已安裝")
    except ImportError as e:
        print(f"  ❌ google-generativeai 缺失: {e}")
        print("     請運行: pip install google-generativeai")
        return False

    try:
        from app.core.config import settings
        print("  ✅ 配置模塊已加載")
    except ImportError as e:
        print(f"  ❌ 配置模塊缺失: {e}")
        return False

    try:
        from app.services.ai_service import ai_service
        print("  ✅ AI 服務已加載")
    except ImportError as e:
        print(f"  ❌ AI 服務缺失: {e}")
        return False

    return True


def test_config():
    """測試 2：檢查環境變量配置"""
    print("\n🧪 測試 2: 檢查環境變量...")

    from app.core.config import settings

    checks = [
        ("GEMINI_API_KEY", settings.gemini_api_key),
        ("GEMINI_MODEL", settings.gemini_model),
        ("AI_FREE_DAILY_LIMIT", settings.ai_free_daily_limit),
        ("AI_VIP_DAILY_LIMIT", settings.ai_vip_daily_limit),
    ]

    all_ok = True
    for key, value in checks:
        if value:
            print(f"  ✅ {key} = {str(value)[:30]}{'...' if len(str(value)) > 30 else ''}")
        else:
            print(f"  ❌ {key} 未設置")
            all_ok = False

    if not all_ok:
        print("\n  💡 請在 .env 文件中配置缺失的環境變量")

    return all_ok


def test_gemini_api():
    """測試 3：驗證 Gemini API 連接"""
    print("\n🧪 測試 3: 驗證 Gemini API 連接...")

    from app.core.config import settings

    if not settings.gemini_api_key:
        print("  ❌ GEMINI_API_KEY 未設置，跳過 API 測試")
        return False

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)

        model = genai.GenerativeModel(settings.gemini_model)
        response = model.generate_content("Say 'Hello, FanFan!'", stream=False)

        if response.text:
            print(f"  ✅ API 連接成功")
            print(f"     模型: {settings.gemini_model}")
            print(f"     回應: {response.text[:100]}...")
            return True
        else:
            print(f"  ❌ API 返回空回應")
            return False

    except Exception as e:
        print(f"  ❌ API 連接失敗: {e}")
        print("     檢查項:")
        print("     1. GEMINI_API_KEY 是否正確")
        print("     2. 網路連接是否正常")
        print("     3. API 配額是否超限")
        return False


def test_database():
    """測試 4：檢查數據庫連接和表"""
    print("\n🧪 測試 4: 檢查數據庫...")

    try:
        from app.db.session import SessionLocal, init_db
        from app.db.models import AIConversation, AIMessage, AIUsageLog

        # 初始化數據庫表
        init_db()
        print("  ✅ 數據庫初始化成功")

        # 測試連接
        db = SessionLocal()

        # 檢查表
        tables = [
            (AIConversation, "ai_conversations"),
            (AIMessage, "ai_messages"),
            (AIUsageLog, "ai_usage_logs"),
        ]

        for model_class, table_name in tables:
            try:
                count = db.query(model_class).count()
                print(f"  ✅ {table_name} 表存在 ({count} 條紀錄)")
            except Exception as e:
                print(f"  ❌ {table_name} 表錯誤: {e}")
                return False

        db.close()
        return True

    except Exception as e:
        print(f"  ❌ 數據庫錯誤: {e}")
        return False


def test_ai_service():
    """測試 5：測試 AI 服務功能"""
    print("\n🧪 測試 5: 測試 AI 服務...")

    try:
        from app.services.ai_service import ai_service
        from app.db.session import SessionLocal

        if not ai_service:
            print("  ❌ AI 服務未初始化")
            return False

        # 測試對話創建
        test_user_id = "U_test_user_" + str(hash("test"))

        db = SessionLocal()
        conversation = ai_service.start_conversation(test_user_id)
        print(f"  ✅ 創建對話成功: {conversation}")

        # 測試日限檢查
        exceeded, used, limit = ai_service.check_daily_limit(test_user_id, is_vip=False)
        print(f"  ✅ 日限檢查成功: {used}/{limit}")

        # 測試聊天
        if ai_service.model:
            response, conv_id, stats = ai_service.chat(
                user_id=test_user_id,
                query="Hello, Gemini!",
                conversation_id=conversation,
                is_vip=False,
                language="en"
            )
            print(f"  ✅ AI 對話成功")
            print(f"     回應: {response[:100]}...")

        db.close()
        return True

    except Exception as e:
        print(f"  ❌ AI 服務測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_handlers():
    """測試 6：檢查 LINE 指令處理器"""
    print("\n🧪 測試 6: 檢查指令處理器...")

    try:
        from app.bot.handlers_ai import (
            handle_ai_menu_command,
            handle_ai_start_command,
            handle_ai_chat,
            handle_ai_history_command,
            handle_ai_stats_command,
        )
        print("  ✅ 所有 AI 指令處理器已加載")

        from app.bot.handlers import (
            AI菜單指令,
            AI開始對話指令,
            AI返回翻譯指令,
        )
        print(f"  ✅ AI 菜單指令: {AI菜單指令}")
        print(f"  ✅ AI 開始指令: {AI開始對話指令}")
        print(f"  ✅ AI 返回指令: {AI返回翻譯指令}")

        return True

    except Exception as e:
        print(f"  ❌ 指令處理器檢查失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """運行所有測試"""
    print("=" * 60)
    print("🤖 FanFan VIP - Google Gemini AI 集成測試")
    print("=" * 60)

    results = []

    # 運行測試
    results.append(("模塊導入", test_imports()))

    if results[-1][1]:  # 只有模塊導入成功才繼續
        results.append(("環境變量", test_config()))
        results.append(("Gemini API", test_gemini_api()))
        results.append(("數據庫", test_database()))
        results.append(("AI 服務", test_ai_service()))
        results.append(("指令處理", test_handlers()))

    # 顯示總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print("=" * 60)
    print(f"總計: {passed} 通過, {failed} 失敗")

    if failed == 0:
        print("\n🎉 所有測試都通過了！")
        print("✅ Gemini AI 已準備好使用")
        print("\n💡 接下來:")
        print("   1. 啟動應用: uvicorn app.main:app --reload")
        print("   2. 向 LINE bot 發送: /ai")
        print("   3. 開始 AI 對話: /ai開始")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 個測試失敗")
        print("   請檢查上面的錯誤信息並修正")
        return 1


if __name__ == "__main__":
    sys.exit(main())
