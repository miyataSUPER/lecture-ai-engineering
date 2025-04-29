"""
サイドバーコンポーネント

このモジュールは、Streamlitアプリケーションのサイドバー部分を提供します。
ナビゲーション、フィルター、その他のサイドバー機能を表示します。
"""

import streamlit as st
from typing import List, Optional, Dict, Any

def display_sidebar(
    menu_items: List[Dict[str, Any]],
    show_filters: bool = True,
    show_info: bool = True
) -> None:
    """
    サイドバーを表示する

    Args:
        menu_items (List[Dict[str, Any]]): メニュー項目のリスト
        show_filters (bool): フィルターを表示するかどうか
        show_info (bool): 情報を表示するかどうか
    """
    st.sidebar.title("メニュー")
    
    # メニュー項目の表示
    for item in menu_items:
        if st.sidebar.button(item["label"]):
            st.session_state["current_page"] = item["key"]
    
    if show_filters:
        st.sidebar.markdown("---")
        st.sidebar.subheader("フィルター")
        
        # 日付フィルター
        date_range = st.sidebar.date_input(
            "日付範囲",
            value=(None, None)
        )
        
        # カテゴリーフィルター
        categories = st.sidebar.multiselect(
            "カテゴリー",
            options=["技術", "ビジネス", "教育", "その他"]
        )
    
    if show_info:
        st.sidebar.markdown("---")
        st.sidebar.subheader("情報")
        st.sidebar.info(
            "このアプリケーションは、AIモデルを使用してテキストを生成します。"
        )
        
        # バージョン情報
        st.sidebar.markdown("### バージョン情報")
        st.sidebar.text("v1.0.0")
        
        # リンク
        st.sidebar.markdown("### リンク")
        st.sidebar.markdown(
            "[GitHubリポジトリ](https://github.com/example/repo)"
        ) 
