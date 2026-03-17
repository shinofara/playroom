#!/usr/bin/env python3
"""s3000 Slackチャンネルからメッセージを取得するスクリプト"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Tuple
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://slack.com/api"
DEFAULT_CHANNEL_ID = "C08BB9WKXEV"


def _api_get(method: str, token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Slack APIにGETリクエストを送信（レートリミット対応）"""
    url = f"{API_BASE}/{method}?{urlencode(params)}"
    request = Request(url, headers={"Authorization": f"Bearer {token}"})

    for _ in range(5):
        try:
            with urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code != 429:
                raise
            retry_after = error.headers.get("Retry-After", "1")
            time.sleep(int(retry_after))

    raise RuntimeError(f"Slack API {method} がレートリミットに繰り返し到達")


def _api_paginated(
    method: str, token: str, params: Dict[str, Any], key: str
) -> Iterable[Dict[str, Any]]:
    """ページネーション対応のSlack APIリクエスト"""
    cursor = ""
    while True:
        payload = dict(params)
        if cursor:
            payload["cursor"] = cursor

        data = _api_get(method, token, payload)
        if not data.get("ok"):
            raise RuntimeError(
                f"Slack API {method} 失敗: {data.get('error', 'unknown_error')}"
            )

        for item in data.get(key, []):
            yield item

        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            return


def _resolve_thread_replies(
    token: str, channel_id: str, thread_ts: str
) -> List[Dict[str, Any]]:
    """スレッドの返信を取得"""
    replies = list(
        _api_paginated(
            "conversations.replies",
            token,
            {"channel": channel_id, "ts": thread_ts, "limit": 200},
            "messages",
        )
    )
    # 親メッセージを除外して返信のみ返す
    return [r for r in replies if r["ts"] != thread_ts]


def _target_range(target_date: str | None, days: int = 1) -> Tuple[datetime, datetime]:
    """取得対象の日付範囲を計算"""
    if target_date:
        day = datetime.strptime(target_date, "%Y-%m-%d")
    else:
        now = datetime.now()
        day = (now - timedelta(days=days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=days)
    return start, end


def _format_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """メッセージを整形して返す"""
    ts = float(message["ts"])
    return {
        "ts": message["ts"],
        "datetime": datetime.fromtimestamp(ts).isoformat(timespec="seconds"),
        "user": message.get("user", ""),
        "text": message.get("text", ""),
        "thread_ts": message.get("thread_ts"),
        "reply_count": message.get("reply_count", 0),
        "subtype": message.get("subtype"),
    }


def fetch_channel_messages(
    token: str,
    channel_id: str,
    start: datetime,
    end: datetime,
    include_threads: bool = False,
) -> Dict[str, Any]:
    """指定チャンネルからメッセージを取得"""
    oldest = f"{start.timestamp():.6f}"
    latest = f"{end.timestamp():.6f}"

    messages_raw = list(
        _api_paginated(
            "conversations.history",
            token,
            {
                "channel": channel_id,
                "oldest": oldest,
                "latest": latest,
                "inclusive": "true",
                "limit": 200,
            },
            "messages",
        )
    )

    messages = []
    for msg in messages_raw:
        formatted = _format_message(msg)

        if include_threads and msg.get("reply_count", 0) > 0:
            replies_raw = _resolve_thread_replies(token, channel_id, msg["ts"])
            formatted["replies"] = [_format_message(r) for r in replies_raw]

        messages.append(formatted)

    messages.sort(key=lambda m: float(m["ts"]))

    return {
        "channel_id": channel_id,
        "period_start": start.isoformat(timespec="seconds"),
        "period_end": end.isoformat(timespec="seconds"),
        "total_messages": len(messages),
        "messages": messages,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="s3000 Slackチャンネルからメッセージを取得"
    )
    parser.add_argument(
        "--channel",
        default=DEFAULT_CHANNEL_ID,
        help=f"チャンネルID (デフォルト: {DEFAULT_CHANNEL_ID})",
    )
    parser.add_argument(
        "--date", help="対象日 YYYY-MM-DD (デフォルト: 昨日)"
    )
    parser.add_argument(
        "--days", type=int, default=1, help="取得日数 (デフォルト: 1)"
    )
    parser.add_argument(
        "--threads", action="store_true", help="スレッドの返信も取得"
    )
    parser.add_argument(
        "--token-env",
        default="SLACK_USER_TOKEN",
        help="Slackトークンの環境変数名 (デフォルト: SLACK_USER_TOKEN)",
    )
    parser.add_argument(
        "--pretty", action="store_true", help="JSON整形出力"
    )
    args = parser.parse_args()

    token = os.getenv(args.token_env)
    if not token:
        print(
            f"エラー: 環境変数 {args.token_env} が設定されていません",
            file=sys.stderr,
        )
        return 2

    try:
        start, end = _target_range(args.date, args.days)
        result = fetch_channel_messages(
            token, args.channel, start, end, include_threads=args.threads
        )
    except Exception as error:
        print(f"エラー: {error}", file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
