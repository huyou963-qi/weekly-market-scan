# Weekly Market Scan — Coverage Matrix

## Cross-asset minimum set

### Equities

| Region | Index / ETF | Role |
|--------|-------------|------|
| US large | SPX, SPY | Core benchmark |
| US growth | NDX, QQQ | Tech/growth proxy |
| US small | RUT, IWM | Risk appetite / credit sensitivity |
| US value | — or RPV/IWD | Style leg |
| China A | CSI 300, 000300.SS | Onshore risk (if in scope) |
| HK | HSI, 2800.HK | Offshore China / Asia |
| Europe | STOXX 600, DAX | Global cycle |
| Japan | N225, 1321.T | Yen / carry context |
| EM | EEM, VWO | Dollar / commodity beta |

### Fixed income & rates

| Instrument | Role |
|------------|------|
| UST 2Y, 10Y, 30Y yields | Policy & term premium |
| 2s10s, 10s30s spread | Curve / recession signal |
| TIPS breakeven 5Y/10Y | Inflation expectations |
| TLT / IEF | Duration equity |
| LQD, HYG | IG / HY credit proxy |
| CDX IG/HY (if available) | Pure credit risk |

### FX

| Pair / Index | Role |
|--------------|------|
| DXY | Global USD liquidity |
| EURUSD | ECB vs Fed |
| USDJPY | Risk / BOJ |
| USDCNH | China policy / flows |
| AUDUSD, USDMXN | Commodity / EM FX |

### Commodities

| Instrument | Role |
|------------|------|
| WTI, Brent | Energy inflation / geopolitics |
| Gold | Real rates / fear |
| Copper | Global growth |
| Natural gas | Energy shock |
| CRB / DBC | Broad commodity beta |

### Volatility & alternatives

| Instrument | Role |
|------------|------|
| VIX, VIX9D/VIX3M ratio | Near-term fear vs term structure |
| VVIX | Vol-of-vol |
| MOVE | Bond market stress |
| BTC, ETH | Risk-on liquidity (optional) |

---

## Equity structure — GICS Level 1

Always score vs SPX (1W relative return):

| Code | Sector | Typical macro sensitivity |
|------|--------|---------------------------|
| XLK | Technology | Rates, growth, AI capex |
| XLF | Financials | Curve, credit, regulation |
| XLV | Health Care | Defensive, policy, FDA |
| XLE | Energy | Oil, geopolitics |
| XLI | Industrials | Cycle, PMI, capex |
| XLP | Consumer Staples | Defensive, consumer |
| XLY | Consumer Discretionary | Consumer, rates |
| XLU | Utilities | Rates, defensive |
| XLRE | Real Estate | Rates, credit |
| XLB | Materials | China, USD, commodities |
| XLC | Communication Services | Ad cycle, mega-cap |

**Level 2 drill-down triggers** (report sub-industry detail when):
- Industry 1W rel perf vs sector > ±2%
- Clear catalyst (regulation, commodity, earnings cluster)
- User watchlist concentrated in one industry

Examples: Semiconductors vs Software; Banks vs Insurance; E&P vs Refiners; Homebuilders vs Retail.

---

## Factor & style lens

| Factor | Proxy | What to note |
|--------|-------|--------------|
| Growth vs Value | QQQ vs IWD / IWF vs IWD | Rates regime |
| Large vs Small | SPY vs IWM | Liquidity / recession fear |
| Quality | QUAL vs SPY | Flight to quality |
| Momentum | MTUM vs SPY | Trend persistence |
| Low vol | USMV vs SPY | Defensive bid |
| Dividend | VYM vs SPY | Yield hunting |

---

## Event taxonomy

### Tier 1 (always detail in report)

- FOMC decision, CPI, Core PCE, NFP, GDP advance
- Megacap earnings (AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA — adjust list)
- Geopolitical shock with energy/trade channel
- Credit event (bank stress, sovereign, large default)

### Tier 2 (table row + sector tag)

- Retail sales, ISM PMI, housing starts, jobless claims trend
- ECB/BOJ/PBoC decisions
- Sector-heavy earnings week
- OPEX / index rebalance

### Tier 3 (calendar mention only)

- Single mid-cap earnings
- Minor regulatory filing
- Low-impact international data

---

## Move thresholds (when to expand detail)

| Object | Threshold | Action |
|--------|-----------|--------|
| Index | \|1W\| > 2% | Explain drivers in narrative |
| Sector ETF | \|1W rel\| > 1.5% | Sector paragraph |
| Single stock | \|1W\| > 5% or >2σ vol | Name-level card |
| Yield (10Y) | \|1W\| > 15bp | Rates section lead |
| VIX | Level > 20 or \|1W\| > 4 pts | Risk dashboard highlight |
| HY OAS | \|1W\| > 25bp | Credit stress flag |
| DXY | \|1W\| > 1.5% | FX transmission paragraph |
| HBM/API/GPU price | Official change or >5% WoW (reported) | Step 4.5 detail |
| Hyperscaler capex guide | Any revision | Step 4.5 + event matrix |

---

## AI infrastructure watchlist (Step 4.5)

| Layer | Tickers / entities | Data type |
|-------|-------------------|-----------|
| Memory | MU, SK Hynix, Samsung | HBM ASP, bit growth |
| GPU | NVDA, AMD | DC revenue, supply |
| Cloud | MSFT, AMZN, GOOGL | Capex, GPU rental $/hr |
| Models | OpenAI, Anthropic, GOOGL | API $/1M tokens |
| Semi equip | AMAT, LRCX, KLAC | Order trends |

---

## Data source priority

1. **FRED API / FRED MCP** — HY OAS (`BAMLH0A0HYM2`), 10Y-2Y (`T10Y2Y`), UST yields (`DGS2`, `DGS10`); optional capex macro (`PNFI`, `A34SNO`). See [fred-data.md](fred-data.md).
2. Exchange / index official closes
3. **AI vendor pricing pages** — cloud GPU, model API (see [ai-supply-chain.md](ai-supply-chain.md))
4. Industry research — TrendForce/DRAMeXchange for HBM
5. Central bank & statistical agency releases
6. Major financial data terminals / aggregators (verify date)
7. Company IR / SEC filings for capex & AI commentary
8. Reputable financial press for narrative — cross-check numbers

If live data unavailable in automation run: state lag explicitly; do not guess.
