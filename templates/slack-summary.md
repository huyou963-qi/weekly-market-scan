# Slack 摘要消息模板（Parent message）

> 作为 **频道主消息** 发送；完整报告发在同一条消息的 **thread** 里。  
> 目标长度：**≤ 2500 字符**（留余量给 Slack 格式）。

---

```
📊 *Weekly Market Scan* · Week ending {{FRIDAY_DATE}}

*Regime* · {{one line}}
*Top move* · {{cross-asset headline}}
*Rotation* · {{FROM → TO}}
*Key risk* · {{risk + trigger level}}
*Playbook* · {{one actionable line}}

*Quick levels*
• SPX {{level}} ({{1W}}) · NDX {{1W}} · RUT {{1W}}
• HY OAS {{bp}} ({{1W Δ}}bp, FRED) · 10Y-2Y {{spread}} ({{1W Δ}}bp)
• VIX {{level}} · DXY {{level}}

*vs last week* · {{1-2 lines from memory, or "首周无对比"}}

_完整报告见 thread ↓_
```

---

## 格式规则

- 用 Slack `*bold*` 和 `•` bullet，**不要用 Markdown 表格**
- 数字 inline：`SPX 7354 (-2.0% 1W)`
- FRED 字段标注 `(FRED)` 和 as-of 日期
- 末尾固定 `_完整报告见 thread ↓_` 引导点击
