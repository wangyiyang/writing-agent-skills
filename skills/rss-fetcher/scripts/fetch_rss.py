#!/usr/bin/env python3
"""
RSS 抓取脚本 - 按日期范围获取 RSS 结果，支持关键词过滤
"""

import json
import sys
import os
import re
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
import concurrent.futures
import threading

# 默认浏览器 UA，用于绕过 WAF 拦截
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

# 本地数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date(date_str):
    """解析多种日期格式为 datetime 对象"""
    if not date_str:
        return None
    date_str = date_str.strip()
    # ISO 8601
    for fmt in [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    # RFC 822 (RSS 常用)
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        pass
    return None


class MLStripper(HTMLParser):
    """简单 HTML 标签剥离器"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return "".join(self.text)


def strip_html(html):
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except Exception:
        return html


def fetch_url(url, timeout=15, requires_ua=False):
    """获取 URL 内容，返回 bytes 或 None"""
    # 始终使用浏览器 UA，大多数站点会拦截 Python 默认 UA
    headers = {"User-Agent": BROWSER_UA}
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            return data, content_type
    except (URLError, HTTPError, Exception) as e:
        return None, str(e)


def parse_rss(xml_data, source_name):
    """解析 RSS/Atom XML，返回文章列表"""
    articles = []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        return articles

    # 检测命名空间
    ns = {}
    if root.tag.startswith("{"):
        ns["ns"] = root.tag.split("}")[0].strip("{")
    else:
        ns["ns"] = ""

    # RSS 2.0
    for item in root.findall(".//item", ns):
        title_el = item.find("title", ns)
        link_el = item.find("link", ns)
        desc_el = item.find("description", ns)
        # ElementTree 中空元素是 falsy，不能用 `or` 链式查找
        date_el = item.find("pubDate", ns)
        if date_el is None:
            date_el = item.find("date", ns)
        if date_el is None:
            date_el = item.find("{http://purl.org/dc/elements/1.1/}date", ns)

        title = title_el.text if title_el is not None and title_el.text else ""
        link = link_el.text if link_el is not None and link_el.text else ""
        desc = desc_el.text if desc_el is not None and desc_el.text else ""
        date_str = date_el.text if date_el is not None and date_el.text else ""

        # 清理 HTML
        title = strip_html(title).strip()
        desc = strip_html(desc).strip()

        articles.append({
            "title": title,
            "link": link,
            "description": desc,
            "date": parse_date(date_str),
            "source": source_name,
        })

    # Atom
    atom_entries = root.findall(".//{http://www.w3.org/2005/Atom}entry", ns)
    if not atom_entries:
        atom_entries = root.findall(".//entry", ns)
    for entry in atom_entries:
        title_el = entry.find("{http://www.w3.org/2005/Atom}title", ns)
        if title_el is None:
            title_el = entry.find("title", ns)
        link_el = entry.find("{http://www.w3.org/2005/Atom}link", ns)
        if link_el is None:
            link_el = entry.find("link", ns)
        summary_el = entry.find("{http://www.w3.org/2005/Atom}summary", ns)
        if summary_el is None:
            summary_el = entry.find("summary", ns)
        date_el = entry.find("{http://www.w3.org/2005/Atom}published", ns)
        if date_el is None:
            date_el = entry.find("published", ns)
        if date_el is None:
            date_el = entry.find("{http://www.w3.org/2005/Atom}updated", ns)
        if date_el is None:
            date_el = entry.find("updated", ns)

        title = title_el.text if title_el is not None and title_el.text else ""
        link = ""
        if link_el is not None:
            link = link_el.get("href", "") or (link_el.text or "")
        desc = summary_el.text if summary_el is not None and summary_el.text else ""
        date_str = date_el.text if date_el is not None and date_el.text else ""

        title = strip_html(title).strip()
        desc = strip_html(desc).strip()

        articles.append({
            "title": title,
            "link": link,
            "description": desc,
            "date": parse_date(date_str),
            "source": source_name,
        })

    return articles


def filter_by_date(articles, start_date, end_date):
    """按日期范围过滤文章"""
    if not start_date and not end_date:
        return articles
    filtered = []
    for a in articles:
        if a["date"] is None:
            # 无日期的文章默认包含
            filtered.append(a)
            continue
        if start_date and a["date"] < start_date:
            continue
        if end_date and a["date"] > end_date:
            continue
        filtered.append(a)
    return filtered


def filter_by_keywords(articles, positive_keywords, negative_keywords):
    """按关键词过滤文章"""
    if not positive_keywords and not negative_keywords:
        return articles

    # 构建正则（不区分大小写）
    pos_patterns = []
    for kw in positive_keywords:
        kw_text = kw.get("keyword", "") if isinstance(kw, dict) else str(kw)
        if kw_text:
            pos_patterns.append(re.compile(re.escape(kw_text), re.IGNORECASE))

    neg_patterns = []
    for kw in negative_keywords:
        kw_text = kw.get("keyword", "") if isinstance(kw, dict) else str(kw)
        if kw_text:
            neg_patterns.append(re.compile(re.escape(kw_text), re.IGNORECASE))

    filtered = []
    for a in articles:
        text = f"{a['title']} {a['description']}"

        # 反向关键词：匹配即排除
        if neg_patterns and any(p.search(text) for p in neg_patterns):
            continue

        # 正向关键词：至少匹配一个（如果有正向关键词）
        if pos_patterns:
            if not any(p.search(text) for p in pos_patterns):
                continue

        filtered.append(a)

    return filtered


def compute_score(article, positive_keywords):
    """根据正向关键词权重计算文章得分"""
    text = f"{article['title']} {article['description']}"
    score = 0
    matched_keywords = []

    for kw in positive_keywords:
        kw_text = kw.get("keyword", "") if isinstance(kw, dict) else str(kw)
        kw_weight = kw.get("weight", 1) if isinstance(kw, dict) else 1
        if kw_text and re.search(re.escape(kw_text), text, re.IGNORECASE):
            score += kw_weight
            matched_keywords.append(kw_text)

    return score, matched_keywords


def fetch_source(source, start_date=None, end_date=None):
    """抓取单个 RSS 源"""
    name = source.get("name", "unknown")
    url = source.get("url", "")
    status = source.get("status", "active")
    requires_ua = source.get("requires_ua", False)
    timeout = source.get("timeout", 15)
    proxy_url = source.get("proxy_url")

    # 跳过不可用的源
    if status != "active":
        return {"source": name, "status": "skipped", "reason": f"status={status}", "articles": []}

    # 使用代理 URL（如果有）
    fetch_url_str = proxy_url if proxy_url else url

    data, content_type = fetch_url(fetch_url_str, timeout=timeout, requires_ua=requires_ua)
    if data is None:
        return {"source": name, "status": "error", "reason": f"fetch failed: {content_type}", "articles": []}

    # 解析 RSS
    articles = parse_rss(data, name)
    if not articles:
        # 可能是 HTML（如 GitHub Trending）
        return {"source": name, "status": "error", "reason": "no RSS items found (may be HTML)", "articles": []}

    # 按日期过滤
    articles = filter_by_date(articles, start_date, end_date)

    return {"source": name, "status": "ok", "articles": articles}


def main():
    parser = argparse.ArgumentParser(description="RSS 抓取工具 - 按日期范围获取并过滤 RSS 结果")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="最近 N 天")
    parser.add_argument("--source", help="只抓取指定源（名称匹配）")
    parser.add_argument("--no-filter", action="store_true", help="不按关键词过滤")
    parser.add_argument("--format", choices=["json", "text", "markdown"], default="markdown", help="输出格式")
    parser.add_argument("--max-workers", type=int, default=5, help="并发抓取线程数")
    parser.add_argument("--min-score", type=int, default=0, help="最低关键词得分（0=不过滤）")
    args = parser.parse_args()

    # 计算日期范围
    end_date = None
    start_date = None
    if args.days:
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=args.days)
    elif args.start_date or args.end_date:
        if args.start_date:
            start_date = parse_date(args.start_date)
        if args.end_date:
            end_date = parse_date(args.end_date)
            if end_date:
                end_date = end_date.replace(hour=23, minute=59, second=59)

    # 加载数据
    sources_data = load_json("sources.json")
    keywords_data = load_json("keywords.json")

    sources = sources_data.get("sources", [])
    positive_keywords = keywords_data.get("positive_keywords", [])
    negative_keywords = keywords_data.get("negative_keywords", [])

    # 过滤源
    if args.source:
        sources = [s for s in sources if args.source.lower() in s.get("name", "").lower()]

    # 并发抓取
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(fetch_source, s, start_date, end_date): s
            for s in sources
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            all_results.append(result)

    # 合并所有文章
    all_articles = []
    for r in all_results:
        all_articles.extend(r.get("articles", []))

    # 关键词过滤
    if not args.no_filter:
        all_articles = filter_by_keywords(all_articles, positive_keywords, negative_keywords)

    # 计算得分
    for a in all_articles:
        score, matched = compute_score(a, positive_keywords)
        a["score"] = score
        a["matched_keywords"] = matched

    # 按最低得分过滤
    if args.min_score > 0:
        all_articles = [a for a in all_articles if a.get("score", 0) >= args.min_score]

    # 按日期排序（最新的在前）
    all_articles.sort(key=lambda x: x.get("date") or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    # 输出
    output = {
        "query": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "days": args.days,
            "source_filter": args.source,
            "no_filter": args.no_filter,
            "min_score": args.min_score,
        },
        "stats": {
            "total_sources": len(sources),
            "sources_ok": sum(1 for r in all_results if r["status"] == "ok"),
            "sources_error": sum(1 for r in all_results if r["status"] == "error"),
            "sources_skipped": sum(1 for r in all_results if r["status"] == "skipped"),
            "total_articles": len(all_articles),
        },
        "articles": all_articles,
        "source_results": [
            {"source": r["source"], "status": r["status"], "reason": r.get("reason", ""), "count": len(r.get("articles", []))}
            for r in all_results
        ],
    }

    if args.format == "json":
        # 自定义序列化 datetime
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                return super().default(obj)
        print(json.dumps(output, ensure_ascii=False, indent=2, cls=DateTimeEncoder))
    elif args.format == "markdown":
        print(f"# RSS 抓取结果")
        print(f"日期范围: {output['query']['start_date'] or '最早'} ~ {output['query']['end_date'] or '最新'}")
        print(f"源: {output['stats']['sources_ok']} 成功, {output['stats']['sources_error']} 失败, {output['stats']['sources_skipped']} 跳过")
        print(f"共 {output['stats']['total_articles']} 篇文章\n")
        for a in all_articles:
            date_str = a["date"].strftime("%Y-%m-%d %H:%M") if a.get("date") else "未知日期"
            print(f"## {a['title']}")
            print(f"- 来源: {a['source']}")
            print(f"- 日期: {date_str}")
            print(f"- 链接: {a['link']}")
            if a.get("score"):
                print(f"- 得分: {a['score']} (匹配: {', '.join(a.get('matched_keywords', []))})")
            if a.get("description"):
                desc = a["description"][:200]
                print(f"- 摘要: {desc}{'...' if len(a['description']) > 200 else ''}")
            print()
    else:  # text
        for a in all_articles:
            date_str = a["date"].strftime("%Y-%m-%d %H:%M") if a.get("date") else "未知"
            print(f"[{a['source']}] {a['title']} ({date_str})")
            print(f"  {a['link']}")
            if a.get("description"):
                print(f"  {a['description'][:150]}")
            print()


if __name__ == "__main__":
    main()
