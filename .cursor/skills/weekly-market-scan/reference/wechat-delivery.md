# 微信推送 — 方案与配置

Cursor Automation **没有原生微信工具**。可通过 **Webhook + 格式化正文** 实现定时推送到微信。

---

## 方案对比

| 方案 | 难度 | 适合 | 格式支持 |
|------|------|------|----------|
| **PushPlus** | ⭐ 低 | 个人微信 | HTML/Markdown，推荐 |
| **企业微信群机器人** | ⭐⭐ 中 | 团队/自己建群 | Markdown（部分） |
| **微信公众号** | ⭐⭐⭐⭐ 高 | 已有**企业认证**公众号 | HTML 图文，见下方 |
| **Server酱 Turbo** | ⭐ 低 | 个人 | Markdown |
| **手动复制** | ⭐ 最低 | 偶尔查看 | 用 `wechat-report.md` 模板 |
| **Slack → 微信桥** | ⭐⭐⭐ | 已有 Slack | 间接 |

---

## 方案 A — PushPlus（推荐个人）

1. 注册 [pushplus.plus](https://www.pushplus.plus)，微信扫码绑定
2. 复制 **token**
3. Automation 结束时调用 webhook，或使用 `scripts/push_wechat.py`

### 环境变量

```
PUSHPLUS_TOKEN=your_token
```

### 手动测试

```bash
export PUSHPLUS_TOKEN=your_token
python scripts/push_wechat.py --title "周报摘要 06-26" --file /path/to/wechat-body.txt
```

### Automation 集成

- **Trigger**: cron 周一 08:00
- **Agent 指令**: 输出 `wechat-report.md` 格式 → 拆成摘要+详情两段 → 调用 push 脚本
- **Webhook trigger**（可选）: Automation 完成后 POST 到自建中间层再调 PushPlus

PushPlus API:
```
POST https://www.pushplus.plus/send
Content-Type: application/json
{"token":"TOKEN","title":"标题","content":"正文","template":"markdown"}
```

**限制**: 单条约 2 万字符；建议摘要 ≤800 字、详情 ≤3000 字。

---

## 方案 B — 企业微信群机器人

1. 企业微信 → 群聊 → 群机器人 → 添加 → 复制 **Webhook URL**
2. 设置 `WECHAT_WEBHOOK_URL`

```bash
export WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXXX
python scripts/push_wechat.py --channel qywx --title "周报" --file body.txt
```

企业微信 markdown 限制：
- 不支持复杂表格
- 单条 ≤ 4096 bytes
- 用 `wechat-report.md` 的 bullet 格式，勿用 HTML 大表格

---

## 方案 D — 微信公众号（Official Account）

**能发，但门槛高。** Cursor 无原生公众号接口；Automation 云端生成正文后，调用 **微信公众平台 API** 写入草稿或发布。

### 前提条件（必读）

| 条件 | 说明 |
|------|------|
| **账号类型** | 订阅号或服务号；自 **2025-07 起**，**个人主体 / 未认证企业** 账号已被回收 **发布能力 API**（`freepublish/*`） |
| **推荐** | **企业认证** 的订阅号/服务号，否则只能走「草稿 + 人工后台发布」或完全手动 |
| **开发者配置** | 公众平台 → 设置与开发 → 基本配置 → **AppID + AppSecret** |
| **IP 白名单** | 调用 API 的服务器 IP 需在公众平台配置（Cloud Agent 出口 IP 可能变动 → 见下方 workaround） |

官方文档：[发布能力](https://developers.weixin.qq.com/doc/subscription/guide/product/publish.html) · [草稿箱](https://developers.weixin.qq.com/doc/subscription/guide/product/draft.html)

### 两种投递模式

**模式 1 — 草稿箱（推荐起步）**

```
Automation 生成 HTML 正文
  → POST /cgi-bin/draft/add（写入草稿）
  → 你在 mp.weixin.qq.com 后台预览 → 手动点「发布」
```

- 适合：想人工终审、账号 API 权限不全
- 粉丝体验：正式发布后出现在订阅号消息列表

**模式 2 — 全自动发布**

```
draft/add → freepublish/submit → freepublish/get 轮询状态
```

- 需要：**企业认证** + 发布接口权限
- 内容须为 **HTML**（非 Markdown 表格）；图片须先调「上传图文消息内图片」接口

### 内容格式限制

| 字段 | 限制 |
|------|------|
| title | ≤ 32 字 |
| digest | ≤ 128 字（摘要，推送卡片显示） |
| content | HTML，≤ 2 万字符；**不支持外部图片 URL**（须先上传获微信 URL） |
| 周报建议 | 用 `wechat-report.md` 转 HTML；长文拆 **上/下篇** 或 **摘要文 + 阅读原文链接** |

### Cloud Secrets（Automation 用）

```
WECHAT_MP_APPID=wx................
WECHAT_MP_SECRET=................
WECHAT_MP_PUBLISH=0   # 0=仅草稿  1=自动发布（需认证权限）
```

脚本：`scripts/push_wechat_mp.py`（见 skill 目录）

```bash
python scripts/push_wechat_mp.py \
  --title "周度市场检测 06-26" \
  --digest "NDX -4.6%，轮动至医疗防御…" \
  --file wechat-body.html
```

### IP 白名单问题（Cloud Agent）

微信 API 要求来源 IP 在白名单内。Cursor Cloud Agent 出口 IP **不固定** 时：

1. **中间层服务器**（固定 IP 的 VPS）— Automation webhook 触发 VPS，VPS 调微信 API（最稳）
2. **仅草稿 + 本地脚本** — Cloud 生成 HTML 输出到 artifact/repo，本机或 VPS cron 调 `push_wechat_mp.py`
3. **阅读原文外链** — 公众号只发短摘要，全文放 Notion/飞书/自建页（规避 2 万字符与 HTML 限制）

### 订阅号 vs 服务号（推送频率）

| 类型 | 群发/发表 | 适合周报 |
|------|-----------|----------|
| **订阅号** | 发表后展示于订阅号列表；群发有次数限制 | 每周 1 篇 ✅ |
| **服务号** | 每月群发 4 次（服务号规则更严） | 更适合短提醒 + 外链 |

### 与 PushPlus 的区别

| | PushPlus | 微信公众号 |
|--|----------|------------|
| 触达 | 个人微信聊天窗 | 订阅号/服务号消息列表 |
| 需要 | token | AppID/Secret + 认证 |
| 内容 | Markdown 即可 | HTML + 素材上传 |
| 粉丝 | 无需关注公众号 | 需关注你的号 |

**若目标是「自己看」** → PushPlus 足够。  
**若目标是「给订阅粉丝发每周研报」** → 走公众号 API 或草稿箱。

---

## 方案 C — Automation 纯 Agent 流程（无脚本）

在 Automation prompt 末尾追加：

```
## 微信投递
1. 按 templates/wechat-report.md 生成正文（禁止表格）
2. 拆成两条：摘要（≤800字）+ 详情（≤3000字）
3. 若配置了 PUSHPLUS_TOKEN，运行 scripts/push_wechat.py 推送
4. 否则在输出末尾单独给出「微信可复制版」代码块
```

---

## 可读性要点

1. **永远不用 Markdown 表格** — 微信内会乱码
2. **数字带上下文** — `SPX 7354（-2.0% 1W）` 而非单独 `-2%`
3. **FRED 标注** — `HY OAS 312bp（6/24 FRED）`
4. **先摘要后详情** — 忙时只看第一条
5. **固定发送时间** — 周一 08:00 或周日 20:00（用户自选）

---

## Automation 草稿字段（供 automate skill 使用）

| 字段 | 建议值 |
|------|--------|
| Name | Weekly Market Scan → WeChat |
| Trigger | `0 8 * * 1`（周一 08:00） |
| Memory | Enabled（对比上周 AI/credit 数据） |
| Tools | MCP (FRED) + webhook/脚本 |
| Output | `wechat-report.md` split × 2 |
| Secrets | `FRED_API_KEY`, `PUSHPLUS_TOKEN` 或 `WECHAT_WEBHOOK_URL` |

---

## 安全

- Token / Webhook URL **只放环境变量或 Cursor Secrets**，勿写入 skill 或 git
- PushPlus token 泄露可在官网重置
