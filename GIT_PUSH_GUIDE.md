# GitHub への push 手順

## 前提

- Git がインストール済み（`git --version` で確認）
- GitHub アカウントで `keith-river/jade-hunter-ai` リポジトリを作成済み
- SSH キーまたは GitHub CLI (`gh`) で認証済み

---

## 手順

### 1. ファイルをローカルに展開

Claudeから受け取った ZIP を展開する場合：

```bash
unzip jade-hunter-ai.zip
cd jade-hunter-ai
```

### 2. Git を初期化

```bash
git init
git branch -M main
```

### 3. リモートを設定

```bash
# SSH を使う場合（推奨）
git remote add origin git@github.com:keith-river/jade-hunter-ai.git

# HTTPS を使う場合
git remote add origin https://github.com/keith-river/jade-hunter-ai.git
```

リモートの確認：
```bash
git remote -v
```

### 4. .env ファイルが除外されていることを確認

```bash
cat .gitignore    # .env が含まれていることを確認
ls -la            # .env ファイルが存在する場合は絶対にステージしない
```

### 5. 全ファイルをステージ

```bash
git add .
git status        # ステージされたファイルを確認（.env が含まれていないこと！）
```

### 6. コミット

```bash
git commit -m "feat: 翡翠ハンターAI 初回リリース

- Streamlit多ページアプリ（天気予測・スポット推薦・AI識別・ゲーム・チュートリアル）
- Open-Meteo Marine APIによる波浪データ取得
- Claude Vision APIによる石の識別（デモモードあり）
- HTML+JS SPAデモ（APIキー不要）
- クリスタルオラクルボーナスアプリ

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

### 7. GitHub に push

```bash
git push -u origin main
```

初回 push 後は `git push` だけで OK。

---

## GitHub Pages の有効化（HTMLデモを公開する場合）

1. GitHub リポジトリの **Settings** タブを開く
2. 左メニューの **Pages** をクリック
3. Source: **Deploy from a branch**
4. Branch: **main** / folder: **/ docs**
5. Save をクリック

数分後に `https://keith-river.github.io/jade-hunter-ai/` でデモが公開されます。

Qiita 記事の「公開URL」にこのアドレスを記載してください。

---

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `Permission denied (publickey)` | SSH キー未設定 | `ssh-keygen` → GitHubに公開鍵を登録 |
| `remote: Repository not found` | リポジトリURLが間違い | `git remote -v` で確認・修正 |
| `Updates were rejected` | リモートに先行コミットあり | `git pull --rebase origin main` → 再push |
| `nothing to commit` | ファイルが既にコミット済み | `git status` で確認 |

---

## セキュリティチェックリスト

push 前に必ず確認：

- [ ] `.env` が `.gitignore` に含まれている
- [ ] `git status` に `.env` が表示されない
- [ ] `requirements.txt` にバージョンが明記されている
- [ ] `README.md` にセットアップ手順が書かれている
