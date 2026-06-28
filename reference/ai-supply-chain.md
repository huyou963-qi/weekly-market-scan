# AI Supply Chain & Capex Tracker

Weekly add-on for **Step 4.5**. Tracks the AI stack from **memory → compute rental → model API → hyperscaler capex**. Separate **事实 / 解读 / 判断**.

Data is mostly **vendor pages + industry research + web search** (not FRED). Store last-run values in Automation memory for week-over-week deltas.

---

## 4.5.1 HBM / DRAM memory pricing

### What to track

| Item | Metric | Why it matters |
|------|--------|----------------|
| HBM3e spot/contract | $/GB or $/unit trend | NVDA supply chain, MU/SK Hynix/Samsung margin |
| DRAM overall | DDR5 contract trend | PC/server baseline |
| Supply tightness | Lead times, allocation | Pricing power signal |

### Source priority

1. **TrendForce** — DRAM/HBM price trend reports (search: `TrendForce HBM price` + month)
2. **DRAMeXchange** / **Omdia** summaries (via press)
3. **Company calls** — MU, SK Hynix (000660.KS), Samsung (005930.KS) guidance on HBM bit growth & ASP
4. **Trade press** — Reuters, Nikkei Asia, EE Times on HBM allocation

### Report table

| 指标 | 本期 | 1W/1M Δ | 来源 | 解读 |
|------|------|---------|------|------|
| HBM (HBM3e) | | | TrendForce / vendor | tight/loosening |
| DRAM DDR5 | | | | |
| HBM supply commentary | | | Earnings/IR | |

If no numeric update this week: report **"no new print"** + last known level from memory.

---

## 4.5.2 AI cloud / GPU rental prices

Track **$/GPU-hour** for comparable configs (normalize to **H100 80GB** or **H200** where possible).

### Vendors to check (official pricing pages)

| Provider | Instance / SKU | Page pattern |
|----------|----------------|--------------|
| **AWS** | p5.48xlarge (H100) | aws.amazon.com/ec2/pricing/on-demand |
| **GCP** | a3-highgpu-8g (H100) | cloud.google.com/compute/gpus-pricing |
| **Azure** | ND H100 v5 | azure.microsoft.com/pricing/details/virtual-machines |
| **CoreWeave** | H100/H200 bare metal | coreweave.com/pricing |
| **Lambda** | H100 on-demand | lambdalabs.com/service/gpu-cloud |
| **Crusoe / Nebius** | If material price change | vendor site |

Also note **spot vs on-demand** spread if published.

### Report table

| Provider | SKU | $/hr (on-demand) | 1W Δ | Spot discount | Signal |
|----------|-----|------------------|------|---------------|--------|
| AWS | p5… | | | | |
| GCP | a3… | | | | |
| Azure | ND… | | | | |
| CoreWeave | H100 | | | | |

**Interpretation tags**: `tight supply` · `demand softening` · `promo/new instance` · `unchanged`

---

## 4.5.3 AI model API pricing

Track **$/1M tokens** (input / output) for flagship models. Flag **any official price change** in the week.

### Vendor checklist

| Vendor | Models | Pricing URL |
|--------|--------|-------------|
| **OpenAI** | GPT-4o, o-series, GPT-4.1 mini | platform.openai.com/docs/pricing |
| **Anthropic** | Claude Opus/Sonnet/Haiku | anthropic.com/pricing |
| **Google** | Gemini Pro/Flash | ai.google.dev/pricing |
| **Meta** | Llama via partners | llama.com or cloud partner pages |
| **AWS Bedrock** | Claude/Titan if changed | aws.amazon.com/bedrock/pricing |
| **Azure OpenAI** | Same as OpenAI tier | azure.microsoft.com/pricing/details/cognitive-services/openai-service |
| **Mistral / Cohere** | If competitive move | vendor pricing |

### Report table

| Vendor | Model | Input $/1M | Output $/1M | Change this week? | Effective date |
|--------|-------|------------|-------------|-------------------|----------------|
| OpenAI | | | | Y/N | |
| Anthropic | | | | | |
| Google | | | | | |

Note **price cuts** → margin pressure on infra; **price hikes** → demand inelasticity or cost pass-through.

---

## 4.5.4 AI Capex tracking

### Company-level (primary)

Pull from latest **10-Q/10-K, earnings call, investor day** — update on earnings weeks; otherwise carry forward with "unchanged since [date]".

| Company | Metric | Ticker |
|---------|--------|--------|
| Microsoft | Capex + capex guide | MSFT |
| Alphabet | Capex + cloud capex commentary | GOOGL |
| Amazon | AWS + total capex | AMZN |
| Meta | Capex guide | META |
| Oracle | Cloud/AI infra spend | ORCL |
| **NVIDIA** | Data center revenue, not capex | NVDA |

### Hyperscaler aggregate (quick math)

Sum guided **calendar-year capex** for MSFT+GOOGL+AMZN+META; note **1W change** only if new guidance.

### Macro overlay (FRED, optional)

| Series | ID | Frequency |
|--------|-----|-----------|
| Private nonresidential fixed investment | `PNFI` | Quarterly |
| Manufacturers' new orders: info processing equipment | `A34SNO` | Monthly |

### Report table

| Entity | LQ capex / guide | YoY | QoQ | AI-specific commentary | 1W update |
|--------|------------------|-----|-----|------------------------|-----------|
| MSFT | | | | | |
| GOOGL | | | | | |
| AMZN | | | | | |
| META | | | | | |
| Hyperscaler sum | | | | | |

---

## 4.5.5 AI stack synthesis (required paragraph)

Answer in 3–5 sentences:

1. **Cost curve**: HBM + GPU rental + API — getting cheaper, stable, or more expensive?
2. **Capex cycle**: accelerating, peaking, or questioned (tie to SOX/XLK price action)?
3. **Margin chain**: who captures margin (memory vs foundry vs cloud vs model)?
4. **Market linkage**: connect to **XLK, SOX, MU, NVDA** weekly moves.

---

## Search queries (copy-paste)

```
TrendForce HBM price trend [month year]
GPU cloud H100 price per hour AWS GCP Azure [month year]
OpenAI API pricing change [month year]
Anthropic Claude pricing [month year]
Microsoft Google Amazon Meta capex guidance [quarter year]
```

---

## Quality rules

- API/cloud prices: cite **vendor page + access date**; archived pages if price changed mid-week.
- HBM: prefer **industry researcher** over random blog quotes.
- Capex: **SEC filing > press summary**; include fiscal quarter label.
- Never invent WoW % if no new data — write `vs last report: unchanged`.
