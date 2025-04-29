"""
ロギング設定ファイル

このモジュールは、アプリケーション全体で使用されるロギング機能を提供します。
ログのフォーマット、出力先、ログレベルなどを設定します。

Attributes:
    logger (Logger): アプリケーション全体で使用するロガーインスタンス
"""

import logging
import sys
from pathlib import Path
from .config import LOG_LEVEL, BASE_DIR

# ログディレクトリの作成
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ログファイルのパス
LOG_FILE = LOG_DIR / "app.log"

# ロガーの設定
logger = logging.getLogger("ai_engineering")
logger.setLevel(LOG_LEVEL)

# フォーマッターの設定
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ファイルハンドラーの設定
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# コンソールハンドラーの設定
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    指定された名前のロガーを取得します。

    Args:
        name (str): ロガーの名前

    Returns:
        logging.Logger: ロガーインスタンス
    """
    return logger.getChild(name) 
