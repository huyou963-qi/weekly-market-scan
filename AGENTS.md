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
- Output: full markdown in run output; if Post to Slack enabled, deliver per Step 12 (summary + GitHub link, 0 thread)

### Step 12 — Slack + GitHub archive (Post to Slack enabled)

See `reference/slack-delivery.md` and `templates/slack-summary.md`:

1. Write full report to `reports/week-ending-YYYY-MM-DD.md` (per `templates/weekly-report.md`)
2. `git add` → `commit` → `push` to `main` (`report: week ending YYYY-MM-DD`)
3. Post **one** Slack parent to configured channel (≤2500 chars): summary + Quick levels + vs last week + GitHub blob URL:
   `https://github.com/huyou963-qi/weekly-market-scan/blob/main/reports/week-ending-YYYY-MM-DD.md`
4. **Do not** post thread replies
5. Always keep complete Markdown in run output
6. If push fails: note in Slack that full report is in Run output only; do not post a broken link

### Templates

See `templates/weekly-report.md` for structure.
