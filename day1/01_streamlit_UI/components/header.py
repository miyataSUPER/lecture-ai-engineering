"""
ヘッダーコンポーネント

このモジュールは、Streamlitアプリケーションのヘッダー部分を提供します。
アプリケーションのタイトル、説明、設定などを表示します。
"""

import streamlit as st
from typing import Optional

def display_header(
    title: str,
    description: Optional[str] = None,
    show_settings: bool = True
) -> None:
    """
    ヘッダーを表示する

    Args:
        title (str): アプリケーションのタイトル
        description (Optional[str]): アプリケーションの説明文
        show_settings (bool): 設定を表示するかどうか
    """
    st.title(title)
    
    if description:
        st.markdown(description)
    
    if show_settings:
        with st.expander("設定", expanded=False):
            st.selectbox(
                "モデル",
                ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"],
                key="model"
            )
            st.slider(
                "最大長",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                key="max_length"
            )
            st.slider(
                "温度",
                min_value=0.1,
                max_value=2.0,
                value=0.7,
                step=0.1,
                key="temperature"
            ) 
