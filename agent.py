"""
Web Research Agent — NO-KEY version (free).

Original: LangGraph + Tavily + OpenAI GPT-4o-mini (all needed paid keys).
This version: NO API keys at all, NO paid services, NO LangChain/LangGraph.

  Search:   DuckDuckGo HTML (free, no key) + Wikipedia API fallback (free, no key)
  Synthesise: extractive, deterministic — no LLM. It groups the real
              snippets into Summary / Key Findings / Sources, with URLs.
              It does NOT invent findings; if search returns nothing,
              it says so instead of making up a report.

Usage:
    python3 agent.py
    python3 agent.py --query "latest advances in quantum computing"
    python3 agent.py --query "Mind What If YouTube Shorts" --count 8

Only dependency: requests (already installed here). No .env needed.
The original key-based version is kept as agent-original.py.
"""

import argparse
import html
import re
import sys
from urllib.parse import quote_plus, urlparse

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def clean(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def ddg_search(query, count=5):
    """Free DuckDuckGo search, no key. Returns [{title, url, content}].
    Tries Lite first (works in this sandbox), then HTML."""
    from urllib.parse import unquote
    import subprocess
    for base, pat in [
        ("https://lite.duckduckgo.com/lite/?q=",
         r"""<a[^>]*href="([^"]+)"[^>]*class=['"]result-link['"][^>]*>(.*?)</a>.*?<td class=['"]result-snippet['"][^>]*>(.*?)</td>"""),
        ("https://html.duckduckgo.com/html/?q=",
         r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>'),
    ]:
        # curl works here where python-requests gets a 202 empty page from DDG
        try:
            html_text = subprocess.check_output(
                ["curl", "-s", "-A", HEADERS["User-Agent"], "-m", "20",
                 base + quote_plus(query)], text=True, timeout=25)
        except Exception:
            continue
        out = []
        for href, title, snippet in re.findall(pat, html_text, re.S):
            m = re.search(r"uddg=([^&]+)", href)
            if m:
                href = unquote(m.group(1))
            if href.startswith("//"):
                href = "https:" + href
            out.append({"title": clean(title), "url": href, "content": clean(snippet)})
            if len(out) >= count:
                break
        if out:
            return out
    return []


def wiki_search(query, count=5):
    """Free Wikipedia search API, no key. Fallback if DDG returns nothing."""
    url = ("https://en.wikipedia.org/w/api.php?action=query&list=search"
           "&srsearch=" + quote_plus(query) + "&format=json&srlimit=" + str(count))
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    out = []
    for hit in r.json().get("query", {}).get("search", []):
        out.append({
            "title": hit.get("title", ""),
            "url": "https://en.wikipedia.org/wiki/" + quote_plus(hit.get("title", "").replace(" ", "_")),
            "content": clean(hit.get("snippet", "")),
        })
    return out


def first_sentence(text):
    text = (text or "").strip()
    if not text:
        return ""
    m = re.match(r"(.{40,}?[.!?])(\s|$)", text)
    return m.group(1).strip() if m else text[:220]


def synthesize(query, results):
    """Extractive report from real snippets only — no LLM, no invented facts."""
    seen, findings = set(), []
    for r in results:
        s = first_sentence(r.get("content", ""))
        key = s.lower()[:80]
        if s and key not in seen:
            seen.add(key)
            findings.append((s, r.get("title", ""), r.get("url", "")))
    lines = []
    lines.append(f"## Summary\n{query}: {len(results)} sources found. "
                 f"Top finding — {findings[0][0] if findings else 'no snippets returned.'}")
    lines.append("\n## Key Findings")
    for i, (s, title, url) in enumerate(findings, 1):
        lines.append(f"- {s} [{title}]")
    lines.append("\n## Sources")
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r.get('title','')} — {r.get('url','')}")
    lines.append("\n_Note: extractive report from live search snippets — no LLM was used, "
                 "so findings are quoted, not rewritten._")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Web Research Agent (no keys, free)")
    p.add_argument("--query", default="latest advances in AI agents 2026",
                   help="Research query")
    p.add_argument("--count", type=int, default=5, help="Max sources (default 5)")
    args = p.parse_args()

    print(f"\n🔍 Researching: {args.query}\n", flush=True)
    try:
        results = ddg_search(args.query, args.count)
    except Exception as e:
        print(f"DDG search failed ({e}); trying Wikipedia…", file=sys.stderr)
        results = []
    if not results:
        try:
            results = wiki_search(args.query, args.count)
        except Exception as e:
            print(f"Wikipedia fallback failed: {e}", file=sys.stderr)
            results = []

    print("=" * 60)
    print("📄 RESEARCH REPORT  (free, no-key version)")
    print("=" * 60)
    if not results:
        print("No results found. Check the query / connection and try again.")
        return 1
    print(synthesize(args.query, results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
