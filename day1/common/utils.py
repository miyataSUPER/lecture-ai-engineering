"""
共通ユーティリティ関数

このモジュールは、アプリケーション全体で使用される共通のユーティリティ関数を提供します。
キャッシュ、エラーハンドリング、型変換などの機能を含みます。
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
from functools import wraps
import time

from .config import MODEL_CACHE_DIR, ERROR_MESSAGES
from .logger import get_logger

logger = get_logger(__name__)

def cache_result(func):
    """
    関数の結果をキャッシュするデコレータ

    Args:
        func: キャッシュ対象の関数

    Returns:
        デコレートされた関数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # キャッシュキーの生成
        cache_key = hashlib.md5(
            f"{func.__name__}{str(args)}{str(kwargs)}".encode()
        ).hexdigest()
        
        cache_file = MODEL_CACHE_DIR / f"{cache_key}.json"
        
        # キャッシュが存在する場合は読み込み
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"キャッシュの読み込みに失敗しました: {e}")
        
        # 関数の実行
        result = func(*args, **kwargs)
        
        # 結果をキャッシュ
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"キャッシュの保存に失敗しました: {e}")
        
        return result
    
    return wrapper

def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """
    エラー発生時にリトライするデコレータ

    Args:
        max_retries (int): 最大リトライ回数
        delay (float): リトライ間隔（秒）

    Returns:
        デコレートされた関数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"リトライ {attempt + 1}/{max_retries}: {str(e)}"
                        )
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

def format_error_message(error_type: str, **kwargs) -> str:
    """
    エラーメッセージをフォーマットする

    Args:
        error_type (str): エラーの種類
        **kwargs: エラーメッセージのフォーマットに使用する引数

    Returns:
        str: フォーマットされたエラーメッセージ
    """
    if error_type not in ERROR_MESSAGES:
        return f"不明なエラー: {error_type}"
    return ERROR_MESSAGES[error_type].format(**kwargs)

def safe_json_load(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    JSONファイルを安全に読み込む

    Args:
        file_path (Path): JSONファイルのパス

    Returns:
        Optional[Dict[str, Any]]: 読み込んだJSONデータ
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSONファイルの読み込みに失敗しました: {e}")
        return None 
