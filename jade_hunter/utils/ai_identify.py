"""
Claude Vision API を使った翡翠識別
APIキーがない場合はデモ結果を返す
"""
import base64
import json
from typing import Optional


def identify_jade_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    api_key: Optional[str] = None,
) -> dict:
    """
    画像から翡翠かどうかを識別する

    Returns:
        {
          "is_jade": bool,
          "confidence": int,          # 0-100
          "mineral_name": str,
          "color": str,
          "hardness_estimate": str,
          "luster": str,
          "reasoning": str,
          "recommendation": str,
          "source": "api" | "demo"
        }
    """
    if not api_key:
        return _demo_result()

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

        system_prompt = """あなたは鉱物・宝石の専門家です。
ユーザーが送る石の画像を見て、翡翠（ジェダイト）かどうかを判定してください。
必ず以下のJSON形式のみで回答してください（他のテキストは一切含めない）:

{
  "is_jade": true/false,
  "confidence": 0-100,
  "mineral_name": "推定鉱物名（日本語）",
  "color": "色の説明",
  "hardness_estimate": "硬度の推定（例: 6.5-7）",
  "luster": "光沢の種類（ガラス光沢など）",
  "reasoning": "判断根拠（2-3文）",
  "recommendation": "採集者へのアドバイス"
}"""

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": "この石を鑑定してください。"},
                ],
            }],
        )

        result = json.loads(response.content[0].text)
        result["source"] = "api"
        return result

    except Exception as e:
        demo = _demo_result()
        demo["reasoning"] += f"（API エラー: {str(e)[:60]}）"
        return demo


def _demo_result() -> dict:
    """デモ用のサンプル結果"""
    return {
        "is_jade": False,
        "confidence": 45,
        "mineral_name": "蛇紋岩（推定）",
        "color": "淡緑色〜灰緑色",
        "hardness_estimate": "3-4（爪で傷つく可能性あり）",
        "luster": "脂肪光沢",
        "reasoning": (
            "色調は翡翠に似ていますが、光沢が脂肪光沢に近く、"
            "翡翠特有のガラス光沢とは異なります。"
            "硬度が低い可能性があり、蛇紋岩や緑泥石片岩の可能性が高いです。"
        ),
        "recommendation": (
            "コイン（硬度3.5）で引っかいて傷がつくなら翡翠ではありません。"
            "より詳しい鑑定は糸魚川市のフォッサマグナミュージアムへ。"
        ),
        "source": "demo",
    }
