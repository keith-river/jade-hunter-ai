"""
翡翠採集ゲームエンジン
現実の採集確率を参考にしたシミュレーション
"""
from dataclasses import dataclass, field
from typing import List, Optional
import random
import math


@dataclass
class SearchResult:
    day: int
    spot: str
    found: bool
    item: str
    description: str
    jade_score: int


@dataclass
class GameDay:
    day: int
    jade_score: int
    weather: str
    wave: float
    results: List[SearchResult] = field(default_factory=list)


@dataclass
class GameState:
    total_days: int = 7
    current_day: int = 1
    finds: List[SearchResult] = field(default_factory=list)
    game_over: bool = False
    score: int = 0
    days: List[GameDay] = field(default_factory=list)


SPOTS = ["親不知海岸", "姫川河口", "須沢海岸", "小滝川礫層", "能生海岸"]

ITEMS = {
    "jade": {
        "name": "翡翠（本物）🪨",
        "description": "硬度6.5〜7のヒスイ輝石。光に透かすと深い緑が美しい。",
        "score": 100,
    },
    "serpentine": {
        "name": "蛇紋岩（類似石）",
        "description": "翡翠に似た緑色だが、爪で傷がつく（硬度3〜4）。",
        "score": 10,
    },
    "quartz": {
        "name": "石英・チャート",
        "description": "白〜灰色。川で丸く磨かれた一般的な礫石。",
        "score": 5,
    },
    "nothing": {
        "name": "収穫なし",
        "description": "今日は見つからなかった。明日に期待しよう。",
        "score": 0,
    },
}

WEATHERS = ["晴れ☀️", "曇り☁️", "小雨🌧️", "強風💨"]


def calc_jade_probability(jade_score: int) -> float:
    """
    翡翠発見確率を計算

    現実: 約 1/200 = 0.5% / 日
    ゲーム: jade_score=100 で最大 15% 程度（楽しめる難易度）

    formula: base + boost * (score/100)^1.5
    """
    base  = 0.005
    boost = 0.145
    prob  = base + boost * math.pow(jade_score / 100.0, 1.5)
    return min(prob, 0.20)


def search_beach(jade_score: int, spot: str, day: int) -> SearchResult:
    """ビーチ探索を実行し結果を返す"""
    prob = calc_jade_probability(jade_score)
    r = random.random()

    if r < prob:
        item_key = "jade"
    elif r < prob + 0.25:
        item_key = "serpentine"
    elif r < prob + 0.55:
        item_key = "quartz"
    else:
        item_key = "nothing"

    item = ITEMS[item_key]
    return SearchResult(
        day=day,
        spot=spot,
        found=(item_key == "jade"),
        item=item["name"],
        description=item["description"],
        jade_score=jade_score,
    )


def advance_day(state: GameState, jade_score: int, spot: str) -> GameState:
    """1日進める"""
    result = search_beach(jade_score, spot, state.current_day)
    state.finds.append(result)

    game_day = GameDay(
        day=state.current_day,
        jade_score=jade_score,
        weather=random.choice(WEATHERS),
        wave=round(random.uniform(0.3, 4.0), 1),
        results=[result],
    )
    state.days.append(game_day)

    if result.found:
        state.score += 100
    else:
        state.score += ITEMS.get(
            next((k for k, v in ITEMS.items() if v["name"] == result.item), "nothing"),
            ITEMS["nothing"]
        )["score"]

    state.current_day += 1
    if state.current_day > state.total_days:
        state.game_over = True

    return state


def init_game() -> GameState:
    return GameState()


def get_final_rating(state: GameState) -> str:
    jade_count = sum(1 for r in state.finds if r.found)
    if jade_count >= 3:
        return "🏆 翡翠マスター"
    elif jade_count == 2:
        return "💎 熟練ハンター"
    elif jade_count == 1:
        return "🌊 見習いハンター"
    else:
        return "🪨 次回に期待"
