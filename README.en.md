# Writing Agent Skills

English | [中文](README.md)

A collection of writing-related Agent Skills, installable in one command via [`npx skills`](https://skills.sh) to 70+ coding agents including Claude Code, Cursor, Codex, and Kimi Code CLI.

## Skills

| Skill | Description | Docs |
| --- | --- | --- |
| `rss-fetcher` | Fetch RSS feeds within a date range, with keyword filtering and weighted scoring | [SKILL.md](rss-fetcher/SKILL.md) |
| `content-originality-check` | Pre-publish originality review (anti "low-originality" penalties): diagnose and revise drafts | [SKILL.md](content-originality-check/SKILL.md) |
| `notion-to-blog` | Automatically convert Notion pages into Jekyll blog posts | [SKILL.md](notion-to-blog/SKILL.md) |

## Installation

### Option 1: npx skills (recommended)

No global install needed — one command does it:

```bash
# Interactive install: pick the skills and target agents
npx skills add wangyiyang/writing-agent-skills
```

Common options:

```bash
# List available skills in the repo (without installing)
npx skills add wangyiyang/writing-agent-skills --list

# Install a specific skill
npx skills add wangyiyang/writing-agent-skills --skill rss-fetcher

# Target specific agents (multiple allowed)
npx skills add wangyiyang/writing-agent-skills -a claude-code -a cursor

# Install to your user directory (available across all projects), skipping prompts
npx skills add wangyiyang/writing-agent-skills -g -y
```

By default, skills are installed into the project directory (e.g. `.agents/skills/`, `.claude/skills/`) so they can be committed and shared with your team; add `-g` to install them at user level instead.

### Option 2: Manual install

```bash
git clone https://github.com/wangyiyang/writing-agent-skills.git
```

Then copy (or symlink) the skill directories you need into your agent's skills directory, e.g. `~/.claude/skills/` for Claude Code or the generic `~/.agents/skills/`.

## Usage

### rss-fetcher

Fetch RSS feeds within a date range, with keyword filtering and weighted scoring.

- 26 verified working RSS sources (Chinese tech communities, big-tech blogs, international media, cloud-native, AI/LLM)
- 58 positive keywords + 7 negative keywords for filtering
- Weighted scoring, three output formats (JSON / Markdown / Text), concurrent fetching

```bash
python3 rss-fetcher/scripts/fetch_rss.py --days 3
```

See [rss-fetcher/SKILL.md](rss-fetcher/SKILL.md) for details.

### content-originality-check

Pre-publish originality review (anti "low-originality" penalties). Diagnose and revise drafts across topic selection, writing, and publishing.

- Four red-line categories: homogenization / plagiarism & rewriting / insufficient information / low-value AIGC
- A complete library of AI-writing trace patterns (content, language, formatting, conversational residue — with before/after examples)
- 50-point quality score; anything below 45 goes back for revision

See [content-originality-check/SKILL.md](content-originality-check/SKILL.md) for details.

### notion-to-blog

Automatically convert Notion pages into Jekyll blog posts.

- Fully automated: extract page properties → download Markdown → download images → generate Front Matter → verify with a Jekyll build
- Handles Notion-specific markup (callouts, empty blocks, image path rewriting)
- MD5-based image deduplication to prevent ordering issues
- Works with any Jekyll blog via the `BLOG_ROOT` environment variable

```bash
export BLOG_ROOT=/path/to/jekyll-blog
python3 notion-to-blog/convert.py <notion-page-uuid-or-url>
```

See [notion-to-blog/SKILL.md](notion-to-blog/SKILL.md) for details.

## Managing Installed Skills

```bash
npx skills list      # List installed skills
npx skills update    # Update to the latest versions
npx skills remove    # Uninstall
```

## Project Structure

```
├── rss-fetcher/                 # RSS fetcher skill
│   ├── SKILL.md
│   ├── data/                    # Source list + keyword config
│   └── scripts/                 # Fetch scripts
├── content-originality-check/   # Originality review skill
│   ├── SKILL.md
│   ├── references/              # AI-trace pattern library (progressive loading)
│   └── evals/                   # Test cases (evals.json) + eval run results (iteration-1/)
└── notion-to-blog/              # Notion → Jekyll converter skill
    ├── SKILL.md
    └── convert.py               # Fully automated conversion script
```

## Follow the WeChat Official Account

![WeChat Official Account QR code](https://www.wangyiyang.cc/images/qrcode.jpg)

## License

[MIT](LICENSE)
