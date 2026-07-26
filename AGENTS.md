# AGENTS.md — writing-agent-skills

## Project Overview

`writing-agent-skills` 是一个面向 AI 编程 Agent 的写作相关技能（Skills）集合。仓库托管在 `github.com/wangyiyang/writing-agent-skills`，可通过 [`npx skills`](https://skills.sh) 一键安装到 Claude Code、Cursor、Codex、Kimi Code CLI 等 70+ 编程 Agent。许可证为 MIT。

项目包含 3 个独立技能：

| Skill | 作用 | 技术形态 |
|---|---|---|
| `rss-fetcher` | 按日期范围抓取 RSS 结果，支持关键词过滤和权重评分 | Python 脚本 + JSON 配置 |
| `content-originality-check` | 内容原创性自检（防低创作度），诊断与去 AI 味 | 纯 SKILL.md 指令（无代码） |
| `notion-to-blog` | 将 Notion 页面自动转化为 Jekyll 博客文章 | Python 脚本 |

## Technology Stack

- **Python 3.8+** — rss-fetcher 和 notion-to-blog 的运行环境
- **仅标准库** — 两个 Python 脚本均无外部依赖（`xml.etree.ElementTree`、`concurrent.futures`、`urllib`、`subprocess`、`re`、`json`、`hashlib` 等）
- **Notion REST API v2022-06-28** — notion-to-blog 通过 `curl` 命令行调用 Notion API
- **Jekyll** — notion-to-blog 在输出文章后执行 `bundle exec jekyll build` 做构建验证
- **RSS / Atom** — rss-fetcher 使用标准库解析 XML feed，支持 RSS 2.0 和 Atom 两种格式

## Project Structure

```
├── skills/                                    # npx skills 标准发现目录
│   ├── rss-fetcher/                           # RSS 抓取技能
│   │   ├── SKILL.md                           # 技能描述与使用说明
│   │   ├── data/
│   │   │   ├── sources.json                   # RSS 源列表（37 个，26 个可用）
│   │   │   └── keywords.json                  # 正向关键词（58 个）+ 反向关键词（8 个）
│   │   └── scripts/
│   │       └── fetch_rss.py                   # RSS 抓取主脚本（427 行）
│   ├── content-originality-check/             # 内容原创性自检技能
│   │   ├── SKILL.md                           # 技能描述与执行步骤（100 行）
│   │   ├── references/
│   │   │   └── ai-patterns.md                 # AI 痕迹模式库（4 大类，含前后对照示例）
│   │   └── evals/
│   │       └── evals.json                     # 评测用例（3 个测试场景）
│   └── notion-to-blog/                        # Notion → Jekyll 转换技能
│       ├── SKILL.md                           # 技能描述与工作流（102 行）
│       └── convert.py                         # 自动化转换脚本（337 行）
├── eval-workspaces/                           # 评测运行结果
│   └── content-originality-check/
│       └── iteration-1/                       # 第一轮基准测试
│           ├── benchmark.json                 # 结构化评测数据（含 with/without skill 对比）
│           ├── benchmark.md                   # 评测摘要
│           ├── eval-de-ai-only/               # "去 AI 味"场景
│           ├── eval-restructure-needed/       # "需要重构"场景
│           ├── eval-topic-precheck/           # "选题预检"场景
│           └── review.html                    # 评审报告
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-07-26-readme-rewrite-design.md  # README 重写设计文档
├── README.md                                  # 中文 README（主文档）
├── README.en.md                               # 英文 README
├── LICENSE                                    # MIT License
├── .gitignore                                 # 忽略规则
└── AGENTS.md                                  # 本文件
```

## Skill 文件规范

每个 skill 目录必须包含一个 `SKILL.md` 文件，格式如下：

```yaml
---
name: <skill-name>
description: >-
  <一句话说明该技能何时触发>
---
```

- `name` — 技能名称，与目录名一致
- `description` — 触发条件描述，使用 YAML 多行字符串，给 AI agent 判断是否该使用本技能
- SKILL.md 正文使用 Markdown 编写，包含详细的使用步骤、参数说明、完成标准等

## Build & Test Commands

### rss-fetcher

```bash
# 抓取最近 3 天的 RSS
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 3

# 按日期范围抓取
python3 skills/rss-fetcher/scripts/fetch_rss.py --start-date 2026-07-20 --end-date 2026-07-25

# 其他参数
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 7 --format json
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 1 --no-filter
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 3 --source "掘金"
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 3 --min-score 2
```

### notion-to-blog

```bash
export NOTION_API_TOKEN=$(cat ~/.config/notion/api_key 2>/dev/null)
export BLOG_ROOT=/path/to/jekyll-blog
python3 skills/notion-to-blog/convert.py <page-uuid-or-url>
```

## Code Style Guidelines

- Python 脚本使用 `#!/usr/bin/env python3` shebang
- Python 命名：函数名 `snake_case`，常量 `UPPER_SNAKE_CASE`，类名 `PascalCase`
- Python 注释中/英文混合使用，与相邻内容语言一致
- argparse 作为 CLI 参数解析标准库
- `subprocess.run()` 用于外部命令调用（curl、jekyll）
- `concurrent.futures.ThreadPoolExecutor` 用于并发任务
- 错误处理模式：返回 (data, error_string) 二元组，或使用自定义 `die()` 函数打印错误并退出
- 日志输出使用 emoji 前缀（ℹ️ 信息、✅ 成功、❌ 错误）
- JSON 配置文件使用 schema：sources 数组包含 `name`/`url`/`weight`/`status`/`notes` 等字段
- keywords.json 使用 `positive_keywords` 和 `negative_keywords` 两个数组，每个条目含 `keyword`/`category`/`weight`

## Testing Strategy

### 技能级评测（content-originality-check）

技能本身不包含可运行的测试代码，而是通过 `evals/evals.json` 定义 3 个评测场景：

1. **eval-de-ai-only** — "去 AI 味"场景：测试仅去味不重构的能力
2. **eval-restructure-needed** — "需要重构"场景：测试识别同质化/搬运等红线问题的能力  
3. **eval-topic-precheck** — "选题预检"场景：测试选题饱和度的评估能力

每个场景包含 prompt（用户输入）、expected_output（期望行为）和 keyword-based 自动判分逻辑。

### 基准测试方法论

`eval-workspaces/content-originality-check/iteration-1/` 包含实际运行结果：

- **with_skill** vs **without_skill** 对照实验（各运行 3 次）
- 评测维度：pass rate、time、tokens
- 评分方式：关键字命中匹配（非语义判断）
- 基准结果（iteration-1）：with_skill 通过率 100%，without_skill 89%，时间成本增加约 91 秒

## Deployment

### 通过 npx skills 安装（推荐）

```bash
# 交互式安装
npx skills add wangyiyang/writing-agent-skills

# 只安装指定 skill
npx skills add wangyiyang/writing-agent-skills --skill rss-fetcher

# 指定目标 agent
npx skills add wangyiyang/writing-agent-skills -a claude-code -a cursor

# 安装到用户级目录
npx skills add wangyiyang/writing-agent-skills -g -y
```

### 手动安装

```bash
git clone https://github.com/wangyiyang/writing-agent-skills.git
# 将 skills/ 下需要的目录拷贝到 agent 的 skills 目录
cp -r skills/rss-fetcher ~/.agents/skills/
```

### 管理命令

```bash
npx skills list      # 查看已安装的 skills
npx skills update    # 更新到最新版本
npx skills remove    # 卸载
```

## Security Considerations

- notion-to-blog 需要 `NOTION_API_TOKEN`，支持从环境变量或 `~/.config/notion/api_key` 文件读取
- .gitignore 已排除 `.env` 和 `.pi-subagents/` 等敏感目录
- rss-fetcher 使用浏览器 User-Agent 绕过 WAF 拦截，但不处理需要认证的 RSS 源
- 两个 Python 脚本均不在任何安全沙箱中运行——`subprocess.run()` 和 `urlopen()` 都直接操作宿主机网络和文件系统

## Additional Notes

- 仓库默认分支为 `master`
- 所有文档/注释以中文为主，英文为辅助（`README.en.md`）
- rss-fetcher 数据中 37 个源仅 26 个可用，不可用源因 WAF/GFW/RSS 下线等原因无法访问，脚本自动跳过
- notion-to-blog 涉及 S3 签名 URL、md5 去重、图片路径替换等多个已知陷阱（详见 SKILL.md）
- 新增技能时必须创建 `skills/<skill-name>/SKILL.md`，并在 README 的技能一览表中补充
