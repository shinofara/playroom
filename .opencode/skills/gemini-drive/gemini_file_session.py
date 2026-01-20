#!/usr/bin/env python3
"""
Gemini 2.5 Flash Liteでファイルを添付してセッションを開始する

使用方法:
    python gemini_file_session.py --file <ローカルファイル> --prompt "指示文"
    python gemini_file_session.py --drive-url <Google Drive URL> --prompt "指示文"
    python gemini_file_session.py --drive-url <Google Drive URL> --prompt-file <プロンプトファイル>
    python gemini_file_session.py --drive-url <Google Drive URL> --prompt-file <プロンプトファイル> --job-description <募集要項ファイル>
    python gemini_file_session.py --drive-url <Google Drive URL> --prompt-file <プロンプトファイル> --candidate-name "山田太郎" --output-dir docs/hr/reviews

環境変数:
    GEMINI_API_KEY または GOOGLE_API_KEY
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

# プロジェクトルートの.envを読み込む
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

from download_from_drive import authenticate, download_file, parse_drive_file_id

try:
    import google.generativeai as genai
except ImportError as exc:  # pragma: no cover - 実行環境依存
    print("google-generativeai が見つかりません。requirements.txt を参照してください。")
    raise SystemExit(1) from exc


DEFAULT_MODEL = "gemini-2.5-flash-lite"


def get_api_key() -> str:
    """APIキーを取得する"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY または GOOGLE_API_KEY を設定してください")
    return api_key


def resolve_input_file(args: argparse.Namespace) -> Path:
    """入力ファイルを解決する"""
    if args.file_path:
        file_path = Path(args.file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"ファイルが存在しません: {file_path}")
        return file_path

    if args.drive_url:
        file_id = parse_drive_file_id(args.drive_url)
        service = authenticate()
        downloaded_path = download_file(service, file_id, args.download_path)
        return Path(downloaded_path)

    raise ValueError("--file または --drive-url のどちらかを指定してください")


def run_session(file_path: Path, prompt: str, model_name: str) -> str:
    """Geminiにファイルを添付して応答を得る"""
    genai.configure(api_key=get_api_key())
    model = genai.GenerativeModel(model_name)
    uploaded_file = genai.upload_file(str(file_path))
    response = model.generate_content([uploaded_file, prompt])
    return response.text


def resolve_prompt(args: argparse.Namespace) -> str:
    """プロンプトを解決する（直接指定またはファイルから読み込み）"""
    base_prompt = ""

    if args.prompt:
        base_prompt = args.prompt
    elif args.prompt_file:
        prompt_path = Path(args.prompt_file)
        if not prompt_path.exists():
            raise FileNotFoundError(f"プロンプトファイルが存在しません: {prompt_path}")
        base_prompt = prompt_path.read_text(encoding="utf-8").strip()
    else:
        raise ValueError("--prompt または --prompt-file のどちらかを指定してください")

    # 募集要項ファイルが指定されている場合、プロンプトに追加
    if args.job_description:
        jd_path = Path(args.job_description)
        if not jd_path.exists():
            raise FileNotFoundError(f"募集要項ファイルが存在しません: {jd_path}")
        jd_content = jd_path.read_text(encoding="utf-8").strip()
        base_prompt = f"{base_prompt}\n\n【募集要項】\n{jd_content}"

    return base_prompt


def save_output(content: str, candidate_name: str, output_dir: Path, job_description: str | None = None) -> Path:
    """評価結果をMarkdownファイルとして保存する"""
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    # ファイル名に使えない文字を置換
    safe_name = candidate_name.replace("/", "_").replace("\\", "_").replace(" ", "_")
    filename = f"{today}_{safe_name}.md"
    output_path = output_dir / filename

    # メタ情報をヘッダーとして追加
    header_lines = [
        "---",
        f"candidate: {candidate_name}",
        f"evaluation_date: {today}",
    ]
    if job_description:
        header_lines.append(f"job_description: {job_description}")
    header_lines.append("---")
    header_lines.append("")

    full_content = "\n".join(header_lines) + content

    output_path.write_text(full_content, encoding="utf-8")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gemini 2.5 Flash Liteセッション起動")
    parser.add_argument("--file", dest="file_path", help="ローカルファイルパス")
    parser.add_argument("--drive-url", dest="drive_url", help="Google DriveのURLまたはID")
    parser.add_argument("--download-path", help="Driveからの保存先パス")
    parser.add_argument("--prompt", help="Geminiへの指示文")
    parser.add_argument("--prompt-file", dest="prompt_file", help="プロンプトを記載した外部ファイルパス")
    parser.add_argument("--job-description", dest="job_description", help="募集要項ファイルパス（プロンプトに追加）")
    parser.add_argument("--candidate-name", dest="candidate_name", help="候補者名（出力ファイル名に使用）")
    parser.add_argument("--output-dir", dest="output_dir", help="評価結果の出力ディレクトリ")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="利用するモデル名")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        file_path = resolve_input_file(args)
        prompt = resolve_prompt(args)
        response_text = run_session(file_path, prompt, args.model)
    except (ValueError, FileNotFoundError) as exc:
        print(f"入力エラー: {exc}")
        raise SystemExit(1) from exc

    # 出力ディレクトリと候補者名が指定されている場合、ファイルに保存
    if args.output_dir and args.candidate_name:
        output_dir = Path(args.output_dir)
        output_path = save_output(
            response_text,
            args.candidate_name,
            output_dir,
            args.job_description
        )
        print(f"評価結果を保存しました: {output_path}")
    elif args.output_dir and not args.candidate_name:
        print("警告: --output-dir が指定されていますが --candidate-name がありません。ファイル保存をスキップします。")
        print(response_text)
    else:
        print(response_text)


if __name__ == "__main__":
    main()
