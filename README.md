# Free Web Research Agent — no keys, no cost

A web research agent that searches the web for any topic and returns a
structured report — **Summary, Key Findings, Sources** — with **no API keys,
no paid services, and no LLM**.

```bash
python3 agent.py --query "latest advances in AI agents 2026"
python3 agent.py --query "HyperFrames video framework" --count 8
```

## What it does

Give it any topic — a technology, a person, a place, a current event, a
concept — and it returns a short, structured research report you can read
in under a minute:

- **Summary** — how many sources were found, and what they agree on.
- **Key Findings** — the main facts, quoted from the sources themselves.
- **Sources** — every finding traced back to a named source with a link,
  so you can check it yourself.

It never invents findings. If nothing useful is found, it says so instead
of guessing.

## How it works

1. **Search (free, no key):** DuckDuckGo Lite first. If DuckDuckGo
   rate-limits or returns nothing, it falls back to the Wikipedia API
   (also free, no key, no sign-up).
2. **Synthesis (no LLM):** extractive and deterministic. It quotes the
   real search snippets into the report — the same query always gives
   the same report. There is no model rewriting, paraphrasing, or
   hallucinating.
3. **Output:** a plain-text report printed to your terminal. Pipe it to
   a file (`> report.txt`) to keep it, or hand it to your favourite LLM
   for a polished essay.

**Only dependency:** `requests`.

## Install

```bash
pip install -r requirements.txt
python3 agent.py --query "your topic here"
```

No `.env`, no keys, no sign-up, no spend.

## Usage

```bash
# Default: 5 sources
python3 agent.py --query "artificial intelligence agents"

# More sources
python3 agent.py --query "HyperFrames video framework" --count 8

# Save the report
python3 agent.py --query "quantum computing" --count 5 > quantum-report.txt
```

Options:

| Option | Default | What it does |
| --- | --- | --- |
| `--query "topic"` | required | The topic to research |
| `--count N` | 5 | How many sources to include |

## Sample output

```
🔍 Researching: artificial intelligence agents

📄 RESEARCH REPORT  (free, no-key version)
## Summary
artificial intelligence agents: 5 sources found. ...

## Key Findings
- An AI agent is an artificial intelligence program that can make
  decisions, pursue goals, and take actions independent of humans. ...

## Sources
1. Intelligent agent — https://en.wikipedia.org/wiki/Intelligent_agent
...
```

## Details

- **Language:** Python 3, one file (`agent.py`).
- **Search sources:** DuckDuckGo Lite, then Wikipedia API.
- **Cost:** $0. No API keys, no accounts, no subscriptions.
- **Privacy:** your query goes only to DuckDuckGo / Wikipedia — the
  public search services themselves. No data is sent to any AI provider.
- **Works offline?** No — it needs internet to search, but nothing else.
- **Deterministic:** no randomness, no model temperature. Same query,
  same sources, same report.

## How this differs from the original

This repo is derived from agent 01, Web Research Agent, in
[ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects)
(MIT). The original needs three paid/keyed parts:

| Original | This version |
| --- | --- |
| OpenAI GPT-4o-mini (paid key) | No LLM — extractive quoting |
| Tavily search API (paid key) | DuckDuckGo Lite + Wikipedia (free) |
| LangGraph / LangChain | Plain Python, no framework |

The original key-based version is kept untouched as
`agent-original.py` — use it if you later add those keys.

## Limits (honest)

- Findings are quoted snippets, not a polished essay — there is no LLM
  rewriting them. Hand the report to your favourite LLM for a polish.
- Niche topics can come out thin when the search falls back to Wikipedia.
- DuckDuckGo can rate-limit on heavy use; the Wikipedia fallback covers
  that, but a very heavy burst of queries may still slow down.
- It reports what sources say; it does not fact-check them against each
  other. Check the Sources list for anything you will rely on.

## License

MIT — see `LICENSE`.
