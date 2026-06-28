#!/usr/bin/env python3
"""Fetch mandatory FRED series for weekly-market-scan.

Reads FRED_API_KEY from environment. Never hardcode keys in this repo.

Usage:
  export FRED_API_KEY=your_key
  python scripts/fetch_fred.py
  python scripts/fetch_fred.py --weeks 2 --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any

# Mandatory series for weekly scan
SERIES = {
    "hy_oas": {
        "id": "BAMLH0A0HYM2",
        "label": "ICE BofA US HY OAS",
        "units": "percent (1 pt = 100bp)",
    },
    "curve_10y2y": {
        "id": "T10Y2Y",
        "label": "10Y-2Y Treasury spread",
        "units": "percent",
    },
    "ust_2y": {
        "id": "DGS2",
        "label": "UST 2Y constant maturity",
        "units": "percent",
    },
    "ust_10y": {
        "id": "DGS10",
        "label": "UST 10Y constant maturity",
        "units": "percent",
    },
    "ig_oas": {
        "id": "BAMLC0A0CM",
        "label": "ICE BofA US IG OAS (optional context)",
        "units": "percent",
        "optional": True,
    },
}

FRED_OBS_URL = "https://api.stlouisfed.org/fred/series/observations"


def _get_api_key() -> str:
    key = os.environ.get("FRED_API_KEY", "").strip()
    if not key:
        print(
            "Error: FRED_API_KEY not set.\n"
            "Set env var or add to Cursor MCP server env (see reference/fred-data.md).",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def fetch_observations(
    series_id: str,
    api_key: str,
    *,
    limit: int = 30,
) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": str(limit),
        }
    )
    url = f"{FRED_OBS_URL}?{params}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"FRED HTTP {exc.code} for {series_id}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"FRED network error for {series_id}: {exc}") from exc

    rows = payload.get("observations", [])
    return [r for r in rows if r.get("value") not in (".", "", None)]


def _to_float(value: str) -> float:
    return float(value)


def _pick_on_or_before(obs: list[dict[str, str]], target: datetime) -> dict[str, str] | None:
    target_s = target.strftime("%Y-%m-%d")
    for row in obs:
        if row["date"] <= target_s:
            return row
    return obs[-1] if obs else None


def summarize_series(
    key: str,
    meta: dict[str, Any],
    obs: list[dict[str, str]],
) -> dict[str, Any]:
    if not obs:
        return {"key": key, "error": "no observations", **meta}

    latest = obs[0]
    latest_dt = datetime.strptime(latest["date"], "%Y-%m-%d")
    week_ago = _pick_on_or_before(obs, latest_dt - timedelta(days=7))
    month_ago = _pick_on_or_before(obs, latest_dt - timedelta(days=30))

    latest_v = _to_float(latest["value"])
    w1_v = _to_float(week_ago["value"]) if week_ago else latest_v
    m1_v = _to_float(month_ago["value"]) if month_ago else latest_v

    return {
        "key": key,
        "series_id": meta["id"],
        "label": meta["label"],
        "units": meta["units"],
        "as_of": latest["date"],
        "value": latest_v,
        "change_1w": round(latest_v - w1_v, 4),
        "change_1w_bps": round((latest_v - w1_v) * 100, 1),
        "change_1m": round(latest_v - m1_v, 4),
        "change_1m_bps": round((latest_v - m1_v) * 100, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch FRED data for weekly market scan")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    parser.add_argument("--weeks", type=int, default=1, help="Reserved for future use")
    args = parser.parse_args()

    api_key = _get_api_key()
    results: dict[str, Any] = {
        "fetched_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "series": {},
    }

    for key, meta in SERIES.items():
        try:
            obs = fetch_observations(meta["id"], api_key)
            results["series"][key] = summarize_series(key, meta, obs)
        except RuntimeError as exc:
            if meta.get("optional"):
                results["series"][key] = {"key": key, "error": str(exc), **meta}
            else:
                print(f"Error: {exc}", file=sys.stderr)
                sys.exit(2)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"FRED snapshot (UTC {results['fetched_at']})\n")
    for key, row in results["series"].items():
        if "error" in row:
            print(f"- {row.get('label', key)}: ERROR — {row['error']}")
            continue
        print(
            f"- {row['label']} ({row['series_id']})"
            f"\n  as_of={row['as_of']}  value={row['value']}"
            f"  1W={row['change_1w_bps']:+.1f}bp  1M={row['change_1m_bps']:+.1f}bp"
        )


if __name__ == "__main__":
    main()
