# RSS Fetcher Skill

按日期范围抓取 RSS 结果，支持关键词过滤和权重评分的 Agent Skill。

## 功能

- 按日期范围抓取 RSS 文章（`--days 3` 或 `--start-date/--end-date`）
- 关键词过滤（58 个正向关键词 + 7 个反向关键词）
- 权重评分（根据匹配关键词计算文章得分）
- 26 个已验证可用的 RSS 源
- 三种输出格式（JSON / Markdown / Text）
- 并发抓取，纯 Python 标准库

## 安装

### 通过 NPX 使用（推荐）

```bash
# 直接运行，无需安装
npx rss-fetcher-skill --days 3
npx rss-fetcher-skill --start-date 2026-07-20 --end-date 2026-07-25
npx rss-fetcher-skill --days 1 --format json
```

### 全局安装

```bash
npm install -g rss-fetcher-skill
rss-fetcher --days 3
```

### 作为 Skill 安装到 Agent

将 `rss-fetcher/` 目录软链或复制到 Agent 的 skills 目录：

```bash
ln -s /path/to/rss-fetcher ~/.agents/skills/rss-fetcher
```

### 从源码运行

```bash
git clone https://github.com/wangyiyang/writing-agent-skills.git
cd writing-agent-skills
python3 rss-fetcher/scripts/fetch_rss.py --days 3
```

## 使用方法

```bash
# 抓取最近 3 天的 RSS
rss-fetcher --days 3

# 按日期范围抓取
rss-fetcher --start-date 2026-07-20 --end-date 2026-07-25

# 输出 JSON
rss-fetcher --days 1 --format json

# 不按关键词过滤
rss-fetcher --days 1 --no-filter

# 只抓取指定源
rss-fetcher --days 3 --source "掘金"

# 设置最低关键词得分
rss-fetcher --days 3 --min-score 3
```

## 参数

| 参数 | 说明 |
|------|------|
| `--days N` | 抓取最近 N 天 |
| `--start-date` | 开始日期 (YYYY-MM-DD) |
| `--end-date` | 结束日期 (YYYY-MM-DD) |
| `--source` | 按名称过滤源 |
| `--no-filter` | 跳过关键词过滤 |
| `--min-score` | 最低关键词得分 |
| `--format` | 输出格式：json / markdown / text |
| `--max-workers` | 并发线程数（默认 5） |

## 数据源

内置 37 个 RSS 源（26 个已验证可用），涵盖：

- 中文技术社区：掘金、OSChina、SegmentFault、InfoQ 中文站
- 大厂技术博客：AWS、Azure、MongoDB、美团
- 国际技术媒体：The Verge、Ars Technica、TechCrunch、Wired
- 云原生与基础设施：Kubernetes、CNCF、Go、Rust
- AI/LLM 相关：HackNews、Dev.to、何夕2077

## 项目结构

```
rss-fetcher/
├── SKILL.md                  # Skill 使用说明
├── data/
│   ├── sources.json          # RSS 源列表
│   └── keywords.json         # 关键词配置
└── scripts/
    └── fetch_rss.py          # 抓取脚本
bin/
└── rss-fetcher.js            # NPX 入口
package.json                  # npm 包配置
```

## 环境要求

- Node.js 14+（用于 NPX 入口）
- Python 3.8+（RSS 抓取脚本）

## License

[MIT](LICENSE)
