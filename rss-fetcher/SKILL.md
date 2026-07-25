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
| `--days N` | 抓取最近 N 天的文章 |
| `--start-date` | 开始日期 (YYYY-MM-DD) |
| `--end-date` | 结束日期 (YYYY-MM-DD) |
| `--source` | 按名称过滤源 |
| `--no-filter` | 跳过关键词过滤 |
| `--min-score` | 最低关键词得分 |
| `--format` | 输出格式: json / markdown / text |
| `--max-workers` | 并发线程数（默认 5） |

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
