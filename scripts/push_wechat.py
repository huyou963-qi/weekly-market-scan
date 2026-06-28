#!/usr/bin/env python3
"""Push weekly scan text to WeChat via PushPlus or 企业微信群机器人.

Usage:
  export PUSHPLUS_TOKEN=xxx
  python scripts/push_wechat.py --title "周报摘要" --content "正文..."

  export WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
  python scripts/push_wechat.py --channel qywx --title "周报" --file body.txt
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def push_pushplus(token: str, title: str, content: str) -> None:
    payload = json.dumps(
        {
            "token": token,
            "title": title,
            "content": content,
            "template": "markdown",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://www.pushplus.plus/send",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.load(resp)
    if result.get("code") != 200:
        raise RuntimeError(f"PushPlus error: {result}")
    print(f"PushPlus OK: {result.get('msg', 'sent')}")


def push_qywx(webhook_url: str, title: str, content: str) -> None:
    # Enterprise WeChat markdown: title as header line
    md = f"## {title}\n\n{content}"
    if len(md.encode("utf-8")) > 4096:
        md = md[:3500] + "\n\n...(内容过长已截断，请查看完整版)"
    payload = json.dumps({"msgtype": "markdown", "markdown": {"content": md}}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.load(resp)
    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"企业微信 error: {result}")
    print("企业微信 webhook OK")


def main() -> None:
    parser = argparse.ArgumentParser(description="Push report to WeChat")
    parser.add_argument("--channel", choices=["pushplus", "qywx"], default="pushplus")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", default="")
    parser.add_argument("--file", help="Read body from file (UTF-8)")
    args = parser.parse_args()

    content = args.content
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            content = f.read()
    if not content.strip():
        print("Error: empty content", file=sys.stderr)
        sys.exit(1)

    if args.channel == "pushplus":
        token = os.environ.get("PUSHPLUS_TOKEN", "").strip()
        if not token:
            print("Error: PUSHPLUS_TOKEN not set", file=sys.stderr)
            sys.exit(1)
        push_pushplus(token, args.title, content)
    else:
        url = os.environ.get("WECHAT_WEBHOOK_URL", "").strip()
        if not url:
            print("Error: WECHAT_WEBHOOK_URL not set", file=sys.stderr)
            sys.exit(1)
        push_qywx(url, args.title, content)


if __name__ == "__main__":
    main()
