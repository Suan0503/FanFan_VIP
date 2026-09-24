def build_ai_menu_card(user_locale: str = "zh-TW") -> dict:
    """
    構建 AI 助手菜單卡片
    """
    if user_locale == "zh-TW":
        return {
            "type": "flex",
            "altText": "🤖 AI 助手",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "heading",
                            "text": "🤖 AI 智慧助手",
                            "level": 2,
                            "weight": "bold",
                            "color": "#667BC6",
                            "margin": "none"
                        },
                        {
                            "type": "text",
                            "text": "由 Google Gemini 提供支援",
                            "size": "xs",
                            "color": "#999999"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✨ 功能",
                                    "weight": "bold",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "• 智慧回答問題\n• 知識檢索\n• 文稿撰寫\n• 多語言對話",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📊 每日額度",
                                    "weight": "bold",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "免費版: 10次/日\nVIP版: 無限次",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🚀 開始對話",
                                "text": "/ai開始"
                            },
                            "style": "primary",
                            "color": "#667BC6"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📋 查看對話歷史",
                                "text": "/ai歷史"
                            },
                            "style": "secondary"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📊 使用統計",
                                "text": "/ai統計"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            }
        }
    else:
        return {
            "type": "flex",
            "altText": "🤖 AI Assistant",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "heading",
                            "text": "🤖 AI Assistant",
                            "level": 2,
                            "weight": "bold",
                            "color": "#667BC6",
                            "margin": "none"
                        },
                        {
                            "type": "text",
                            "text": "Powered by Google Gemini",
                            "size": "xs",
                            "color": "#999999"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✨ Features",
                                    "weight": "bold",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "• Smart Q&A\n• Knowledge Search\n• Writing Assistance\n• Multi-language Support",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📊 Daily Quota",
                                    "weight": "bold",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "Free: 10/day\nVIP: Unlimited",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🚀 Start Chat",
                                "text": "/ai start"
                            },
                            "style": "primary",
                            "color": "#667BC6"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📋 Chat History",
                                "text": "/ai history"
                            },
                            "style": "secondary"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📊 Stats",
                                "text": "/ai stats"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            }
        }


def build_ai_conversation_card(
    conversation_id: str,
    query: str,
    response: str,
    daily_used: int,
    daily_limit: int,
    user_locale: str = "zh-TW"
) -> dict:
    """
    構建 AI 對話結果卡片
    """
    if user_locale == "zh-TW":
        return {
            "type": "flex",
            "altText": "💬 AI 回應",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "heading",
                            "text": "💬 AI 回應",
                            "level": 2,
                            "weight": "bold",
                            "color": "#667BC6"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "padding": "md",
                            "backgroundColor": "#F5F5F5",
                            "cornerRadius": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "你的提問：",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#999999"
                                },
                                {
                                    "type": "text",
                                    "text": query[:200] + ("..." if len(query) > 200 else ""),
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "padding": "md",
                            "backgroundColor": "#E8F0FE",
                            "cornerRadius": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🤖 AI 回答：",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#667BC6"
                                },
                                {
                                    "type": "text",
                                    "text": response[:300] + ("..." if len(response) > 300 else ""),
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"今日使用: {daily_used}/{daily_limit}",
                                    "size": "xs",
                                    "color": "#999999",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "🔋" if daily_used < daily_limit else "⚠️ 已達上限",
                                    "size": "xs",
                                    "color": "#667BC6" if daily_used < daily_limit else "#FF6B6B"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "💭 繼續對話",
                                "text": "/ai繼續對話"
                            },
                            "style": "primary",
                            "color": "#667BC6"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🆕 新建對話",
                                "text": "/ai開始"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            }
        }
    else:
        return {
            "type": "flex",
            "altText": "💬 AI Response",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "heading",
                            "text": "💬 AI Response",
                            "level": 2,
                            "weight": "bold",
                            "color": "#667BC6"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "padding": "md",
                            "backgroundColor": "#F5F5F5",
                            "cornerRadius": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Your Question:",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#999999"
                                },
                                {
                                    "type": "text",
                                    "text": query[:200] + ("..." if len(query) > 200 else ""),
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "padding": "md",
                            "backgroundColor": "#E8F0FE",
                            "cornerRadius": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🤖 AI Answer:",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#667BC6"
                                },
                                {
                                    "type": "text",
                                    "text": response[:300] + ("..." if len(response) > 300 else ""),
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"Today: {daily_used}/{daily_limit}",
                                    "size": "xs",
                                    "color": "#999999",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "🔋" if daily_used < daily_limit else "⚠️ Limit Reached",
                                    "size": "xs",
                                    "color": "#667BC6" if daily_used < daily_limit else "#FF6B6B"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "💭 Continue Chat",
                                "text": "/ai continue"
                            },
                            "style": "primary",
                            "color": "#667BC6"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🆕 New Chat",
                                "text": "/ai start"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            }
        }
