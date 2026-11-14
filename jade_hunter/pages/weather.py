"""天気・波浪予測ページ"""
import streamlit as st
import plotly.graph_objects as go
from utils.weather import build_score_calendar


def show():
    st.title("🌊 天気・波浪予測")
    st.markdown("**Open-Meteo Marine API** で糸魚川沖のリアルタイムデータを取得します。")

    with st.spinner("データ取得中..."):
        df = build_score_calendar()

    st.success(f"✅ {len(df)} 日分のデータを取得しました（過去3日 + 今日 + 予報6日）")

    # ── スコアグラフ ──
    fig = go.Figure()
    colors = ["#2ecf96" if s >= 70 else "#f4c430" if s >= 40 else "#e05c5c"
              for s in df["jade_score"]]

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["jade_score"],
        marker_color=colors,
        name="翡翠スコア",
        hovertemplate="<b>%{x}</b><br>翡翠スコア: %{y}<br><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["wave_height"],
        mode="lines+markers",
        name="波高 (m)",
        yaxis="y2",
        line=dict(color="#4fc3f7", width=2),
        marker=dict(size=5),
    ))
    fig.update_layout(
        title="翡翠採集スコアカレンダー",
        yaxis=dict(title="翡翠スコア (0-100)", range=[0, 105]),
        yaxis2=dict(title="波高 (m)", overlaying="y", side="right", range=[0, 6]),
        legend=dict(x=0, y=1.1, orientation="h"),
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── テーブル ──
    st.subheader("📊 日別データ")
    display_df = df.copy()
    display_df["スコア"] = display_df["jade_score"].apply(
        lambda s: f"🟢 {s}" if s >= 70 else f"🟡 {s}" if s >= 40 else f"🔴 {s}"
    )
    st.dataframe(
        display_df[["date", "wave_height", "wind_speed", "スコア"]].rename(columns={
            "date": "日付", "wave_height": "波高(m)", "wind_speed": "風速(km/h)"
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    with st.expander("📐 スコア計算式を見る"):
        st.markdown("""
```
翡翠スコア = 前日高波スコア(60%) + 当日静穏スコア(30%) + 低風スコア(10%)

前日高波 = min(前日波高 / 3.5, 1.0) × 60
当日静穏 = (1 - min(当日波高 / 2.5, 1.0)) × 30
低風    = (1 - min(風速 / 15.0, 1.0)) × 10
```
**経験則**: 前日に荒れた海が翡翠を打ち上げ、当日凪いだときが採集好機。
        """)
