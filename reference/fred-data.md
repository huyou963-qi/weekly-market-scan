# FRED Data — API & MCP

Mandatory for **HY OAS** and **10Y-2Y spread**. Use FRED first; web search only as fallback.

## API key (never commit)

Store the key in **one** of these places:

| Location | Use case |
|----------|----------|
| `FRED_API_KEY` env var | Local runs, `scripts/fetch_fred.py` |
| Cursor **Settings → MCP → env** | Agent + Automation sessions |
| Automation Cloud secrets | Scheduled automations |

Do **not** paste API keys into `SKILL.md`, reports, or git-tracked files.

---

## Mandatory series

| Field | FRED ID | Notes |
|-------|---------|-------|
| **HY OAS** | `BAMLH0A0HYM2` | ICE BofA US HY Master II OAS, daily, % |
| **10Y-2Y spread** | `T10Y2Y` | Fed precomputed curve spread, % |
| UST 2Y (context) | `DGS2` | Validate vs T10Y2Y |
| UST 10Y (context) | `DGS10` | Cross-asset dashboard |
| IG OAS (optional) | `BAMLC0A0CM` | Credit context vs HY |

**Units**: FRED returns **percent** (3.25 = 325bp). Report as **bp** for 1W changes using `Δ × 100`.

**HY OAS lag**: Daily close; week ending Friday uses last business day ≤ Friday.

---

## Fetch priority (agent workflow)

```
1. FRED MCP (if connected)     → get_observations / fred_get_series
2. scripts/fetch_fred.py       → python scripts/fetch_fred.py --json
3. FRED REST API (curl)        → last resort, same series IDs
4. Web / ETF proxy (HYG/LQD)   → label "proxy, not OAS"
```

### Script

From skill root:

```bash
export FRED_API_KEY=your_key_here
python scripts/fetch_fred.py --json
```

Paste `series.hy_oas` and `series.curve_10y2y` into Step 1 dashboard and Step 7 risk table.

### REST (no script)

```
GET https://api.stlouisfed.org/fred/series/observations
  ?series_id=BAMLH0A0HYM2
  &api_key=$FRED_API_KEY
  &file_type=json
  &sort_order=desc
  &limit=10
```

Repeat for `T10Y2Y`, `DGS2`, `DGS10`.

---

## MCP setup (recommended)

Add a FRED MCP server in **Cursor Settings → MCP**. Example using [fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server):

```json
{
  "mcpServers": {
    "fred": {
      "command": "npx",
      "args": ["-y", "fred-mcp-server"],
      "env": {
        "FRED_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

Alternatives: `nicoloceneda/mcp-fred`, `shanehull/fred-mcp`, `zachspar/fred-mcp` (see each repo for install).

### MCP tool calls (weekly scan)

For each mandatory series, request **last 15 observations** (covers 1W + holidays):

| Tool (varies by server) | Args |
|-------------------------|------|
| `fred_get_series` / `get_series_observations` | `series_id=BAMLH0A0HYM2`, `limit=15` |
| same | `series_id=T10Y2Y`, `limit=15` |

Compute 1W Δ: `latest.value - value_on_or_before(latest.date - 7 days)`.

### Automation MCP action

When drafting a Cursor Automation, enable the **mcp** tool with the dashboard-configured FRED server name. Prompt must say: *"Pull HY OAS and T10Y2Y from FRED MCP before writing the report."*

---

## Report fields (required when data available)

**Step 1 — Cross-asset dashboard**

| 资产 | 标的 | 1W | … |
|------|------|-----|---|
| 信用 | HY OAS (FRED) | Δbp | |
| 利率 | 10Y-2Y (FRED T10Y2Y) | Δbp | |

**Step 7 — Risk dashboard**

| 指标 | 现值 | 1W Δ | 解读 |
|------|------|------|------|
| HY OAS | X bp | ±Y bp | widening/tightening |
| 10Y-2Y | X% | ±Y bp | steepening/flattening/inverted |

**Alert thresholds** (from coverage-matrix): |HY OAS 1W| > 25bp → credit stress flag.

---

## Optional FRED macro (AI capex context)

| Series | ID | Use |
|--------|-----|-----|
| Private nonres fixed investment | `PNFI` | Broad capex cycle |
| Info processing equipment orders | `A34SNO` | Tech hardware demand proxy |

These are **monthly/quarterly** — note release lag in report.
