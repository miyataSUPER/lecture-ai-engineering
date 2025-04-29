"""
共通設定ファイル

このモジュールは、アプリケーション全体で使用される共通の設定を管理します。
環境変数やデフォルト値、定数などを定義します。

Attributes:
    HUGGINGFACE_TOKEN (str): HuggingFaceのAPIトークン
    NGROK_TOKEN (str): ngrokの認証トークン
    MODEL_CACHE_DIR (str): モデルのキャッシュディレクトリ
    LOG_LEVEL (str): ログレベル
    MAX_RETRIES (int): API呼び出しの最大リトライ回数
    TIMEOUT (int): API呼び出しのタイムアウト時間（秒）
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# 環境変数の読み込み
load_dotenv(find_dotenv())

# APIトークン
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
NGROK_TOKEN = os.getenv("NGROK_TOKEN")

# ディレクトリ設定
BASE_DIR = Path(__file__).parent.parent
MODEL_CACHE_DIR = BASE_DIR / "cache" / "models"
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API設定
MAX_RETRIES = 3
TIMEOUT = 30

# モデル設定
DEFAULT_MODEL = "gpt2"
SUPPORTED_MODELS = {
    "gpt2": "gpt2",
    "gpt2-medium": "gpt2-medium",
    "gpt2-large": "gpt2-large",
    "gpt2-xl": "gpt2-xl"
}

# エラーメッセージ
ERROR_MESSAGES = {
    "API_ERROR": "API呼び出し中にエラーが発生しました: {error}",
    "MODEL_LOAD_ERROR": "モデルの読み込み中にエラーが発生しました: {error}",
    "INVALID_INPUT": "無効な入力が指定されました: {input}",
    "CACHE_ERROR": "キャッシュ操作中にエラーが発生しました: {error}"
} 
