#!/usr/bin/env python3
"""Push weekly scan to WeChat Official Account (微信公众号) draft or publish.

Requires enterprise-verified account for auto-publish (freepublish) since 2025-07.

Env:
  WECHAT_MP_APPID
  WECHAT_MP_SECRET
  WECHAT_MP_PUBLISH=0|1   (default 0 = draft only)

Usage:
  python scripts/push_wechat_mp.py --title "周度市场检测 06-26" \\
    --digest "摘要128字内" --file article.html
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def _get_token(appid: str, secret: str) -> str:
    url = (
        "https://api.weixin.qq.com/cgi-bin/token?"
        + urllib.parse.urlencode(
            {"grant_type": "client_credential", "appid": appid, "secret": secret}
        )
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)
    if "access_token" not in data:
        raise RuntimeError(f"token error: {data}")
    return data["access_token"]


def _post(url: str, body: dict) -> dict:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def _text_to_html(text: str) -> str:
    """Minimal plain/markdown-ish → WeChat-safe HTML (no external images)."""
    lines = text.strip().splitlines()
    parts: list[str] = []
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("【") and line.endswith("】"):
            parts.append(f"<h2>{line}</h2>")
        elif line.startswith("• ") or line.startswith("- "):
            parts.append(f"<p>{line[2:]}</p>")
        elif line.startswith("━━"):
            parts.append("<hr/>")
        else:
            parts.append(f"<p>{line}</p>")
    html = "\n".join(parts)
    # strip markdown bold
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    return html


def add_draft(token: str, title: str, digest: str, content_html: str, author: str = "") -> str:
    if len(title) > 32:
        title = title[:32]
    if len(digest) > 128:
        digest = digest[:128]
    article = {
        "title": title,
        "author": author[:16] if author else "",
        "digest": digest,
        "content": content_html,
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    result = _post(url, {"articles": [article]})
    if "media_id" not in result:
        raise RuntimeError(f"draft/add failed: {result}")
    return result["media_id"]


def publish_draft(token: str, media_id: str) -> dict:
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
    return _post(url, {"media_id": media_id})


def main() -> None:
    parser = argparse.ArgumentParser(description="Push report to 微信公众号")
    parser.add_argument("--title", required=True, help="≤32 chars")
    parser.add_argument("--digest", required=True, help="≤128 chars, card summary")
    parser.add_argument("--author", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--file", help="HTML or plain text file (UTF-8)")
    parser.add_argument("--html", action="store_true", help="File is already HTML")
    args = parser.parse_args()

    appid = os.environ.get("WECHAT_MP_APPID", "").strip()
    secret = os.environ.get("WECHAT_MP_SECRET", "").strip()
    do_publish = os.environ.get("WECHAT_MP_PUBLISH", "0").strip() == "1"

    if not appid or not secret:
        print("Error: WECHAT_MP_APPID and WECHAT_MP_SECRET required", file=sys.stderr)
        sys.exit(1)

    body = args.content
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            body = f.read()
    if not body.strip():
        print("Error: empty content", file=sys.stderr)
        sys.exit(1)

    content_html = body if args.html else _text_to_html(body)
    token = _get_token(appid, secret)
    media_id = add_draft(token, args.title, args.digest, content_html, args.author)
    print(f"Draft OK media_id={media_id}")

    if do_publish:
        pub = publish_draft(token, media_id)
        if pub.get("errcode", 0) not in (0, None) and "publish_id" not in pub:
            raise RuntimeError(f"freepublish/submit failed: {pub}")
        print(f"Publish submitted: {pub}")
    else:
        print("Draft only (WECHAT_MP_PUBLISH=0). Review at mp.weixin.qq.com → 草稿箱")


if __name__ == "__main__":
    main()
