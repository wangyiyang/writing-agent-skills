# Writing Agent Skills

写作相关的 Agent Skills 集合。

## Skills

### rss-fetcher

按日期范围抓取 RSS 结果，支持关键词过滤和权重评分。

- 26 个已验证可用的 RSS 源（中文技术社区、大厂博客、国际媒体、云原生、AI/LLM）
- 58 个正向关键词 + 7 个反向关键词过滤
- 权重评分、三种输出格式（JSON / Markdown / Text）、并发抓取

```bash
python3 rss-fetcher/scripts/fetch_rss.py --days 3
```

详见 [rss-fetcher/SKILL.md](rss-fetcher/SKILL.md)。

### content-originality-check

内容原创性自检（防低创作度）。在选题 → 写作 → 发布前对稿件做诊断与改稿。

- 四条红线分级：同质化 / 搬运洗稿 / 信息量不足 / 低价值 AIGC
- 完整 AI 痕迹模式库（内容、语言、排版、对话残留四大类，含前后对照示例）
- 50 分制质量评分，45 分以下重新修订

详见 [content-originality-check/SKILL.md](content-originality-check/SKILL.md)。

## 项目结构

```
├── rss-fetcher/                 # RSS 抓取 skill
│   ├── SKILL.md
│   ├── data/                    # 源列表 + 关键词配置
│   └── scripts/                 # 抓取脚本
└── content-originality-check/   # 原创性自检 skill
    ├── SKILL.md
    ├── references/              # AI 痕迹模式库（渐进式加载）
    └── evals/                   # 测试用例
```

## License

[MIT](LICENSE)
