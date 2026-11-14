# 💎 ヒスイハンター AI

> 新潟県糸魚川市の翡翠採集を支援するAIアプリケーション  
> 「地域課題×生成AI×ナッジ実験」Advent Calendar 2026

[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 概要

糸魚川翡翠は日本最古の翡翠文明の発祥地。しかし過度な採集による生態系への影響や、
地域ルールの認知不足が課題となっています。

本アプリは：
- 🌊 **波浪予測** — 翡翠が打ち上げられやすい日を天気データから算出
- 📍 **スポット推薦** — 採集適地をスコアリング
- 🔍 **AI画像識別** — Claude Vision で翡翠と類似石を見分け
- 🎮 **採集ゲーム** — ルールを楽しく学べるシミュレーション
- 📚 **チュートリアル** — 地域ルールと持続可能な採集方法

を通じて、**地域文化への関心と持続可能な行動**を促すナッジアプリです。

## セットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/keith-river/jade-hunter-ai.git
cd jade-hunter-ai

# 2. conda 仮想環境を作成
conda create -n jade-hunter python=3.11 -y
conda activate jade-hunter

# 3. 依存パッケージをインストール
pip install -r requirements.txt

# 4. APIキーを設定（任意）
cp .env.example .env
# .env を開いて ANTHROPIC_API_KEY を記入

# 5. アプリを起動
streamlit run jade_hunter/app.py
```

## ファイル構成

```
jade-hunter-ai/
├── jade_hunter/
│   ├── app.py              # メインエントリーポイント
│   ├── pages/
│   │   ├── home.py         # ホーム画面
│   │   ├── weather.py      # 天気・波浪予測
│   │   ├── spots.py        # スポット推薦
│   │   ├── ai_identify.py  # AI画像識別
│   │   ├── game.py         # 採集ゲーム
│   │   └── tutorial.py     # チュートリアル
│   └── utils/
│       ├── weather.py      # Open-Meteo APIラッパー
│       ├── game_engine.py  # ゲームロジック
│       ├── ai_identify.py  # Claude Vision連携
│       └── spots.py        # スポットデータ
├── docs/
│   ├── jade_hunter_demo.html   # HTMLデモ（API不要）
│   └── powerstone_oracle.html  # クリスタルオラクルボーナス
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 使用技術

- **フロントエンド**: Streamlit / HTML+JS SPA
- **気象データ**: [Open-Meteo Marine API](https://open-meteo.com/)（無料・APIキー不要）
- **AI識別**: [Anthropic Claude Vision](https://www.anthropic.com/)（要APIキー）
- **開発支援**: 生成AI（Claude）を活用した高速プロトタイピング

## Advent Calendar

[地域課題×生成AI×ナッジ実験](https://qiita.com/advent-calendar/2026/turtle-walkers)

## ライセンス

MIT License — 教育・研究目的でご自由にお使いください。
