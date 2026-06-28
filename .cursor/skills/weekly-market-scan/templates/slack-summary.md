# Slack 摘要消息模板（Parent message — 唯一一条）

> 作为 **频道主消息** 发送；完整报告在 **GitHub `reports/`**，不发 thread。  
> 目标长度：**≤ 2500 字符**（留余量给 Slack 格式与 URL）。

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

📎 *完整报告* · https://github.com/huyou963-qi/weekly-market-scan/blob/main/reports/week-ending-{{FRIDAY_DATE}}.md

_完整报告见上方链接_
```

---

## 格式规则

- 用 Slack `*bold*` 和 `•` bullet，**不要用 Markdown 表格**
- 数字 inline：`SPX 7354 (-2.0% 1W)`
- FRED 字段标注 `(FRED)` 和 as-of 日期
- GitHub URL 必须在 **push 成功之后** 再发送
- **不要**发 thread；**不要**写 `_完整报告见 thread ↓_`
