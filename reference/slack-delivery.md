# Slack 投递 — 摘要 + Thread

Automation 启用 **Post to Slack** 时，按本规范投递周报。

---

## 流程

```
1. 完成 weekly-report.md 全文（Step 0–11）
2. 从执行摘要 + 关键数字生成 parent message（templates/slack-summary.md）
3. Post to Slack → 目标频道（parent）
4. 在同一消息的 thread 中按章节发送完整报告（可拆多条）
5. 同时在 Automation run output 保留完整 Markdown（存档）
```

**Parent 与 thread 缺一不可**：parent 仅摘要；细节只在 thread。

---

## Automation 配置

| 项 | 设置 |
|----|------|
| Tools | ✅ **Post to Slack** |
| Channel | 在编辑器选择目标频道（或 thread 回复模式见 Automations UI） |
| Slack 集成 | Cursor Settings 已连接 Slack workspace |
| Instructions | 必须包含「Slack 投递」段落 — 见 `templates/automation-prompt.md` |

Secrets：仅需 `FRED_API_KEY`（与 Slack 无关）。

---

## Parent message（频道主消息）

模板：[slack-summary.md](../templates/slack-summary.md)

| 规则 | 值 |
|------|-----|
| 最大长度 | **≤ 2500 字符** |
| 内容 | 5-bullet 摘要 + Quick levels + vs last week |
| 禁止 | Markdown 表格、超大代码块 |
| 结尾 | `_完整报告见 thread ↓_` |

**标题示例**：`📊 Weekly Market Scan · Week ending 2026-06-26`

---

## Thread 消息（完整报告）

按 `weekly-report.md` 章节顺序发送。**每条 thread 消息 ≤ 3500 字符**；超长则按章节边界拆分。

### 推荐拆分（4 条 thread）

| # | 章节 | 内容 |
|---|------|------|
| 1 | §1–§2 | 大类资产 + 宏观 |
| 2 | §3–§4.5 | 结构 + 轮动 + AI 产业链 |
| 3 | §5–§8 | 事件 + 股票 + 风险 + Regime |
| 4 | §9–§12 + 来源 | 异常 + Playbook + sources |

### Thread 格式

- 每条开头：`📎 *Part 1/4 — 大类资产 & 宏观*`
- 表格改为 bullet（Slack 表格支持差）
- 保留 `事实/解读/判断` 标注
- 最后一条末尾加：`— End of report · Week ending {{date}}`

### 长度超限

若单章仍超 3500 字符：按 `###` 小标题再拆，**同一 thread 内连续发送**，保持 Part x/y 编号。

---

## Agent 指令片段（粘贴到 Automation）

```
## Slack delivery (Post to Slack enabled)

After completing the full report:
1. Post parent message per templates/slack-summary.md (≤2500 chars) to the configured Slack channel.
2. Reply in that message's thread with the full report, split into ≤3500-char parts (see reference/slack-delivery.md). Label Part 1/N … Part N/N.
3. Also return the complete markdown in the automation run output.
4. Do not post WeChat or other channels.
If Post to Slack is disabled, skip steps 1–2; run output only.
```

---

## 质量检查（Slack 开启时）

- [ ] Parent 已发且 ≤ 2500 字符
- [ ] Thread 包含全部 12 章节，无遗漏
- [ ] 每条 thread ≤ 3500 字符
- [ ] Parent 与 thread 的 Week ending 日期一致
- [ ] FRED 数字与正文一致
- [ ] Run output 仍有完整 Markdown

---

## 故障处理

| 问题 | 处理 |
|------|------|
| Slack 未授权 | Cursor Settings 连接 Slack 后重跑 |
| 只发了 parent 无 thread | Instructions 强调必须 thread 发全文 |
| Thread 被截断 | 减小每条字符数，增加 Part 数量 |
| 频道未配置 | Automations 编辑器选择 channel 后保存 |
