# WeChat 周报格式模板

> 微信不支持 Markdown 表格。用此模板替代 `weekly-report.md` 输出，或作为推送正文。
> 目标：单屏可读、分段清晰、数字 inline。**总字数建议 ≤ 3500 字**（超长则拆 2–3 条推送）。

---

## 格式规则

1. **不用表格** — 用「标签：数值」单行展示
2. **章节用【】** — 例：【一、执行摘要】
3. **层级用 emoji 仅作章节标记**（可选，勿滥用）
4. **1W 变动写清楚符号** — 例：SPX 7354（-2.0%）
5. **FRED 数据标注日期** — 例：HY OAS 312bp（6/24，FRED）
6. **判断句末尾标注** — （解读）/（判断）
7. 超 3500 字：拆为 **摘要推送** + **详情推送**（见下方 Split 方案）

---

## 正文模板（复制填充）

```
📊 周度市场检测
周期：Week ending YYYY-MM-DD
生成：YYYY-MM-DD HH:MM | 范围：US+Global Macro

━━━━━━━━━━━━━━━━
【执行摘要】
① Regime：……
② 最大变动：……
③ 轮动：FROM → TO
④ 核心风险：…… @ 触发位
⑤ 下周策略：……

━━━━━━━━━━━━━━━━
【大类资产 · 1W】
• SPX 0000（±X%）| NDX ±X% | RUT ±X%
• 10Y X.XX%（ΔXbp）| 10Y-2Y X.XX%（ΔXbp，FRED T10Y2Y）
• HY OAS XXXbp（ΔXbp，FRED BAMLH0A0HYM2）
• DXY XX.X | WTI $XX | Gold $XXXX | VIX XX.X
→ 一句话：cross-asset 逻辑

━━━━━━━━━━━━━━━━
【宏观 · 本周】
• 事件1：实际 vs 预期 → 市场反应
• 事件2：……
→ 宏观叙事 2–3 句

【宏观 · 下周日历】
🔴 H | 日期 事件
🟡 M | 日期 事件
🟢 L | 日期 事件

━━━━━━━━━━━━━━━━
【市场结构】
• 广度：A/D、NH/NL
• 风格：Growth/Value、Large/Small
• 资金流：……
→ 结构结论 1–2 句

━━━━━━━━━━━━━━━━
【行业轮动 · vs SPX】
领涨：XLV +X% | XLU +X% | …
领跌：XLK -X% | XLC -X% | …
细分：半导体/软件/医疗 …
→ 轮动：FROM → TO

━━━━━━━━━━━━━━━━
【AI 产业链】
内存：HBM/DRAM 价格趋势 + 来源
云 GPU：AWS/GCP/Azure $/hr（有无变动）
API：OpenAI/Anthropic/Google 定价（本周是否调价）
Capex：MSFT/GOOGL/AMZN/META 指引摘要
→ AI stack 结论 2 句

━━━━━━━━━━━━━━━━
【重点事件 & 股票】
• 事件 → 一阶/二阶影响
• NVDA ±X% | MSFT ±X% | …（|1W|>3% 才写）
→ 观点各一行

━━━━━━━━━━━━━━━━
【风险仪表盘】
• VIX XX（ΔX）| HY OAS XXXbp（ΔXbp）
• 10Y-2Y X.XX%（ΔXbp）
• 已触发：…… / 无
• 下周关注位：SPX XXXX | VIX XX | SOX XXXX

━━━━━━━━━━━━━━━━
【Regime】
主 regime + 置信度 H/M/L
失效条件：……
vs 上周：……

【异常 & 背离】
1. 观察 → 解释 → wait/fade/hedge
2. …

━━━━━━━━━━━━━━━━
【下周 Playbook】
Base（~55%）：3 句
Bull 25% | Base 55% | Bear 20%

Setup 1：方向·标的·触发·失效
Setup 2：……
Setup 3：……

仓位：risk budget / 超配 / 低配
重置条件：……

━━━━━━━━━━━━━━━━
来源：FRED / AP / …
免责：信息参考，非投资建议
```

---

## Split 方案（推荐 Automation 使用）

**推送 1 — 摘要（≤ 800 字，必发）**
- 标题：`📊 周报摘要 MM-DD`
- 内容：执行摘要 5 条 + 大类资产 6 行 + Playbook 1 行

**推送 2 — 详情（≤ 3000 字）**
- 标题：`📊 周报详情 MM-DD`
- 内容：宏观/结构/轮动/AI/风险/Regime/Setup

**推送 3 — 可选**
- 仅当 AI 或 semi 周度驱动强时，单独发【AI 产业链】段落

---

## 与完整版关系

| 输出 | 用途 |
|------|------|
| `weekly-report.md` | 存档、Slack、桌面阅读 |
| `wechat-report.md` | 微信推送正文 |
| 摘要 + 详情 split | Automation 定时推送 |
