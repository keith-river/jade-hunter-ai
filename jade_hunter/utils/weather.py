"""
Open-Meteo Marine API ラッパー
糸魚川沖（lat=37.04, lon=137.86）の波浪・気象データを取得
"""
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

ITOIGAWA_LAT = 37.04
ITOIGAWA_LON = 137.86
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def _cache(func):
    """Streamlit の st.cache_data がある場合のみキャッシュ適用"""
    if HAS_STREAMLIT:
        return st.cache_data(ttl=3600)(func)
    return func


@_cache
def fetch_marine_data() -> dict:
    """波浪データを取得（失敗時はダミーデータ）"""
    try:
        params = {
            "latitude": ITOIGAWA_LAT,
            "longitude": ITOIGAWA_LON,
            "hourly": "wave_height,wave_direction,wave_period",
            "daily": "wave_height_max",
            "timezone": "Asia/Tokyo",
            "past_days": 3,
            "forecast_days": 7,
        }
        r = requests.get(MARINE_URL, params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception:
        return _dummy_marine()


@_cache
def fetch_weather_data() -> dict:
    """気象データを取得（失敗時はダミーデータ）"""
    try:
        params = {
            "latitude": ITOIGAWA_LAT,
            "longitude": ITOIGAWA_LON,
            "hourly": "windspeed_10m,winddirection_10m",
            "daily": "windspeed_10m_max",
            "timezone": "Asia/Tokyo",
            "past_days": 3,
            "forecast_days": 7,
        }
        r = requests.get(WEATHER_URL, params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception:
        return _dummy_weather()


def calc_jade_score(today_wave: float, prev_wave: float, wind_speed: float = 5.0) -> int:
    """
    翡翠発見期待スコアを計算（0〜100）

    formula:
      prev_factor  = min(prev_wave / 3.5, 1.0) * 0.60   # 前日高波 60%
      calm_factor  = (1 - min(today_wave / 2.5, 1.0)) * 0.40  # 当日静穏 30% + 低風 10%
      wind_factor  = (1 - min(wind_speed / 15.0, 1.0)) * 0.10

    経験則: 前日に荒れ → 翡翠が打ち上げられ、当日穏やか → 採集しやすい
    """
    prev_factor = min(prev_wave / 3.5, 1.0) * 0.60
    calm_factor = (1 - min(today_wave / 2.5, 1.0)) * 0.30
    wind_factor = (1 - min(wind_speed / 15.0, 1.0)) * 0.10
    score = int((prev_factor + calm_factor + wind_factor) * 100)
    return max(0, min(100, score))


def build_score_calendar() -> pd.DataFrame:
    """日別の翡翠スコアを DataFrame で返す"""
    marine = fetch_marine_data()
    weather = fetch_weather_data()

    daily_wave = marine.get("daily", {}).get("wave_height_max", [])
    daily_wind = weather.get("daily", {}).get("windspeed_10m_max", [])
    dates = marine.get("daily", {}).get("time", [])

    rows = []
    for i, date in enumerate(dates):
        today_wave = float(daily_wave[i]) if i < len(daily_wave) and daily_wave[i] else 1.0
        prev_wave  = float(daily_wave[i-1]) if i > 0 and daily_wave[i-1] else 1.0
        wind       = float(daily_wind[i]) if i < len(daily_wind) and daily_wind[i] else 5.0
        score      = calc_jade_score(today_wave, prev_wave, wind)
        rows.append({
            "date": date,
            "wave_height": round(today_wave, 2),
            "wind_speed": round(wind, 1),
            "jade_score": score,
        })

    return pd.DataFrame(rows)


# ── ダミーデータ（API オフライン時） ──
def _dummy_marine() -> dict:
    rng = np.random.default_rng(42)
    today = datetime.now()
    times = [(today - timedelta(days=3) + timedelta(days=i)).strftime("%Y-%m-%d")
             for i in range(10)]
    waves = [round(float(w), 2) for w in rng.uniform(0.3, 4.0, 10)]
    return {
        "daily": {
            "time": times,
            "wave_height_max": waves,
        }
    }


def _dummy_weather() -> dict:
    rng = np.random.default_rng(42)
    today = datetime.now()
    times = [(today - timedelta(days=3) + timedelta(days=i)).strftime("%Y-%m-%d")
             for i in range(10)]
    winds = [round(float(w), 1) for w in rng.uniform(2, 20, 10)]
    return {
        "daily": {
            "time": times,
            "windspeed_10m_max": winds,
        }
    }
