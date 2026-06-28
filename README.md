# Weekly Market Scan

Cursor Cloud Automation project for the `weekly-market-scan` agent skill.

Scheduled: **Every Sunday 20:00 Beijing time** (Cloud Agent).

## Cloud secrets (Cursor dashboard)

Set before first run:

- `FRED_API_KEY` — HY OAS (`BAMLH0A0HYM2`) and 10Y-2Y (`T10Y2Y`)

## Local test

```bash
export FRED_API_KEY=your_key
python scripts/fetch_fred.py --json
```
