"""
モデルサービス

このモジュールは、AIモデルの操作に関する機能を提供します。
モデルの読み込み、推論、キャッシュなどの機能を含みます。
"""

from typing import Optional, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from common.config import DEFAULT_MODEL, SUPPORTED_MODELS
from common.utils import cache_result, retry_on_error
from common.logger import get_logger

logger = get_logger(__name__)

class ModelService:
    """
    AIモデルを操作するためのサービスクラス
    """
    
    def __init__(self, model_name: str = DEFAULT_MODEL):
        """
        初期化

        Args:
            model_name (str): 使用するモデルの名前
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """
        モデルを読み込む
        """
        try:
            logger.info(f"モデル {self.model_name} を読み込み中...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            logger.info("モデルの読み込みが完了しました")
        except Exception as e:
            logger.error(f"モデルの読み込みに失敗しました: {e}")
            raise
    
    @retry_on_error(max_retries=3)
    @cache_result
    def generate_text(
        self,
        prompt: str,
        max_length: int = 100,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        テキストを生成する

        Args:
            prompt (str): プロンプト
            max_length (int): 生成するテキストの最大長
            temperature (float): 生成の多様性を制御するパラメータ
            **kwargs: その他のパラメータ

        Returns:
            str: 生成されたテキスト
        """
        try:
            # 入力のトークン化
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            # テキスト生成
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    temperature=temperature,
                    **kwargs
                )
            
            # 生成されたテキストのデコード
            generated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            return generated_text
        
        except Exception as e:
            logger.error(f"テキスト生成に失敗しました: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        モデルの情報を取得する

        Returns:
            Dict[str, Any]: モデルの情報
        """
        return {
            "name": self.model_name,
            "parameters": sum(
                p.numel() for p in self.model.parameters()
            ),
            "supported_models": list(SUPPORTED_MODELS.keys())
        } 
