#!/usr/bin/env python3
"""
Google Driveからファイルをダウンロードするスクリプト

使用方法:
    python download_from_drive.py <ファイルIDまたはURL> [出力ファイル名]

例:
    python download_from_drive.py 1abc123XYZ output.pdf
    python download_from_drive.py https://drive.google.com/file/d/1abc123XYZ/view
    python download_from_drive.py 1abc123XYZ  # 元のファイル名で保存
"""

import io
import os
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Google Drive APIのスコープ（読み取り専用）
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# 認証情報ファイルのパス
CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
TOKEN_FILE = Path(__file__).parent / "token.json"


def parse_drive_file_id(value: str) -> str:
    """
    Google DriveのURLまたはファイルIDからファイルIDを抽出する

    Args:
        value: Google DriveのURLまたはファイルID

    Returns:
        str: 抽出したファイルID

    Raises:
        ValueError: URLからファイルIDを抽出できない場合
    """
    patterns = [
        r"https?://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"https?://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
        r"https?://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)",
        r"https?://drive\.google\.com/uc\?export=download&id=([a-zA-Z0-9_-]+)",
        r"https?://docs\.google\.com/.*/d/([a-zA-Z0-9_-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)

    if value.startswith(("http://", "https://")):
        raise ValueError("Google DriveのURLからファイルIDを抽出できませんでした")

    return value


def authenticate():
    """
    Google Drive APIへの認証を行い、認証済みのサービスを返す

    Returns:
        googleapiclient.discovery.Resource: 認証済みのDriveサービス
    """
    creds = None

    # 保存済みのトークンがあれば読み込む
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # 有効な認証情報がない場合は認証フローを実行
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("トークンを更新しています...")
            creds.refresh(Request())
        else:
            print("ブラウザで認証を行ってください...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # トークンを保存
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        print("認証情報を保存しました")

    return build("drive", "v3", credentials=creds)


def get_file_metadata(service, file_id: str) -> dict:
    """
    ファイルのメタデータを取得する

    Args:
        service: Drive APIサービス
        file_id: ダウンロードするファイルのID

    Returns:
        dict: ファイルのメタデータ
    """
    return service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, size"
    ).execute()


def download_file(service, file_id: str, output_path: str = None) -> str:
    """
    Google Driveからファイルをダウンロードする

    Args:
        service: Drive APIサービス
        file_id: ダウンロードするファイルのID
        output_path: 保存先のファイルパス（省略時は元のファイル名を使用）

    Returns:
        str: ダウンロードしたファイルのパス
    """
    # ファイルのメタデータを取得
    metadata = get_file_metadata(service, file_id)
    file_name = metadata.get("name", "downloaded_file")
    mime_type = metadata.get("mimeType", "")

    print(f"ファイル名: {file_name}")
    print(f"MIMEタイプ: {mime_type}")

    # 出力パスが指定されていなければ元のファイル名を使用
    if output_path is None:
        output_path = file_name

    # Google DocsなどのGoogle形式のファイルはエクスポートが必要
    google_mime_types = {
        "application/vnd.google-apps.document": (
            "application/pdf", ".pdf"
        ),
        "application/vnd.google-apps.spreadsheet": (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xlsx"
        ),
        "application/vnd.google-apps.presentation": (
            "application/pdf", ".pdf"
        ),
    }

    if mime_type in google_mime_types:
        export_mime, extension = google_mime_types[mime_type]
        print(f"Google形式のファイルを {export_mime} としてエクスポートします...")

        # 出力ファイル名に拡張子がなければ追加
        if not Path(output_path).suffix:
            output_path = output_path + extension

        request = service.files().export_media(
            fileId=file_id,
            mimeType=export_mime
        )
    else:
        # 通常のファイルをダウンロード
        request = service.files().get_media(fileId=file_id)

    # ダウンロード実行
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"ダウンロード中... {int(status.progress() * 100)}%")

    # ファイルに保存
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())

    print(f"ダウンロード完了: {output_path}")
    return output_path


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python download_from_drive.py <ファイルIDまたはURL> [出力ファイル名]")
        print("\nファイルIDはGoogle DriveのURLから取得できます:")
        print("  https://drive.google.com/file/d/<ファイルID>/view")
        sys.exit(1)

    raw_input = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        file_id = parse_drive_file_id(raw_input)
    except ValueError as exc:
        print(f"入力エラー: {exc}")
        sys.exit(1)

    print(f"ファイルID: {file_id}")

    # 認証
    service = authenticate()

    # ダウンロード
    download_file(service, file_id, output_path)


if __name__ == "__main__":
    main()
