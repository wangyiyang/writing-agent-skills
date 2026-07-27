---
name: rss-fetcher
description: Use when the user wants to fetch, aggregate, or filter RSS feed results within a date range. Supports keyword-based filtering with positive/negative keyword lists. Covers 26 verified working RSS sources including tech blogs, cloud provider blogs, and developer community feeds. Handles common access issues (WAF blocks, geo-restrictions, slow servers) with built-in workarounds.
---

# RSS Fetcher

按日期范围抓取 RSS 结果，支持关键词过滤和权重评分。

## 数据源

内置 37 个 RSS 源，其中 26 个已验证可用。数据文件：

- `data/sources.json` — RSS 源列表（含 URL、权重、访问方式、状态）
- `data/keywords.json` — 58 个正向关键词 + 7 个反向关键词

## 使用方法

```bash
# 抓取最近 3 天的 RSS
python3 scripts/fetch_rss.py --days 3

# 按日期范围抓取
python3 scripts/fetch_rss.py --start-date 2026-07-20 --end-date 2026-07-25

# 只抓取 AI 相关源，输出 JSON
python3 scripts/fetch_rss.py --days 7 --format json

# 不按关键词过滤，抓取所有文章
python3 scripts/fetch_rss.py --days 1 --no-filter

# 只抓取指定源
python3 scripts/fetch_rss.py --days 3 --source "掘金"

# 设置最低关键词得分
python3 scripts/fetch_rss.py --days 3 --min-score 2
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--days N` | 抓取最近 N 天的文章（⚠️ 注意是 `now() - N*24h`，不是自然天） |
| `--start-date` | 开始日期 (YYYY-MM-DD)，取当天 00:00 UTC |
| `--end-date` | 结束日期 (YYYY-MM-DD)，取当天 23:59:59 UTC |
| `--source` | 按名称过滤源 |
| `--no-filter` | 跳过关键词过滤 |
| `--min-score` | 最低关键词得分 |
| `--format` | 输出格式: json / markdown / text |
| `--max-workers` | 并发线程数（默认 5） |

### ⚠️ 时间窗口说明

`--days N` 覆盖的是「过去 N×24 小时」（`now() - timedelta(days=N)`），不是「前 N 个自然天」。
如果按自然天抓取（如每天 06:00 抓「昨天」的文章），应使用 `--start-date` + `--end-date` 指定精确的日期范围，避免跨天边界导致同篇文章重复出现在连续两次抓取中。

```bash
# ❌ 过去24小时（会跨越两个自然天，易产生重复）
python3 scripts/fetch_rss.py --days 1

# ✅ 昨天一整天（精确的自然天范围）
yesterday=$(date -d 'yesterday' '+%Y-%m-%d')
python3 scripts/fetch_rss.py --start-date "$yesterday" --end-date "$yesterday"
```

## Cron 配置

用于 `rss-to-notion-daily` cron 任务（每天早上 06:00 Asia/Shanghai 执行）：

```bash
cd /home/kk/Documents/Github/writing-agent-skills/rss-fetcher
yesterday=$(date -d 'yesterday' '+%Y-%m-%d')
python3 scripts/fetch_rss.py --start-date "$yesterday" --end-date "$yesterday" --format json --max-workers 5
```

输出为 JSON 格式后，按 `source` 分组，去重写入 Notion 数据库 `64533ee1-58c0-4906-ae17-dbacbf285ce6`。
字段映射：title → 名称、link → 链接、source → 来源、description → 摘要（截取前 2000 字符，Notion rich_text 限制）。

## 已知不可用源（11 个）

以下源因 WAF/GFW/RSS 接口下线等原因无法访问，脚本会自动跳过：

- 腾讯云开发者社区（RSS 接口下线）
- 阿里技术（RSS 接口下线）
- 字节跳动技术博客（域名废弃）
- Docker Blog（RSS 接口下线）
- GitHub Trending（HTML 页面，非 RSS）
- The Register（RSS 接口下线）
- IEEE Spectrum（Varnish WAF）
- ACM TechNews（Cloudflare WAF）
- Reddit r/programming（GFW 封锁）
- CSDN 资讯（RSS 接口下线）
- Lambda the Ultimate（服务器极不稳定）

## 依赖

- Python 3.8+
- 仅标准库，无需安装额外包
