# Writing Agent Skills

[English](README.en.md) | 中文

写作相关的 Agent Skills 集合,可通过 [`npx skills`](https://skills.sh) 一键安装到 Claude Code、Cursor、Codex、Kimi Code CLI 等 70+ 编程 Agent。

## Skills 一览

| Skill | 简介 | 文档 |
| --- | --- | --- |
| `rss-fetcher` | 按日期范围抓取 RSS 结果,支持关键词过滤和权重评分 | [SKILL.md](skills/rss-fetcher/SKILL.md) |
| `content-originality-check` | 内容原创性自检(防低创作度),发布前对稿件做诊断与改稿 | [SKILL.md](skills/content-originality-check/SKILL.md) |
| `notion-to-blog` | 将 Notion 页面自动转化为 Jekyll 博客文章 | [SKILL.md](skills/notion-to-blog/SKILL.md) |

## 安装

### 方式一:npx skills(推荐)

无需全局安装,一条命令即可:

```bash
# 交互式安装:选择要装的 skill 和目标 agent
npx skills add wangyiyang/writing-agent-skills
```

常用选项:

```bash
# 先查看仓库里有哪些 skills(不安装)
npx skills add wangyiyang/writing-agent-skills --list

# 只安装指定的 skill
npx skills add wangyiyang/writing-agent-skills --skill rss-fetcher

# 指定目标 agent(可多个)
npx skills add wangyiyang/writing-agent-skills -a claude-code -a cursor

# 安装到用户级目录(对所有项目生效),并跳过确认提示
npx skills add wangyiyang/writing-agent-skills -g -y
```

默认安装到项目目录(如 `.agents/skills/`、`.claude/skills/`),可随项目提交共享给团队;加 `-g` 则安装到用户级目录。

### 方式二:手动安装

```bash
git clone https://github.com/wangyiyang/writing-agent-skills.git
```

然后把 `skills/` 下需要的 skill 目录拷贝(或软链)到你的 agent skills 目录,例如 Claude Code 的 `~/.claude/skills/` 或通用的 `~/.agents/skills/`。

## 使用

### rss-fetcher

按日期范围抓取 RSS 结果,支持关键词过滤和权重评分。

- 26 个已验证可用的 RSS 源(中文技术社区、大厂博客、国际媒体、云原生、AI/LLM)
- 58 个正向关键词 + 7 个反向关键词过滤
- 权重评分、三种输出格式(JSON / Markdown / Text)、并发抓取

```bash
python3 skills/rss-fetcher/scripts/fetch_rss.py --days 3
```

详见 [skills/rss-fetcher/SKILL.md](skills/rss-fetcher/SKILL.md)。

### content-originality-check

内容原创性自检(防低创作度)。在选题 → 写作 → 发布前对稿件做诊断与改稿。

- 四条红线分级:同质化 / 搬运洗稿 / 信息量不足 / 低价值 AIGC
- 完整 AI 痕迹模式库(内容、语言、排版、对话残留四大类,含前后对照示例)
- 50 分制质量评分,45 分以下重新修订

详见 [skills/content-originality-check/SKILL.md](skills/content-originality-check/SKILL.md)。

### notion-to-blog

将 Notion 页面自动转化为 Jekyll 博客文章。

- 全自动:提取页面属性 → 下载 Markdown → 下载图片 → 生成 Front Matter → Jekyll 构建验证
- 自动处理 Notion 特有标记(callout、空块、图片路径替换)
- md5 去重验证图片,防顺序错乱
- 通过 `BLOG_ROOT` 环境变量适配任意 Jekyll 博客

```bash
export BLOG_ROOT=/path/to/jekyll-blog
python3 skills/notion-to-blog/convert.py <notion-page-uuid-or-url>
```

详见 [skills/notion-to-blog/SKILL.md](skills/notion-to-blog/SKILL.md)。

## 管理已安装的 Skills

```bash
npx skills list      # 查看已安装的 skills
npx skills update    # 更新到最新版本
npx skills remove    # 卸载
```

## 项目结构

```
├── skills/                          # 所有 skills(npx skills 标准发现目录)
│   ├── rss-fetcher/                 # RSS 抓取 skill
│   │   ├── SKILL.md
│   │   ├── data/                    # 源列表 + 关键词配置
│   │   └── scripts/                 # 抓取脚本
│   ├── content-originality-check/   # 原创性自检 skill
│   │   ├── SKILL.md
│   │   ├── references/              # AI 痕迹模式库(渐进式加载)
│   │   └── evals/                   # 测试用例(evals.json)
│   └── notion-to-blog/              # Notion → Jekyll 转换 skill
│       ├── SKILL.md
│       └── convert.py               # 全自动转换脚本
└── eval-workspaces/                 # 评测运行结果
    └── content-originality-check/
        └── iteration-1/             # benchmark + with/without skill 对照输出
```

## 关注公众号

![微信公众号二维码](https://www.wangyiyang.cc/images/qrcode.jpg)

## License

[MIT](LICENSE)
