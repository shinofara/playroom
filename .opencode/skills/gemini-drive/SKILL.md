---
name: gemini-drive
description: Google DriveのファイルをダウンロードしてGemini 2.5 Flash Liteで処理するスキル
---

# gemini-drive

Google DriveのファイルをGemini 2.5 Flash Liteに添付して処理します。

## 使用方法

```bash
# プロンプトを直接指定
python .opencode/skills/gemini-drive/gemini_file_session.py --drive-url <Google Drive URL> --prompt "指示文"

# プロンプトファイルを使用
python .opencode/skills/gemini-drive/gemini_file_session.py --drive-url <Google Drive URL> --prompt-file <プロンプトファイル>
```

## 引数

| 引数 | 必須 | 説明 |
|------|------|------|
| `--drive-url` | はい* | Google DriveのファイルURL または ファイルID |
| `--file` | はい* | ローカルファイルパス（--drive-urlの代わりに使用可能） |
| `--prompt` | はい** | Geminiへの指示文 |
| `--prompt-file` | はい** | プロンプトを記載した外部ファイルパス |
| `--job-description` | いいえ | 募集要項ファイルパス（プロンプトに追加される） |
| `--candidate-name` | いいえ | 候補者名（出力ファイル名に使用） |
| `--output-dir` | いいえ | 評価結果の出力ディレクトリ |
| `--download-path` | いいえ | Driveからダウンロードしたファイルの保存先 |
| `--model` | いいえ | 使用するモデル名（デフォルト: gemini-2.5-flash-lite） |

\* `--drive-url` または `--file` のどちらか一方が必須
\*\* `--prompt` または `--prompt-file` のどちらか一方が必須

## 評価結果の出力

`--candidate-name` と `--output-dir` を指定すると、評価結果がMarkdownファイルとして保存されます。

- ファイル名形式: `YYYY-MM-DD_<候補者名>.md`
- 出力先: `docs/hr/reviews/` （推奨）

## プロンプトファイル

`prompts/` ディレクトリに定義済みプロンプトがあります：

| ファイル | 説明 |
|----------|------|
| `prompts/resume-review.txt` | 汎用レジュメ評価プロンプト（--job-descriptionと併用） |
| `prompts/resume-review-starley.txt` | Starley/Cotomo向けレジュメ評価プロンプト（募集要項込み） |

## 募集要項ファイル

`docs/hr/career/` ディレクトリに募集中のポジションがあります。`--job-description` オプションで指定すると、プロンプトに募集要項が追加されます。

## 対応するGoogle Drive URL形式

- `https://drive.google.com/file/d/<ID>/view`
- `https://drive.google.com/open?id=<ID>`
- `https://docs.google.com/document/d/<ID>/edit`
- `https://docs.google.com/spreadsheets/d/<ID>/edit`

## 例

### PDFを要約する

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py --drive-url "https://drive.google.com/file/d/1abc123XYZ/view" --prompt "このドキュメントを日本語で要約してください"
```

### スプレッドシートを分析する

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py --drive-url "https://docs.google.com/spreadsheets/d/1abc123XYZ/edit" --prompt "このデータの傾向を分析してください"
```

### ローカルファイルを処理する

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py --file "./document.pdf" --prompt "このドキュメントの要点を箇条書きにしてください"
```

### プロンプトファイルを使用してレジュメをレビューする

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py --drive-url "https://drive.google.com/file/d/xxx/view" --prompt-file .opencode/skills/gemini-drive/prompts/resume-review-starley.txt
```

### 募集要項を指定してレジュメをレビューする

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py \
  --drive-url "https://drive.google.com/file/d/xxx/view" \
  --prompt-file .opencode/skills/gemini-drive/prompts/resume-review.txt \
  --job-description docs/hr/career/2026-01-Senior-Product-Engineer.md
```

### 評価結果をMarkdownファイルとして保存する

```bash
python .opencode/skills/gemini-drive/gemini_file_session.py \
  --drive-url "https://drive.google.com/file/d/xxx/view" \
  --prompt-file .opencode/skills/gemini-drive/prompts/resume-review.txt \
  --job-description docs/hr/career/2026-01-Senior-Product-Engineer.md \
  --candidate-name "山田太郎" \
  --output-dir docs/hr/reviews
```

出力例: `docs/hr/reviews/2026-01-21_山田太郎.md`

## 必要な環境変数

- `GEMINI_API_KEY` または `GOOGLE_API_KEY`: Gemini APIキー

## 依存関係

`requirements.txt` に記載されたパッケージをインストールしてください：

```bash
pip install -r .opencode/skills/gemini-drive/requirements.txt
```
