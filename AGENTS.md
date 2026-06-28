# Weekly Market Scan — Cloud Automation

When this automation runs, produce a **trader-grade weekly market brief** for the prior US trading week (Mon–Fri). Label "Week ending [Friday date]". Language: 中文正文，关键术语保留英文.

## Mandatory workflow (Steps 0–11)

Read `.cursor/skills/weekly-market-scan/SKILL.md` if present; otherwise follow this file.

### Step 1a — FRED (mandatory before credit/curve fields)

Use `FRED_API_KEY` from Cloud secrets.

```
GET https://api.stlouisfed.org/fred/series/observations?series_id=SERIES&api_key=$FRED_API_KEY&file_type=json&sort_order=desc&limit=15
```

Series: `BAMLH0A0HYM2` (HY OAS), `T10Y2Y` (10Y-2Y), `DGS2`, `DGS10`. Report level + 1W Δ in bp. Never fabricate; proxy only if FRED fails.

### Step 4.5 — AI supply chain

HBM/DRAM, cloud GPU $/hr, AI API $/1M tokens, hyperscaler capex (MSFT/GOOGL/AMZN/META). Compare vs last run (memory).

### Report sections (all required)

1. Executive summary (5 bullets)
2. Cross-asset dashboard (FRED HY OAS + T10Y2Y)
3. Macro recap + next-week calendar (H/M/L)
4. Equity structure (breadth, factors, cap tier)
5. GICS sector rotation + sub-industry
6. AI supply chain + synthesis
7. Event impact matrix (2nd-order effects)
8. Watchlist + systemic names (|1W|>3%)
9. Risk dashboard (VIX, FRED credit/curve)
10. Regime + falsifiers + vs last week
11. Anomalies / divergences
12. Next-week playbook (scenarios + ≤3 setups + invalidation)

### Quality

- As-of date + source on every number
- Label 事实 / 解读 / 判断
- Output: full markdown report in run output only — no Slack/WeChat

### Templates

See `templates/weekly-report.md` for structure.
