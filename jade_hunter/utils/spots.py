"""
糸魚川翡翠採集スポットデータ
"""
from dataclasses import dataclass
from typing import List
import pandas as pd


@dataclass
class JadeSpot:
    name: str
    lat: float
    lon: float
    description: str
    access: str
    best_condition: str
    difficulty: str   # 初級 / 中級 / 上級
    rules: str


SPOTS: List[JadeSpot] = [
    JadeSpot(
        name="親不知海岸",
        lat=37.012,
        lon=137.666,
        description="断崖絶壁の下に広がる礫浜。糸魚川西端の有名スポット。",
        access="北陸自動車道・親不知ICから車で5分",
        best_condition="前日波高2m以上、当日1m以下の凪",
        difficulty="中級",
        rules="駐車場あり。高波・落石に注意。単独行動禁止。",
    ),
    JadeSpot(
        name="小滝川礫層",
        lat=36.945,
        lon=137.883,
        description="翡翠が上流から流れてくる川の礫層。国の天然記念物指定区域に隣接。",
        access="JR大糸線・小滝駅から徒歩15分",
        best_condition="増水後の水位低下時（増水中は危険）",
        difficulty="上級",
        rules="⚠️ 一部区域は採集禁止。事前に市のガイドラインを確認のこと。",
    ),
    JadeSpot(
        name="姫川河口",
        lat=37.047,
        lon=137.861,
        description="姫川が日本海に注ぐ河口付近。翡翠の産出地として有名な姫川沿い。",
        access="JR糸魚川駅から車で5分",
        best_condition="大雨後2〜3日、波が落ち着いたタイミング",
        difficulty="初級",
        rules="駐車場あり。河口付近は流れに注意。",
    ),
    JadeSpot(
        name="須沢海岸",
        lat=37.053,
        lon=137.914,
        description="糸魚川市街東側の砂礫浜。家族連れにも人気のアクセスしやすいスポット。",
        access="JR糸魚川駅から車で10分",
        best_condition="北西の風が続いた翌日の凪",
        difficulty="初級",
        rules="海水浴シーズンは混雑。ゴミの持ち帰りを忘れずに。",
    ),
    JadeSpot(
        name="能生海岸",
        lat=37.090,
        lon=138.023,
        description="糸魚川市東部の海岸。比較的穴場で静かに探索できる。",
        access="北陸自動車道・能生ICから車で5分",
        best_condition="冬季〜春季の荒天後",
        difficulty="初級",
        rules="漁港周辺は立入禁止区域あり。地元ルールを守ること。",
    ),
]


def rank_spots(jade_score: int, condition: str = "normal") -> pd.DataFrame:
    """
    翡翠スコアと条件に基づいてスポットをランキング

    Returns:
        DataFrame with columns: スポット, 推奨度, 説明, アクセス, 難易度, 注意事項
    """
    rows = []
    for spot in SPOTS:
        # 難易度補正
        diff_bonus = {"初級": 10, "中級": 0, "上級": -10}.get(spot.difficulty, 0)

        # スコアが高い時は上級スポットを優遇
        if jade_score >= 70:
            diff_bonus = {"初級": 0, "中級": 5, "上級": 15}.get(spot.difficulty, 0)

        base_score = jade_score + diff_bonus
        # スポットごとに微妙にばらつかせる（ハッシュベース）
        offset = hash(spot.name) % 11 - 5
        rank_score = max(0, min(100, base_score + offset))

        emoji = "🟢" if rank_score >= 70 else "🟡" if rank_score >= 40 else "🔴"
        rows.append({
            "スポット": spot.name,
            "推奨度": f"{emoji} {rank_score}点",
            "スコア": rank_score,
            "説明": spot.description,
            "アクセス": spot.access,
            "ベスト条件": spot.best_condition,
            "難易度": spot.difficulty,
            "注意事項": spot.rules,
        })

    df = pd.DataFrame(rows)
    return df.sort_values("スコア", ascending=False).reset_index(drop=True)


def get_spot_coordinates() -> List[dict]:
    """地図表示用の座標リストを返す"""
    return [
        {"name": s.name, "lat": s.lat, "lon": s.lon, "difficulty": s.difficulty}
        for s in SPOTS
    ]
