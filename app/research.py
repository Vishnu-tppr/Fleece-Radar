"""🔬 Deep-research discovery for Fleece Radar — free, keyless, multi-source.

Mimics a deep-research pass:
  1. diversified CN/EN queries over free search backends
     (Bing HTML · DuckDuckGo HTML/Lite · SearXNG public instances · Mojeek,
      plus Brave Search API if BRAVE_SEARCH_API_KEY is set — free tier 2k/mo)
  2. stable community feeds
     (linux.do forum via Discourse JSON · GitHub awesome-list raw READMEs ·
      dynamic GitHub repo search for new key/list repos)
  3. directory crawls (apiindex.me · apisou.com · baipiao.org · getcheapai ·
     freellm · freeaiapi · kelen.cc · apiranking)
  4. one-hop expansion: fetch promising non-gateway pages (blog posts, forum
     threads, gists, docs) and pull gateway links out of them
Every new candidate is then run through the standard passive provider scanner.
"""
from __future__ import annotations
import asyncio
import os
import re
from urllib.parse import unquote, urlparse

import httpx

from . import core

UA = os.getenv("USER_AGENT", "FleeceRadar/1.0 (passive research)")
H = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}

QUERIES = [
    "免费 GPT-6 Astra 中转 API",
    "Claude Fable 5 白嫖 API 中转",
    "免费 DeepSeek V4 Flash API 中转",
    "免费 GLM 5.3 Flash API 注册送",
    "中转站 福利 注册送 token",
    "免费 AI API 公益站 签到",
    "AI API 中转站 导航 排行榜",
    "free Claude API gateway signup credit",
    "free DeepSeek API relay no credit card",
]

DIRECTORIES = [
    "https://apiindex.me/zh/self-publish",
    "https://apisou.com/?type=公益",
    "https://baipiao.org/free/api/",
    "https://www.getcheapai.com/provider",
    "https://freellm.net/",
    "https://freeaiapi.org/",
    "https://kelen.cc/share/free-llm-api-stations",
    "https://apiranking.com/",
]

GITHUB_RAW = [
    "https://raw.githubusercontent.com/mn-api/awesome-ai-proxy/main/README.md",
    "https://raw.githubusercontent.com/guihuashaoxiang/FreeLLM-API-KeyHub/main/README.md",
    "https://raw.githubusercontent.com/AIPMAndy/FreeToken/main/README.md",
    "https://raw.githubusercontent.com/mnfst/awesome-free-llm-apis/main/README.md",
    "https://raw.githubusercontent.com/cuihuan/awesome-ai-gateway/main/README.md",
    "https://raw.githubusercontent.com/12britz/awesome-free-models/main/README.md",
]

SEARXNG_INSTANCES = [
    "https://searx.be",
    "https://search.bus-hit.me",
    "https://searx.tiekoetter.com",
    "https://paulgo.io",
    "https://search.ononoki.org",
    "https://priv.au",
    "https://searxng.site",
    "https://search.inetol.net",
]

URL_RE = r"https?://[^\s\)\]\"'<>]+"
SIGNUP_RE = re.compile(r"(register|sign-up|signup|aff=|ref=|注册|福利)", re.I)


# ---------------- search backends (all free) ----------------

async def bing_search(client, q):
    try:
        await client.get("https://www.bing.com/", follow_redirects=True)  # cookie warm-up
        r = await client.get("https://www.bing.com/search", params={"q": q, "count": 20},
                             follow_redirects=True)
        urls = re.findall(r'<h2[^>]*><a[^>]*href="(https?://[^"]+)"', r.text)
        return [u for u in urls if "bing.com" not in u and "microsoft.com" not in u and "go.micro" not in u]
    except Exception:
        return []


async def ddg_search(client, q):
    out = []
    try:
        r = await client.get("https://html.duckduckgo.com/html/", params={"q": q}, follow_redirects=True)
        out += [unquote(u) for u in re.findall(r"uddg=([^\"&]+)", r.text)]
    except Exception:
        pass
    try:
        r = await client.get("https://lite.duckduckgo.com/lite/", params={"q": q}, follow_redirects=True)
        out += re.findall(r'href="(https?://(?!duckduckgo)[^"]+)"', r.text)
    except Exception:
        pass
    return out


async def searxng_search(client, q):
    for base in SEARXNG_INSTANCES:
        try:
            r = await client.get(base + "/search",
                                 params={"q": q, "format": "json", "language": "zh"},
                                 follow_redirects=True, timeout=10)
            data = r.json()
            urls = [x["url"] for x in data.get("results", []) if x.get("url")]
            if urls:
                return urls
        except Exception:
            continue
    return []


async def mojeek_search(client, q):
    try:
        r = await client.get("https://www.mojeek.com/search", params={"q": q}, follow_redirects=True)
        return re.findall(r'<a class="ob" href="(https?://[^"]+)"', r.text)
    except Exception:
        return []


async def brave_search(client, q):
    key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not key:
        return []
    try:
        r = await client.get("https://api.search.brave.com/res/v1/web/search",
                             params={"q": q, "count": 20},
                             headers={"X-Subscription-Token": key, "Accept": "application/json"})
        return [x["url"] for x in r.json().get("web", {}).get("results", []) if x.get("url")]
    except Exception:
        return []


# ---------------- community feeds ----------------

async def github_feed(client):
    """Static awesome-lists + dynamic repo search → raw READMEs → URLs."""
    urls = []
    for u in GITHUB_RAW:
        try:
            r = await client.get(u, timeout=10)
            urls += re.findall(URL_RE, r.text)
        except Exception:
            pass
    try:
        r = await client.get("https://api.github.com/search/repositories",
                             params={"q": "free llm api", "sort": "stars", "per_page": 5},
                             headers={**H, "Accept": "application/vnd.github+json"}, timeout=10)
        for repo in r.json().get("items", []):
            slug = f"{repo['owner']['login']}/{repo['name']}"
            for branch in ("main", "master"):
                try:
                    rr = await client.get(f"https://raw.githubusercontent.com/{slug}/{branch}/README.md",
                                          timeout=10)
                    if rr.status_code == 200:
                        urls += re.findall(URL_RE, rr.text)
                        break
                except Exception:
                    continue
    except Exception:
        pass
    return urls


async def linuxdo_feed(client):
    """linux.do (Discourse) — the hub where Chinese relay freebies are posted.
    Public JSON endpoints, no key: /search.json → /t/{id}.json → /raw/{tid}/{pid}."""
    urls = []
    try:
        r = await client.get("https://linux.do/search.json",
                             params={"q": "免费 API 中转 福利"},
                             headers={**H, "Accept": "application/json"}, timeout=15)
        topics = r.json().get("topics", [])[:8]
        for t in topics:
            tid = t.get("id")
            if not tid:
                continue
            try:
                tr = await client.get(f"https://linux.do/t/{tid}.json",
                                      headers={**H, "Accept": "application/json"}, timeout=15)
                post_ids = tr.json().get("post_stream", {}).get("post_ids", [])[:2]
                for pid in post_ids:
                    raw = await client.get(f"https://linux.do/raw/{tid}/{pid}", timeout=15)
                    urls += re.findall(URL_RE, raw.text)
            except Exception:
                continue
    except Exception:
        pass
    return urls


# ---------------- candidate filtering ----------------

def looks_like_gateway(url, domain):
    if any(s in domain for s in core.SKIP_NETLOCS):
        return False
    if core.DOMAIN_KW.search(domain.lstrip("www.")):
        return True
    if SIGNUP_RE.search(url):
        return True
    return False


async def deep_research(max_context_pages=15, max_scan=120):
    rows = core.list_findings(limit=100000)
    existing = {core.canonical_domain(r["url"]) for r in rows}
    raw_hits: list[str] = []
    backends_used = 0

    async with httpx.AsyncClient(timeout=12, follow_redirects=True, headers=H) as client:
        # phase 1 — queries × free search backends
        for q in QUERIES:
            for fn in (bing_search, ddg_search, searxng_search, mojeek_search):
                found = await fn(client, q)
                if found:
                    backends_used += 1
                raw_hits += found
            found = await brave_search(client, q)
            if found:
                backends_used += 1
            raw_hits += found
            await asyncio.sleep(0.4)
        # phase 2 — community feeds
        raw_hits += await github_feed(client)
        raw_hits += await linuxdo_feed(client)
        # directories
        for durl in DIRECTORIES:
            raw_hits += await core.discover_directory(durl)

    cands: list[str] = []
    seen: set[str] = set()
    for u in raw_hits:
        u = u.strip().rstrip('.,;:)')
        try:
            n = core.normalize_url(u)
        except Exception:
            continue
        if not n or n in seen:
            continue
        d = core.canonical_domain(n)
        if not d or not looks_like_gateway(n, d):
            continue
        seen.add(n)
        cands.append(n)

    new_cands = [c for c in cands if core.canonical_domain(c) not in existing]
    provider_domains = {core.canonical_domain(c) for c in new_cands}

    # phase 3 — one-hop expansion: pull gateway links out of non-gateway pages
    # (blog posts, forum threads, gists, docs, comparison sites)
    expanded: list[str] = []
    pages = 0
    async with httpx.AsyncClient(timeout=12, follow_redirects=True, headers=H) as client2:
        for u in cands:
            if pages >= max_context_pages:
                break
            d = core.canonical_domain(u)
            if d in provider_domains:
                continue  # the gateway itself is already a candidate
            try:
                r = await client2.get(u)
                pages += 1
                for x in core.extract_urls(r.text):
                    xd = core.canonical_domain(x)
                    if xd in existing or xd in provider_domains:
                        continue
                    if looks_like_gateway(x, xd):
                        expanded.append(x)
            except Exception:
                continue
    cset = set(cands)
    for e in dict.fromkeys(expanded):
        if e not in cset:
            cset.add(e)
            cands.append(e)
            new_cands.append(e)

    to_scan = list(dict.fromkeys(new_cands))[:max_scan]
    scanned = await core.scan_many(to_scan, "discovery") if to_scan else []

    return {
        "queries": QUERIES,
        "directories": DIRECTORIES,
        "search_backends_with_results": backends_used,
        "raw_hits": len(raw_hits),
        "gateway_candidates": len(cands),
        "new_candidates": len(new_cands),
        "context_pages_expanded": pages,
        "scanned": len(to_scan),
        "alive": sum(1 for f in scanned if f.alive),
        "new_domains": sorted({core.canonical_domain(u) for u in to_scan}),
        "generated_at": core.utcnow(),
    }


# ---------------- synthesis: the "deep research" digest ----------------

def research_report_md() -> str:
    rows = core.list_findings(limit=100000)
    alive = [r for r in rows if r["alive"]]
    L = []
    L.append("# 🐑 Fleece Radar — research digest  (薅羊毛雷达)")
    L.append(f"\nGenerated: {core.utcnow()}")
    L.append("")
    L.append(f"- Providers tracked: **{len(rows)}**")
    L.append(f"- Alive: **{len(alive)}**")
    L.append(f"- Free-tier evidence (免费/注册送/签到/free…): **{sum(1 for r in alive if r['free_evidence'])}**")
    L.append(f"- Live model lists confirmed via /models: **{sum(1 for r in alive if r['api_models'])}**")
    L.append(f"- Discovered by the radar itself: **{sum(1 for r in rows if r['source'] == 'discovery')}**")

    L.append("\n## Target model coverage")
    L.append("\n*verified* = present in the provider's own /models response; *claim* = marketing copy only.")
    for m in core.TARGET_MODELS:
        pat = core.MODEL_PATTERNS[m]
        verified = [r["domain"] for r in alive
                    if r["api_models"] and any(re.search(pat, mid, re.I) for mid in r["api_models"])]
        claimed = [r["domain"] for r in alive
                   if m in r["models_claimed"] and r["domain"] not in verified]
        L.append(f"\n### {m}")
        L.append(f"- **verified live** ({len(verified)}): {', '.join(verified) or '—'}")
        L.append(f"- claim only ({len(claimed)}): {', '.join(claimed[:15]) or '—'}")

    L.append("\n## Top 20 providers by score")
    L.append("\n| score | provider | live models | free evidence | base_url |")
    L.append("|---|---|---|---|---|")
    for r in sorted(alive, key=lambda x: -x["score"])[:20]:
        base = core.api_base_url(r).replace("|", "/")
        L.append(f"| {r['score']} | {r['domain']} | {len(r['api_models'])} | "
                 f"{', '.join(r['free_evidence'][:3]) or '—'} | {base} |")

    mirrors = core.alias_groups()
    if mirrors:
        L.append("\n## Mirror groups (one gateway, many domains)")
        for t, ds in mirrors.items():
            L.append(f"- **{t}** → {', '.join(ds)}")

    new = sorted((r for r in rows if r["source"] == "discovery"), key=lambda x: -x["score"])[:20]
    if new:
        L.append("\n## Newest radar discoveries")
        for r in new:
            L.append(f"- {r['domain']} (score {r['score']}, alive={int(r['alive'])})")

    L.append("\n## ⚠️ Risk notes")
    L.append("- Model **names** on relays are not proof of model **identity** — official GPT-6 Astra /")
    L.append("  Fable 5 / Opus 5 are metered and expensive; 'free unlimited' relays use promos,")
    L.append("  shared accounts or relabels.")
    L.append("- Unofficial relays log your prompts. Never route credentials, private repos or")
    L.append("  confidential data through them. Register with unique passwords; skip OAuth where possible.")
    L.append("- Free relay endpoints die weekly — re-run **Deep research** regularly; this digest is a")
    L.append("  snapshot at generation time.")
    return "\n".join(L)
