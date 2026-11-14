"""採集ゲームページ"""
import streamlit as st
import random
from utils.game_engine import init_game, advance_day, get_final_rating, SPOTS
from utils.weather import build_score_calendar


def show():
    st.title("🎮 翡翠採集シミュレーション")
    st.markdown("7日間の採集旅をシミュレーション。現実の採集難易度を体験しよう。")

    # ゲーム初期化
    if "game_state" not in st.session_state:
        st.session_state.game_state = None

    # 天気スコア取得
    try:
        df = build_score_calendar()
        scores = df["jade_score"].tolist()
    except Exception:
        scores = [random.randint(20, 80) for _ in range(10)]

    if st.session_state.game_state is None:
        st.info("7日間の翡翠採集をシミュレーションします。毎日スポットを選んで探索！")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🎮 ゲームスタート！", type="primary", use_container_width=True):
                st.session_state.game_state = init_game()
                st.session_state.game_scores = scores[:7] if len(scores) >= 7 else scores + [50] * 7
                st.rerun()
        return

    state = st.session_state.game_state
    game_scores = st.session_state.get("game_scores", [50] * 7)

    if state.game_over:
        _show_result(state)
        if st.button("🔄 もう一度プレイ"):
            st.session_state.game_state = None
            st.rerun()
        return

    # ── 現在の状況 ──
    day = state.current_day
    jade_score = game_scores[day - 1] if day - 1 < len(game_scores) else 50

    st.markdown(f"### 📅 {day} 日目 / {state.total_days} 日間")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("今日の翡翠スコア", f"{jade_score} / 100")
    with col2:
        jade_found = sum(1 for r in state.finds if r.found)
        st.metric("発見した翡翠", f"{jade_found} 個")
    with col3:
        st.metric("累計スコア", f"{state.score} pt")

    if day > 1 and state.finds:
        last = state.finds[-1]
        icon = "✅" if last.found else "❌"
        st.info(f"{icon} 昨日（{last.spot}）: **{last.item}**\n\n{last.description}")

    st.divider()
    st.subheader("今日のスポットを選んでください")
    spot = st.radio("採集スポット", SPOTS, horizontal=True)

    if st.button(f"🔍 {spot} を探索する", type="primary"):
        new_state = advance_day(state, jade_score, spot)
        st.session_state.game_state = new_state
        st.rerun()


def _show_result(state):
    rating = get_final_rating(state)
    jade_count = sum(1 for r in state.finds if r.found)

    st.balloons()
    st.success(f"## 🏁 旅終了！ あなたの評価: **{rating}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("発見した翡翠", f"{jade_count} 個")
        st.metric("合計スコア", f"{state.score} pt")
    with col2:
        st.markdown("#### 採集記録")
        for r in state.finds:
            icon = "💎" if r.found else "🪨"
            st.write(f"{icon} {r.day}日目 {r.spot}: {r.item}")

    st.divider()
    st.info(
        "🌊 **気づきましたか？**\n\n"
        f"7日間で翡翠が見つかったのは **{jade_count} 回**。"
        "現実の採集難易度を少し体感できましたか？\n\n"
        "糸魚川では年間数百人の愛好家が訪れますが、"
        "本物の翡翠と出会えるのはほんの一部の人だけ。"
        "だからこそ、見つけたときの喜びは格別です。\n\n"
        "**採集ルールを守り、地域の自然文化遺産を次の世代に残しましょう。**"
    )
