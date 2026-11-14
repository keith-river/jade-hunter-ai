"""ホームページ"""
import streamlit as st
from utils.weather import build_score_calendar


def show():
    st.title("💎 ヒスイハンター AI")
    st.markdown("### 糸魚川翡翠 探索支援システム")

    st.info(
        "🌊 **糸魚川市**（新潟県）は日本最古の翡翠文明の発祥地。"
        "世界でも珍しい翡翠の自然採集ができる場所ですが、"
        "**持続可能な採集のためのルール**を守ることが大切です。",
        icon="ℹ️",
    )

    # 今日のスコア
    try:
        df = build_score_calendar()
        today_row = df[df["date"] >= df["date"].iloc[3]].iloc[0]
        score = int(today_row["jade_score"])
    except Exception:
        score = 42

    col1, col2, col3 = st.columns(3)
    with col1:
        color = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"
        st.metric("今日の翡翠スコア", f"{color} {score} / 100")
    with col2:
        st.metric("採集スポット数", "5 カ所")
    with col3:
        st.metric("対応機能", "4 種類")

    st.divider()

    st.subheader("📋 このアプリについて")
    st.markdown("""
| 機能 | 説明 |
|------|------|
| 🌊 天気・波浪予測 | Open-Meteo API で波浪データを取得し、翡翠が打ち上げられやすい日を予測 |
| 📍 スポット推薦 | 天気条件に応じた採集スポットをスコアリングして地図表示 |
| 🔍 AI画像識別 | 石の写真をアップロードすると Claude Vision が翡翠かどうかを鑑定 |
| 🎮 採集ゲーム | 7日間のシミュレーションゲームで採集の難しさと楽しさを体験 |
| 📚 チュートリアル | 翡翠の見分け方、地域ルール、持続可能な採集について学ぶ |
    """)

    st.divider()
    st.caption(
        "⚠️ このアプリは試作版です。実際の採集には地元のルールと法律を遵守してください。"
        "天然記念物指定区域での採集は法律で禁止されています。"
    )
