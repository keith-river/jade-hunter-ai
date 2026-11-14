"""AI画像識別ページ"""
import streamlit as st
from utils.ai_identify import identify_jade_image


def show():
    st.title("🔍 AI画像識別")
    st.markdown("石の写真をアップロードすると、**Claude Vision AI** が翡翠かどうかを鑑定します。")

    api_key = st.session_state.get("api_key", "")

    if not api_key:
        st.warning(
            "⚠️ Anthropic APIキーが設定されていません。"
            "サイドバーでAPIキーを入力するか `.env` に設定してください。\n\n"
            "**デモモード**: サンプル結果を表示します。"
        )

    uploaded = st.file_uploader(
        "石の画像をアップロード（JPG / PNG）",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded:
        st.image(uploaded, caption="アップロードした画像", width=300)

        if st.button("🔍 鑑定する", type="primary"):
            with st.spinner("Claude Vision AI が鑑定中..."):
                result = identify_jade_image(
                    uploaded.read(),
                    mime_type=uploaded.type or "image/jpeg",
                    api_key=api_key,
                )

            # 結果表示
            if result.get("source") == "demo":
                st.info("📌 デモモードの結果です（実際のAPIは使用していません）")

            is_jade = result.get("is_jade", False)
            conf    = result.get("confidence", 0)

            if is_jade and conf >= 70:
                st.success(f"✅ **翡翠の可能性が高い** — 信頼度: {conf}%")
            elif is_jade:
                st.warning(f"🟡 **翡翠かもしれない** — 信頼度: {conf}%（要追加確認）")
            else:
                st.error(f"❌ **翡翠ではない可能性が高い** — 信頼度: {100-conf}%")

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**推定鉱物**: {result.get('mineral_name', '不明')}")
                st.markdown(f"**色**: {result.get('color', '不明')}")
                st.markdown(f"**硬度推定**: {result.get('hardness_estimate', '不明')}")
                st.markdown(f"**光沢**: {result.get('luster', '不明')}")
            with col2:
                st.markdown("**判断根拠**")
                st.info(result.get("reasoning", ""))
                st.markdown("**採集者へのアドバイス**")
                st.success(result.get("recommendation", ""))

    st.divider()
    with st.expander("💡 自分でできる簡易チェック方法"):
        st.markdown("""
| チェック方法 | 翡翠の場合 | 類似石の場合 |
|-------------|-----------|------------|
| **爪で引っかく** | 傷つかない（硬度6.5〜7） | 傷つく可能性（蛇紋岩は硬度3〜4） |
| **光にかざす** | 半透明〜不透明、繊維状の輝き | 透明すぎる or まったく透けない |
| **表面の光沢** | ガラス光沢〜脂肪光沢 | 絹糸光沢（緑泥石片岩）|
| **比重** | 重い（比重 3.2〜3.4） | 軽め（蛇紋岩は 2.5〜2.8） |
| **叩いた音** | 澄んだ金属音 | 鈍い音 |

⚠️ **最終判断はプロへ**: フォッサマグナミュージアム（糸魚川市）では無料鑑定サービスあり。
        """)
