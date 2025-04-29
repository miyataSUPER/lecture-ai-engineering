"""
Streamlitアプリケーション

このモジュールは、Streamlitを使用したAIアプリケーションのメインファイルです。
UIコンポーネントとモデルサービスを統合し、アプリケーションを実行します。
"""

import streamlit as st
from typing import Dict, Any

from components.header import display_header
from components.sidebar import display_sidebar
from services.model_service import ModelService

# ページ設定
st.set_page_config(
    page_title="AI Text Generator",
    page_icon="🤖",
    layout="wide"
)

# セッション状態の初期化
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# メニュー項目
menu_items = [
    {"label": "ホーム", "key": "home"},
    {"label": "テキスト生成", "key": "generate"},
    {"label": "設定", "key": "settings"}
]

def main():
    """
    アプリケーションのメイン関数
    """
    # ヘッダーの表示
    display_header(
        title="AI Text Generator",
        description="AIモデルを使用してテキストを生成するアプリケーションです。",
        show_settings=True
    )
    
    # サイドバーの表示
    display_sidebar(
        menu_items=menu_items,
        show_filters=True,
        show_info=True
    )
    
    # 現在のページに応じたコンテンツの表示
    if st.session_state["current_page"] == "home":
        display_home_page()
    elif st.session_state["current_page"] == "generate":
        display_generate_page()
    elif st.session_state["current_page"] == "settings":
        display_settings_page()

def display_home_page():
    """
    ホームページを表示する
    """
    st.markdown("""
    ## ようこそ！
    
    このアプリケーションは、AIモデルを使用してテキストを生成します。
    
    ### 主な機能
    
    - テキスト生成
    - モデル選択
    - パラメータ調整
    
    ### 使い方
    
    1. サイドバーから「テキスト生成」を選択
    2. プロンプトを入力
    3. パラメータを調整
    4. 「生成」ボタンをクリック
    """)

def display_generate_page():
    """
    テキスト生成ページを表示する
    """
    # モデルサービスの初期化
    model_service = ModelService(st.session_state.get("model", "gpt2"))
    
    # 入力フォーム
    prompt = st.text_area(
        "プロンプト",
        placeholder="テキストを入力してください...",
        height=100
    )
    
    # 生成ボタン
    if st.button("生成"):
        if not prompt:
            st.error("プロンプトを入力してください")
            return
        
        try:
            # プログレスバーの表示
            with st.spinner("テキストを生成中..."):
                # テキスト生成
                generated_text = model_service.generate_text(
                    prompt=prompt,
                    max_length=st.session_state.get("max_length", 100),
                    temperature=st.session_state.get("temperature", 0.7)
                )
            
            # 結果の表示
            st.markdown("### 生成結果")
            st.text_area("", generated_text, height=200)
            
            # モデル情報の表示
            model_info = model_service.get_model_info()
            st.markdown("### モデル情報")
            st.json(model_info)
        
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

def display_settings_page():
    """
    設定ページを表示する
    """
    st.markdown("## 設定")
    
    # モデル選択
    model = st.selectbox(
        "モデル",
        ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"],
        index=0
    )
    st.session_state["model"] = model
    
    # パラメータ設定
    st.markdown("### パラメータ")
    
    max_length = st.slider(
        "最大長",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )
    st.session_state["max_length"] = max_length
    
    temperature = st.slider(
        "温度",
        min_value=0.1,
        max_value=2.0,
        value=0.7,
        step=0.1
    )
    st.session_state["temperature"] = temperature

if __name__ == "__main__":
    main()
