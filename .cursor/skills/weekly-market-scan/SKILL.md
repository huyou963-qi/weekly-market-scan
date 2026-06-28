---
name: weekly-market-scan
description: >-
  Professional weekly cross-asset market scan for traders: major asset classes,
  equity sector/industry structure, macro calendar, key events, watchlist impact,
  risk regime, FRED-backed credit/curve data (HY OAS, 10Y-2Y), AI supply chain
  (HBM, GPU cloud rental, API pricing, hyperscaler capex), and actionable
  next-week views. Use when building or running a weekly market check, market
  wrap, regime review, sector rotation report, or Cursor Automation for scheduled
  market monitoring (周度市场检测, 周报, 大类资产, 行业结构, 重点事件, FRED, HBM, AI capex).
disable-model-invocation: true
---

# Weekly Market Scan

Produce a **trader-grade weekly market brief**: what moved, why it matters, what changed in structure, and what to watch next week. Separate **facts** (with date/source), **interpretation**, and **actionable views**.

This skill has two modes:

| Mode | When | Output |
|------|------|--------|
| `scan` | User asks for this week's market review | [weekly-report.md](templates/weekly-report.md) |
| `scan-wechat` | User wants WeChat-readable format or push | [wechat-report.md](templates/wechat-report.md) — see [wechat-delivery.md](reference/wechat-delivery.md) |
| `automation` | User wants a Cursor Automation for weekly runs | Draft via **automate** skill + [automation-prompt.md](templates/automation-prompt.md) |

Default market scope: **global macro + US equities** unless the user specifies A-share / HK / Europe-only focus.

---

## Scan workflow (checklist)

Copy and track progress:

```
Weekly Scan Progress:
- [ ] 0. Scope & period anchor
- [ ] 1a. FRED pull (HY OAS + 10Y-2Y) — MCP or scripts/fetch_fred.py
- [ ] 1. Cross-asset dashboard
- [ ] 2. Macro & policy recap
- [ ] 3. Equity market structure
- [ ] 4. Sector & industry rotation
- [ ] 4.5. AI supply chain (HBM, cloud GPU, API pricing, capex)
- [ ] 5. Key events & catalyst map
- [ ] 6. Watchlist & systemic names
- [ ] 7. Risk & liquidity dashboard
- [ ] 8. Regime & cross-asset signals
- [ ] 9. Anomalies & divergences
- [ ] 10. Next-week playbook
- [ ] 11. Quality gate
```

### Step 0 — Scope & period anchor

- **Period**: prior trading week (Mon open → Fri close) in user's timezone; if run on weekend, label "week ending [date]".
- **Benchmarks**: S&P 500, Nasdaq, Russell 2000 (or user-specified).
- **Universe extras**: user watchlist, index top weights, names with >5% weekly move or >2σ volume.
- **Prior week carry-over**: if memory or last report exists, note unresolved themes (e.g. "rate-cut repricing still in progress").

### Step 1a — FRED data pull (mandatory)

Fetch **before** filling credit/curve fields. Full spec: [fred-data.md](reference/fred-data.md).

**Priority**: FRED MCP → `python scripts/fetch_fred.py --json` → FRED REST → proxy (label as proxy).

| Series | FRED ID | Report as |
|--------|---------|-----------|
| HY OAS | `BAMLH0A0HYM2` | level (bp) + 1W Δ (bp) |
| 10Y-2Y spread | `T10Y2Y` | level (%) + 1W Δ (bp) |
| UST 2Y / 10Y | `DGS2` / `DGS10` | context in Step 1 |

**API key**: `FRED_API_KEY` env or MCP server env — never hardcode in skill files or reports.

If FRED unavailable after all paths: write `FRED 未连接` and use HYG/LQD ETF spread as **proxy only**.

### Step 1 — Cross-asset dashboard

Cover each bucket with **1W change**, **MTD**, **vs 52W range**, and **one-line driver**:

| Bucket | Minimum instruments |
|--------|---------------------|
| Equities | SPX, NDX, RUT; optional CSI300/HSI/STOXX/N225 |
| Rates | UST 2Y/10Y, **10Y-2Y (FRED `T10Y2Y`)**, real yields |
| Credit | **HY OAS (FRED `BAMLH0A0HYM2`)**, IG OAS optional, financial conditions index |
| FX | DXY; EUR, JPY, CNY if relevant |
| Commodities | WTI/Brent, Gold, Copper, Nat Gas |
| Vol / risk | VIX, VVIX or term structure note, MOVE (bond vol) |
| Crypto (risk proxy) | BTC, ETH — only as sentiment/liquidity overlay |

Full instrument list: [coverage-matrix.md](reference/coverage-matrix.md).

### Step 2 — Macro & policy recap

**Past week (what happened):**
- Major data prints vs consensus (CPI, PPI, payrolls, PMI, retail, GDP revision)
- Central bank speakers & market reaction
- Fiscal / regulatory headlines
- Geopolitics with market transmission (energy, supply chain, sanctions)

**Next week (forward calendar):**
- Tier-1/2 economic releases with consensus if available
- FOMC/ECB/PBoC meetings, minutes, dot plot, QT details
- Earnings: megacap + sectors with heavy reporting
- Index rebalances, options expiry (OPEX), lock-ups, dividend ex-dates

Tag each item: **High / Medium / Low** market impact.

### Step 3 — Equity market structure

Not just index level — **how** the market traded:

- **Breadth**: advance/decline, new highs/lows, % stocks above 50/200 DMA
- **Leadership**: cap tier (mega vs mid vs small), growth vs value, quality vs junk
- **Factor tilts**: momentum, low vol, dividend — what worked / failed
- **Index composition effect**: top-10 contribution to index return
- **Volatility regime**: realized vs implied, up-day vs down-day vol
- **Flows** (if data available): ETF sector flows, equity fund flows, short interest trend

### Step 4 — Sector & industry rotation

Use **GICS Level 1** always; drill to **Level 2/3** where rotation is sharp.

For each sector report:
- 1W / MTD / YTD relative performance vs SPX
- **Driver tag**: rates-sensitive / commodity-linked / defensive / AI-capex / etc.
- **Sub-industry standouts**: best & worst 2–3 industries
- **Relative strength trend**: improving / deteriorating vs 4-week ago
- **Earnings revision breadth** (if accessible): upgrades vs downgrades

End with a **rotation summary table**: "Money rotating FROM → TO" with evidence.

### Step 4.5 — AI supply chain & capex tracker

Full checklist: [ai-supply-chain.md](reference/ai-supply-chain.md). Required when AI/semi/tech is a weekly driver (default: **always include**).

| Track | Metrics | Sources |
|-------|---------|---------|
| **HBM / memory** | HBM3e & DRAM price trend, supply commentary | TrendForce, DRAMeXchange, MU/SK Hynix/Samsung IR |
| **Cloud GPU rental** | $/GPU-hr (H100/H200 normalized) | AWS, GCP, Azure, CoreWeave, Lambda pricing pages |
| **Model API pricing** | $/1M tokens in/out; flag any change | OpenAI, Anthropic, Google, Bedrock/Azure OpenAI |
| **AI capex** | Hyperscaler capex & guides; NVDA DC revenue | 10-Q/calls; optional FRED `PNFI` / `A34SNO` |

Deliverables:
1. Four sub-tables (HBM, cloud, API, capex) with **1W delta vs prior report** (memory or last known)
2. **AI stack synthesis** paragraph — cost curve, capex cycle stage, margin chain, link to SOX/XLK
3. Flag anomalies: e.g. HBM up but semi stocks down; API price cut but cloud GPU flat

### Step 5 — Key events & catalyst map

Build an **event impact matrix**:

| Date | Event | Assets / sectors affected | Base case | Tail risks | Historical vol proxy |
|------|-------|---------------------------|-----------|------------|----------------------|

Include:
- Macro surprises already priced vs still debated
- Earnings: beat/miss rate by sector, guidance tone
- Idiosyncratic: M&A, FDA, antitrust, CEO change, buyback announcements
- Technical market events: OPEX, triple witching, index reconstitution

For each **high-impact event**, state **2nd-order effects** (e.g. hot CPI → rates ↑ → growth ↓ → software ↓ but banks ↑).

### Step 6 — Watchlist & systemic names

**Tier A — User watchlist** (ask if not provided; persist in automation memory).

**Tier B — Systemic / index anchors** (always cover if material move):
- Mag 7 / top index weights
- Largest weekly movers in S&P 500
- Credit-sensitive banks / REITs if spread move > threshold
- Sector ETFs representing rotation thesis (XLK, XLE, XLF, etc.)

Per name (only if |1W| > 3% or major catalyst):
- Move summary + catalyst
- Technical: trend, key levels, RS vs sector
- Fundamental hook (one line)
- **Trader view**: momentum / mean-revert / event / avoid

### Step 7 — Risk & liquidity dashboard

| Indicator | Current | 1W Δ | Signal |
|-----------|---------|------|--------|
| VIX / VIX term structure | | | contango/backwardation |
| **HY OAS (FRED `BAMLH0A0HYM2`)** | | | widening/tightening; alert if \|1W\| > 25bp |
| **10Y-2Y (FRED `T10Y2Y`)** | | | steepening/flattening/inversion |
| Financial conditions (NFCI/ Goldman FCI proxy) | | | tightening/easing |
| USD liquidity proxy | | | |
| Correlation SPX–TLT (20d) | | | diversification broken? |
| Skew / put/call (if available) | | | hedging demand |

Flag **risk-off triggers already fired** vs **watch levels** for next week.

### Step 8 — Regime classification

Assign one primary regime:

| Regime | Typical signals |
|--------|-----------------|
| Goldilocks | Growth stable, inflation cooling, rates ↓, equities ↑ |
| Reflation | Growth ↑, inflation sticky, commodities ↑ |
| Stagflation fear | Growth ↓, inflation sticky |
| Risk-off / recession pricing | Curve bull steepening/inversion resolve, credit wider, VIX ↑ |
| Liquidity-driven | Policy/QT/RRP/TGA dominates |

State **confidence** (high/medium/low) and **what would falsify** the regime call.

### Step 9 — Anomalies & divergences

Actively hunt inconsistencies — these are trader edge:

- Index ↑ but breadth ↓
- Sector ETF ↑ but bellwether stock ↓
- Rates ↓ but growth stocks ↓ (unusual)
- Credit wider but equities at highs
- FX move inconsistent with rate differentials
- Commodity spike without sector follow-through
- HBM/GPU/API cost ↑ but AI capex guide ↑ and SOX ↓ (or reverse)
- HY OAS wider but equities at highs (credit-equity divergence)

Each anomaly: **observation → possible explanations → how to trade or wait**.

### Step 10 — Next-week playbook

Synthesize into trader-usable output:

1. **Base case narrative** (3–5 sentences)
2. **Highest-conviction setups** (max 3): direction, instrument, trigger, invalidation
3. **Scenarios table**: Bull / Base / Bear with probability weights (must sum ~100%)
4. **Calendar trades**: events to fade vs follow
5. **Risk budget**: reduce / maintain / add exposure; sector over/underweights
6. **Stop conditions**: what observation would force a full thesis reset

### Step 11 — Quality gate

Before delivery:

- [ ] **HY OAS + 10Y-2Y** from FRED (or proxy labeled) with 1W Δ in bp
- [ ] **Step 4.5** AI tables filled or explicitly "no new print this week"
- [ ] Every price/level has **as-of date** and source class (FRED / vendor page / exchange close)
- [ ] Facts vs opinions clearly labeled
- [ ] No fabricated consensus numbers — say "unavailable" if not verified
- [ ] Conflicting signals acknowledged, not smoothed over
- [ ] Report fits [weekly-report.md](templates/weekly-report.md) structure
- [ ] Action section has explicit invalidation levels

---

## Automation mode

When the user wants a **scheduled weekly Cursor Automation**, read the **automate** skill and follow its spine. Use this skill for **content design** only.

### Recommended automation defaults

| Field | Default | Notes |
|-------|---------|-------|
| Trigger | **Sunday 20:00 Beijing** (`0 20 * * 0`) | Confirm timezone Asia/Shanghai in editor |
| Name | Weekly Market Scan | |
| Memory | Enabled | Track recurring themes & watchlist |
| Tools | Post to Slack (optional) + **FRED MCP** | Credit/curve data; deliver report to channel |
| Prompt body | [automation-prompt.md](templates/automation-prompt.md) | Paste/adapt into automation instructions |
| Secrets | `FRED_API_KEY` in MCP env or Cloud | Required for HY OAS / T10Y2Y |

### Automation prompt rules

- Agent **must** run the full Step 0–11 checklist
- Agent **must** compare to prior run if memory enabled ("vs last week")
- Agent **must** pull HY OAS + 10Y-2Y via FRED MCP or `fetch_fred.py` before writing credit/curve fields
- Agent **must** run Step 4.5 AI supply chain tracker (HBM, cloud, API, capex)
- Agent **must not** invent data — FRED MCP / script / web search for verification
- Output: complete weekly report + 5-bullet executive summary at top
- If Slack enabled: exec summary in message, full report as thread or attached doc

### User config to collect before drafting automation

1. **Markets**: US only / US+CN / global
2. **Watchlist**: tickers or "use memory"
3. **Delivery**: Slack channel / **WeChat (PushPlus / 企业微信)** / file only / chat only
4. **Schedule**: day + time + timezone
5. **Language**: 中文 / English / bilingual
6. **Risk tolerance**: macro overlay only vs include trade ideas

---

## Output

| Format | Template | Use |
|--------|----------|-----|
| Full report | [weekly-report.md](templates/weekly-report.md) | 存档、Slack、桌面 |
| **WeChat** | [wechat-report.md](templates/wechat-report.md) | 手机阅读、PushPlus / 企业微信 / **公众号** |
| Executive only | summary + playbook | 快速浏览 |

Default: `weekly-report.md`. User asks 微信 / WeChat / 手机阅读 → use **`scan-wechat`** (no markdown tables; split 摘要+详情 if >3500 字).

### WeChat delivery

Cursor has **no native WeChat action**. Options: [wechat-delivery.md](reference/wechat-delivery.md)

1. **PushPlus**（个人微信，推荐）— `PUSHPLUS_TOKEN` + [scripts/push_wechat.py](scripts/push_wechat.py)
2. **企业微信群机器人** — `WECHAT_WEBHOOK_URL` + same script `--channel qywx`
3. **微信公众号** — `WECHAT_MP_APPID/SECRET` + [scripts/push_wechat_mp.py](scripts/push_wechat_mp.py)；需**企业认证**才能 API 自动发布，见 [wechat-delivery.md](reference/wechat-delivery.md)
4. **Automation 输出可复制版** — agent 在 chat 末尾给出 `wechat-report` 正文，手动转发

Automation 微信流：生成 wechat 格式 → 摘要推送 → 详情推送 →（可选）`push_wechat.py`.

---

## Additional resources

- FRED API & MCP setup: [fred-data.md](reference/fred-data.md)
- AI supply chain tracker: [ai-supply-chain.md](reference/ai-supply-chain.md)
- FRED fetch script: [scripts/fetch_fred.py](scripts/fetch_fred.py)
- WeChat format & push: [wechat-delivery.md](reference/wechat-delivery.md), [wechat-report.md](templates/wechat-report.md), [scripts/push_wechat.py](scripts/push_wechat.py)
- Full coverage & thresholds: [coverage-matrix.md](reference/coverage-matrix.md)
- Automation agent prompt: [automation-prompt.md](templates/automation-prompt.md)
- Report template: [weekly-report.md](templates/weekly-report.md)
