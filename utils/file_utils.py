"""
File utilities - 檔案操作工具
"""
import json
import os


def load_json(filepath):
    """
    載入 JSON 檔案
    
    Args:
        filepath: 檔案路徑
    
    Returns:
        dict 或預設空字典
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 讀取 {filepath} 出錯: {e}")
            return {}
    return {}


def save_json(filepath, data):
    """
    保存 JSON 檔案
    
    Args:
        filepath: 檔案路徑
        data: 要保存的字典
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"saved {filepath}")
    except Exception as e:
        print(f"error saving {filepath}: {e}")


def ensure_file_exists(filepath, default_content=None):
    """
    確保檔案存在，若不存在則創建
    
    Args:
        filepath: 檔案路徑
        default_content: 預設內容（dict 則保存為 JSON）
    """
    if not os.path.exists(filepath):
        if default_content:
            if isinstance(default_content, dict):
                save_json(filepath, default_content)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(str(default_content))
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("")
