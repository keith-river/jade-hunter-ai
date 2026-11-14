"""スポット推薦ページ"""
import streamlit as st
from utils.weather import build_score_calendar
from utils.spots import rank_spots, get_spot_coordinates


def show():
    st.title("📍 スポット推薦")
    st.markdown("今日の波浪条件に応じて、採集スポットをランキングします。")

    try:
        df_weather = build_score_calendar()
        today_score = int(df_weather[df_weather["date"] >= df_weather["date"].iloc[3]].iloc[0]["jade_score"])
    except Exception:
        today_score = 50

    st.metric("今日の翡翠スコア", f"{today_score} / 100")

    df = rank_spots(today_score)

    st.subheader("🏆 本日のスポットランキング")
    for i, row in df.iterrows():
        with st.expander(f"**{i+1}位: {row['スポット']}** — {row['推奨度']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**説明**: {row['説明']}")
                st.markdown(f"**アクセス**: {row['アクセス']}")
                st.markdown(f"**ベスト条件**: {row['ベスト条件']}")
            with col2:
                st.markdown(f"**難易度**: {row['難易度']}")
                st.warning(f"⚠️ {row['注意事項']}")

    st.divider()
    st.subheader("🗺️ スポット位置（概略）")

    coords = get_spot_coordinates()
    coord_df = st.dataframe(
        [[c["name"], c["lat"], c["lon"], c["difficulty"]] for c in coords],
        column_config={
            0: "スポット名",
            1: st.column_config.NumberColumn("緯度", format="%.3f"),
            2: st.column_config.NumberColumn("経度", format="%.3f"),
            3: "難易度",
        },
        hide_index=True,
        use_container_width=True,
    )

    st.caption("💡 地図アプリで「糸魚川 ヒスイ海岸」と検索すると詳細な位置が確認できます。")
