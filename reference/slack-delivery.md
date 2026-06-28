# Slack 投递 — 摘要 + GitHub 外链

Automation 启用 **Post to Slack** 时，按本规范投递周报。**不发 thread**。

---

## 流程

```
1. 完成 weekly-report.md 全文（Step 0–11）
2. 写入 reports/week-ending-YYYY-MM-DD.md（按 templates/weekly-report.md）
3. git add → commit → push 到 main（message: report: week ending YYYY-MM-DD）
4. 从执行摘要 + 关键数字生成 parent message（templates/slack-summary.md）
5. Post to Slack → 目标频道（仅 1 条 parent，含 GitHub 链接）
6. 同时在 Automation run output 保留完整 Markdown（存档）
```

**Slack 仅摘要 + 链接**；完整报告在 GitHub `reports/` 与 Run output。

---

## Automation 配置

| 项 | 设置 |
|----|------|
| Tools | ✅ **Post to Slack** |
| Git repo | `huyou963-qi/weekly-market-scan`（Agent 需能 commit/push） |
| Channel | 在编辑器选择目标频道 |
| Slack 集成 | Cursor Settings 已连接 Slack workspace |
| Instructions | 短版即可 — 交付细节以 `AGENTS.md` Step 12 为准 |

Secrets：仅需 `FRED_API_KEY`（与 Slack 无关）。

---

## GitHub 归档

| 项 | 值 |
|----|-----|
| 路径 | `reports/week-ending-YYYY-MM-DD.md` |
| 分支 | `main` |
| Commit message | `report: week ending YYYY-MM-DD` |
| 外链格式 | `https://github.com/huyou963-qi/weekly-market-scan/blob/main/reports/week-ending-YYYY-MM-DD.md` |

Push **成功后** 再把该 URL 写入 Slack parent。Push 失败时：Slack 注明「报告未 push，完整版见 Run output」，不要发无效链接。

---

## Parent message（频道主消息 — 唯一一条）

模板：[slack-summary.md](../templates/slack-summary.md)

| 规则 | 值 |
|------|-----|
| 最大长度 | **≤ 2500 字符** |
| 内容 | 5-bullet 摘要 + Quick levels + vs last week + GitHub 链接 |
| 禁止 | Markdown 表格、超大代码块 |
| Thread | **0 条** — 不要 reply in thread |
| 结尾 | GitHub 完整报告 URL + `_完整报告见上方链接_` |

**标题示例**：`📊 Weekly Market Scan · Week ending 2026-06-26`

---

## Agent 指令片段（Automation Instructions 可仅保留一行）

```
交付格式以 AGENTS.md Step 12 为准：reports/ 归档 + push + Slack 单条摘要含 GitHub 链接，0 thread。
```

完整规范见本文件与 `AGENTS.md`，无需在 Instructions 重复 thread 拆分规则。

---

## 质量检查（Slack 开启时）

- [ ] `reports/week-ending-YYYY-MM-DD.md` 已 commit 并 push
- [ ] Slack parent 已发且 ≤ 2500 字符
- [ ] Parent 含可访问的 GitHub blob URL（日期与 Week ending 一致）
- [ ] **无** thread 回复
- [ ] FRED 数字与正文一致
- [ ] Run output 仍有完整 Markdown

---

## 故障处理

| 问题 | 处理 |
|------|------|
| Slack 未授权 | Cursor Settings 连接 Slack 后重跑 |
| push 失败 | Slack 说明见 Run output；修复 git 权限后重跑 |
| 链接 404 | 确认 push 成功且路径与日期一致 |
| 私有仓库打不开 | 确保 Slack 读者有 GitHub 仓库权限 |
| 频道未配置 | Automations 编辑器选择 channel 后保存 |
