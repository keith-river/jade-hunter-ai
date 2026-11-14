"""
ヒスイハンター AI — メインアプリ
起動: streamlit run jade_hunter/app.py
"""
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="💎 ヒスイハンター AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── グローバルCSS ──
st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #071828; }
  [data-testid="stSidebar"] * { color: #e8f4f0 !important; }
  [data-testid="stSidebar"] label { color: #e8f4f0 !important; }
  [data-testid="stSidebar"] [aria-checked="true"] p { color: #2ecf96 !important; font-weight: 600; }
  [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #8fb8a8 !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #c8e0d8 !important; }
  .jade-metric { color: #2ecf96 !important; }
  .stTabs [data-baseweb="tab"] { font-size: 14px; }
  .stTabs [aria-selected="true"] { color: #2ecf96; border-bottom-color: #2ecf96; }
  div[data-testid="metric-container"] {
    background: rgba(46,207,150,0.06);
    border: 1px solid rgba(46,207,150,0.2);
    border-radius: 8px;
    padding: 12px;
  }
</style>
""", unsafe_allow_html=True)

# ── サイドバー ──
with st.sidebar:
    st.markdown("## 💎 ヒスイハンター AI")
    st.markdown("**糸魚川翡翠 探索支援システム**")
    st.divider()
    page = st.radio(
        "メニュー",
        ["🏠 ホーム", "🌊 天気・波浪予測", "📍 スポット推薦",
         "🔍 AI画像識別", "🎮 採集ゲーム", "📚 チュートリアル"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("**APIステータス**")
    st.success("✅ Open-Meteo (無料)")

    # APIキー: 環境変数 or フォーム入力
    env_key = os.getenv("ANTHROPIC_API_KEY", "")
    if env_key:
        st.session_state["api_key"] = env_key
        st.success("✅ Claude Vision (.env)")
    else:
        api_key = st.text_input("Anthropic API Key", type="password",
                                 placeholder="sk-ant-...")
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("✅ Claude Vision 有効")
        else:
            st.warning("⚠️ Vision AI 未設定（デモモード）")

# ── ページルーティング ──
if page == "🏠 ホーム":
    from pages.home import show; show()
elif page == "🌊 天気・波浪予測":
    from pages.weather import show; show()
elif page == "📍 スポット推薦":
    from pages.spots import show; show()
elif page == "🔍 AI画像識別":
    from pages.ai_identify import show; show()
elif page == "🎮 採集ゲーム":
    from pages.game import show; show()
elif page == "📚 チュートリアル":
    from pages.tutorial import show; show()
