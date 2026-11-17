# Free Web Research Agent — no keys, no cost

A web research agent that searches the web for any topic and returns a
structured report — **Summary, Key Findings, Sources** — with **no API keys,
no paid services, and no LLM**.

```bash
python3 agent.py --query "latest advances in AI agents 2026"
python3 agent.py --query "HyperFrames video framework" --count 8
```

## How it works

- **Search:** DuckDuckGo Lite (free, no key), with a Wikipedia API fallback
  (free, no key). DuckDuckGo can rate-limit on heavy use; the fallback
  covers that.
- **Synthesis:** extractive and deterministic — no LLM. It quotes the real
  search snippets into the report and says so if nothing is found.
  It does not invent findings.
- **Only dependency:** `requests`.

## Install

```bash
pip install -r requirements.txt
python3 agent.py --query "your topic here"
```

No `.env`, no keys, no sign-up, no spend.

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

## Limits (honest)

- Findings are quoted snippets, not a polished essay — there is no LLM
  rewriting them. Hand the report to your favourite LLM for a polish.
- Niche topics can come out thin when the search falls back to Wikipedia.

## Origin

Derived from agent 01, Web Research Agent, in
[ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects)
(MIT). The original key-based version (LangGraph + Tavily + OpenAI
GPT-4o-mini) is kept untouched as `agent-original.py` — use it if you
later add those keys. This rewrite removes all three paid/keyed parts.

## License

MIT — see `LICENSE`.
