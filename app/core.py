from __future__ import annotations
import asyncio, csv, io, json, os, re, sqlite3, time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
import httpx
from bs4 import BeautifulSoup

DB_PATH = Path(os.getenv("DATABASE_PATH", "data/providers.db"))
TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "12"))
CONCURRENCY = int(os.getenv("SCAN_CONCURRENCY", "12"))
UA = os.getenv("USER_AGENT", "FleeceRadar/1.0 (+passive discovery; no credentials)")

MODEL_PATTERNS = {
    "GPT-6 Astra": r"gpt[\s._-]*6[\s._-]*astra",
    "GPT-5.6 Sol": r"gpt[\s._-]*5[\s._-]*6[\s._-]*sol",
    "Claude Fable 5": r"(?:claude[\s._-]*)?fable[\s._-]*5(?:\.1)?",
    "Claude Opus 5": r"(?:claude[\s._-]*)?opus[\s._-]*5",
    "DeepSeek V4 Flash": r"deepseek[\s._-]*v?4[\s._-]*flash",
    "DeepSeek V4": r"deepseek[\s._-]*v?4",
    "GLM-5.3 Flash": r"glm[\s._-]*5[\s._-]*3[\s._-]*flash",
    "GLM": r"\bglm[\s._-]*[45]",
    "Qwen": r"\bqwen(?:[\s._-]*3(?:\.\d+)?)?",
    "Kimi": r"\bkimi(?:[\s._-]*k?\d(?:\.\d+)?)?",
    "MiniMax": r"\bminimax\b",
    "Gemini": r"\bgemini\b",
    "Grok": r"\bgrok\b",
}
FREE_TERMS = ["免费", "公益", "白嫖", "注册送", "签到", "赠送额度", "free", "free tier", "trial credit", "0倍率", "0 倍率"]
API_TERMS = ["openai compatible", "openai兼容", "openai 格式", "/v1/chat/completions", "api gateway", "api网关", "new api", "new-api"]
RISK_TERMS = ["无限", "unlimited", "满血", "纯血", "稳定不跑路", "永久不限量", "秒到", "破解"]
PLATFORM_TERMS = {
    "New API": ["new-api", "new api", "newapi"],
    "One API": ["one-api", "one api", "oneapi"],
    "Veloera": ["veloera"],
    "VoAPI": ["voapi"],
    "Done Hub": ["done-hub", "donehub"],
    "OneHub": ["onehub"],
    "Sub2API": ["sub2api"],
    "Cherry Studio": ["cherry studio"],
}
# Models the user cares about most; presence in a /v1/models listing earns a scoring bonus.
TARGET_MODELS = ["Claude Fable 5", "Claude Opus 5", "GPT-6 Astra", "GPT-5.6 Sol", "DeepSeek V4 Flash", "GLM-5.3 Flash"]
REG_PATHS = ["/register", "/sign-up", "/signup", "/login", "/sign-in"]
PUBLIC_PATHS = ["/api/status", "/api/notice", "/v1/models", "/api/models", "/api/v1/models"]
MODELS_ENDPOINTS = ["/v1/models", "/api/models", "/api/v1/models"]
DOMAIN_KW = re.compile(r"(api|ai|token|relay|route|router|hub|model|chat|free|key|code|claude|gpt|deepseek|qwen|glm|kimi|llm|oai)", re.I)


@dataclass
class Finding:
    url: str
    final_url: str = ""
    domain: str = ""
    title: str = ""
    status_code: int = 0
    alive: bool = False
    free_evidence: list[str] = field(default_factory=list)
    models_claimed: list[str] = field(default_factory=list)
    api_compatible: bool = False
    registration_url: str = ""
    public_endpoints: dict[str, int] = field(default_factory=dict)
    risk_flags: list[str] = field(default_factory=list)
    platform: str = ""
    api_models: list[str] = field(default_factory=list)
    latency_ms: int = 0
    score: int = 0
    source: str = "seed"
    checked_at: str = ""
    error: str = ""


def utcnow(): return datetime.now(timezone.utc).isoformat()

def normalize_url(raw: str) -> str:
    raw = raw.strip().strip("<>()[]{}.,;\"'")
    if not raw: return ""
    if not raw.startswith(("http://", "https://")): raw = "https://" + raw
    p = urlparse(raw)
    if not p.netloc: return ""
    host = p.netloc.lower().split("@")[-1]
    # Refuse loopback/private/link-local targets — the scanner only probes public gateways.
    hostname = host.split(":")[0]
    try:
        import ipaddress
        if ipaddress.ip_address(hostname).is_private or ipaddress.ip_address(hostname).is_loopback or ipaddress.ip_address(hostname).is_link_local:
            return ""
    except ValueError:
        if hostname in ("localhost",) or hostname.endswith(".local"): return ""
    path = re.sub(r"/{2,}", "/", p.path or "/")
    return urlunparse((p.scheme.lower(), host, path, "", p.query, ""))

def canonical_domain(url: str) -> str:
    d = urlparse(url).netloc.lower().split(":")[0]
    return d[4:] if d.startswith("www.") else d

def extract_urls(text: str) -> list[str]:
    found = re.findall(r"https?://[^\s<>\]\[\"']+", text)
    out = []; seen = set()
    for u in found:
        n = normalize_url(u)
        if n and n not in seen:
            seen.add(n); out.append(n)
    return out

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS providers(
          domain TEXT PRIMARY KEY,url TEXT,final_url TEXT,title TEXT,status_code INTEGER,alive INTEGER,
          free_evidence TEXT,models_claimed TEXT,api_compatible INTEGER,registration_url TEXT,
          public_endpoints TEXT,risk_flags TEXT,score INTEGER,source TEXT,checked_at TEXT,error TEXT)""")
        cols = {r[1] for r in c.execute("PRAGMA table_info(providers)")}
        if "platform" not in cols: c.execute("ALTER TABLE providers ADD COLUMN platform TEXT DEFAULT ''")
        if "api_models" not in cols: c.execute("ALTER TABLE providers ADD COLUMN api_models TEXT DEFAULT '[]'")
        if "latency_ms" not in cols: c.execute("ALTER TABLE providers ADD COLUMN latency_ms INTEGER DEFAULT 0")

def save_finding(f: Finding):
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""INSERT INTO providers(domain,url,final_url,title,status_code,alive,free_evidence,
        models_claimed,api_compatible,registration_url,public_endpoints,risk_flags,platform,api_models,
        latency_ms,score,source,checked_at,error) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(domain) DO UPDATE SET url=excluded.url,final_url=excluded.final_url,title=excluded.title,
        status_code=excluded.status_code,alive=excluded.alive,free_evidence=excluded.free_evidence,
        models_claimed=excluded.models_claimed,api_compatible=excluded.api_compatible,
        registration_url=excluded.registration_url,public_endpoints=excluded.public_endpoints,
        risk_flags=excluded.risk_flags,platform=excluded.platform,api_models=excluded.api_models,
        latency_ms=excluded.latency_ms,score=excluded.score,source=excluded.source,
        checked_at=excluded.checked_at,error=excluded.error""", (
        f.domain, f.url, f.final_url, f.title, f.status_code, int(f.alive), json.dumps(f.free_evidence, ensure_ascii=False),
        json.dumps(f.models_claimed, ensure_ascii=False), int(f.api_compatible), f.registration_url,
        json.dumps(f.public_endpoints), json.dumps(f.risk_flags, ensure_ascii=False), f.platform,
        json.dumps(f.api_models, ensure_ascii=False), f.latency_ms, f.score, f.source, f.checked_at, f.error))

def list_findings(q="", model="", alive_only=False, limit=1000):
    init_db(); sql = "SELECT * FROM providers WHERE 1=1"; args = []
    if q: sql += " AND (domain LIKE ? OR title LIKE ? OR free_evidence LIKE ?)"; args += [f"%{q}%"] * 3
    if model: sql += " AND models_claimed LIKE ?"; args.append(f"%{model}%")
    if alive_only: sql += " AND alive=1"
    sql += " ORDER BY score DESC, domain LIMIT ?"; args.append(limit)
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row; rows = c.execute(sql, args).fetchall()
    result = []
    for r in rows:
        x = dict(r)
        for k in ["free_evidence", "models_claimed", "public_endpoints", "risk_flags", "api_models"]:
            x[k] = json.loads(x[k] or "[]")
        x.setdefault("platform", "")
        x["alive"] = bool(x["alive"]); x["api_compatible"] = bool(x["api_compatible"])
        result.append(x)
    return result

def alias_groups():
    """Group providers that share the same page title — likely mirrors of one gateway
    (e.g. dawcode.com / dawcode.ai / dawclaudecode.com, sheapi.cc / sheapi.top,
    api.hcnsec.cn / api.iamhc.cn, rntm.sh / runtime.badtheorylabs.com)."""
    groups = {}
    for r in list_findings(limit=100000):
        if not r["alive"] or not r["title"]: continue
        t = re.sub(r"\s*[-|·]\s*(登录|注册|管理系统|New API|new-api|Veloera|One API|one-api|UI).*$", "", r["title"]).strip()
        if len(t) < 3: continue
        groups.setdefault(t.lower(), []).append(r["domain"])
    # A "group" of many domains sharing a default title (e.g. bare "New API")
    # is platform defaulting, not one operator — drop those.
    return {t: sorted(ds) for t, ds in groups.items()
            if 1 < len(ds) <= 8 and t not in {"new api", "one api", "new-api", "one-api"}}

async def get(client, url):
    try: return await client.get(url, follow_redirects=True)
    except Exception: return None

async def scan_provider(client: httpx.AsyncClient, raw: str, source="seed") -> Finding:
    url = normalize_url(raw)
    f = Finding(url=url, domain=canonical_domain(url), source=source, checked_at=utcnow())
    if not url: f.error = "invalid URL"; return f
    try:
        t0 = time.perf_counter()
        r = await client.get(url, follow_redirects=True)
        f.latency_ms = int((time.perf_counter() - t0) * 1000)
        f.status_code = r.status_code
        f.final_url = str(r.url)
        f.alive = r.status_code < 500
        # Redirect targets (e.g. directory /go/ links, api.iamhc.cn -> api.hcnsec.cn)
        # are the real provider — re-key by final domain.
        final_domain = canonical_domain(f.final_url)
        if final_domain and final_domain != f.domain: f.domain = final_domain
        ctype = r.headers.get("content-type", "")
        text = r.text[:1_500_000] if ("text" in ctype or "json" in ctype or not ctype) else ""
        soup = BeautifulSoup(text, "html.parser")
        f.title = (soup.title.get_text(" ", strip=True) if soup.title else "")[:200]
        clean = " ".join(soup.get_text(" ", strip=True).split())[:500_000]
        lower = clean.lower()
        f.free_evidence = [t for t in FREE_TERMS if t.lower() in lower]
        f.models_claimed = [name for name, pat in MODEL_PATTERNS.items() if re.search(pat, clean, re.I)]
        f.api_compatible = any(t in lower for t in API_TERMS)
        f.risk_flags = [t for t in RISK_TERMS if t.lower() in lower]
        for name, terms in PLATFORM_TERMS.items():
            if any(t in lower for t in terms): f.platform = name; break
        for a in soup.find_all("a", href=True):
            href = urljoin(f.final_url or url, a["href"])
            label = (a.get_text(" ", strip=True) + " " + href).lower()
            if any(x in label for x in ["register", "sign-up", "signup", "注册"]): f.registration_url = href; break
        base = f"{urlparse(f.final_url or url).scheme}://{urlparse(f.final_url or url).netloc}"
        for path in PUBLIC_PATHS:
            rr = await get(client, base + path)
            if rr is not None: f.public_endpoints[path] = rr.status_code
        # Parse unauthenticated /v1/models | /api/models | /api/v1/models JSON for concrete model IDs.
        for path in MODELS_ENDPOINTS:
            if f.public_endpoints.get(path) != 200: continue
            resp = await get(client, base + path)
            if resp is None: continue
            try:
                data = resp.json()
            except Exception:
                continue
            items = data.get("data", data) if isinstance(data, dict) else data
            ids = sorted({m.get("id") for m in items if isinstance(m, dict) and m.get("id")})
            if ids:
                f.api_models = ids[:500]; f.api_compatible = True
                break
        target_hits = [name for name in TARGET_MODELS if any(re.search(MODEL_PATTERNS[name], mid, re.I) for mid in f.api_models)]
        f.models_claimed = sorted(set(f.models_claimed) | set(target_hits))
        f.score = max(0, min(100, (25 if f.alive else 0) + (20 if f.free_evidence else 0)
            + min(25, 5 * len(f.models_claimed)) + (15 if f.api_compatible else 0)
            + (10 if any(v == 200 for v in f.public_endpoints.values()) else 0)
            + (5 if f.registration_url else 0) + (10 if target_hits else 0)
            + min(5, len(f.api_models) // 20 if f.api_models else 0)
            - min(20, 5 * len(f.risk_flags))))
    except Exception as e:
        f.error = f"{type(e).__name__}: {e}"[:300]
    return f

async def scan_many(urls: list[str], source="seed"):
    sem = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient(timeout=TIMEOUT, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}) as client:
        async def one(u):
            async with sem:
                f = await scan_provider(client, u, source); save_finding(f); return f
        return await asyncio.gather(*(one(u) for u in urls))

SKIP_NETLOCS = ("github.com", "docs.", "medium.com", "segmentfault", "cnblogs", "csdn.net",
                "youtube.com", "bilibili.com", "zhihu.com", "x.com", "twitter.com",
                "facebook.com", "telegram.org", "t.me", "wikipedia.org", "weibo.com",
                "reddit.com", "huggingface.co", "cloud.tencent.com")

async def discover_directory(url: str) -> list[str]:
    """Crawl a directory page and extract outbound provider-looking links.

    Two signals: (1) links labelled 注册/register/sign-up/前往 or carrying aff=/ref=
    params; (2) external links whose label or domain looks like an AI gateway
    (api/ai/token/relay/... keywords) — this is what makes apiindex.me /
    apisou.com / baipiao.org style listing pages yield candidates."""
    async with httpx.AsyncClient(timeout=TIMEOUT, headers={"User-Agent": UA}) as client:
        try:
            r = await client.get(url, follow_redirects=True)
            soup = BeautifulSoup(r.text, "html.parser"); base = str(r.url)
            own = urlparse(base).netloc.lower()
            out = []
            for a in soup.find_all("a", href=True):
                href = urljoin(base, a["href"])
                label = " ".join(a.get_text(" ", strip=True).split()).lower()
                if urlparse(href).scheme not in ("http", "https"): continue
                netloc = urlparse(href).netloc.lower()
                if netloc == own or netloc in SKIP_NETLOCS or any(netloc.endswith("." + s) for s in ("github.com", "csdn.net")):
                    continue
                is_signup = any(x in label for x in ["注册", "register", "sign up", "sign-up", "前往"]) or "aff=" in href or "ref=" in href
                looks_like = bool(DOMAIN_KW.search(label) or DOMAIN_KW.search(netloc.lstrip("www.")))
                if is_signup or looks_like:
                    out.append(href)
            return list(dict.fromkeys(out))
        except Exception:
            return []

async def discover_all(directory_urls: list[str], queries: list[str] | None = None, scan=False) -> list[str]:
    found = []
    for u in directory_urls: found.extend(await discover_directory(u))
    for q in (queries or []): found.extend(await discover_search(q))
    found = list(dict.fromkeys(found))
    found = [u for u in found if not any(s in urlparse(u).netloc for s in SKIP_NETLOCS)]
    if found:
        if scan: await scan_many(found, "discovery")
        else:
            for u in found:
                save_finding(Finding(url=u, domain=canonical_domain(u), source="discovery", checked_at=utcnow()))
    return found

async def discover_search(query: str, count=20) -> list[str]:
    brave = os.getenv("BRAVE_SEARCH_API_KEY")
    if not brave: return []
    async with httpx.AsyncClient(timeout=TIMEOUT, headers={"X-Subscription-Token": brave, "Accept": "application/json"}) as c:
        r = await c.get("https://api.search.brave.com/res/v1/web/search", params={"q": query, "count": min(count, 20)})
        r.raise_for_status()
        return [x["url"] for x in r.json().get("web", {}).get("results", []) if x.get("url")]

def export_csv(rows):
    buf = io.StringIO()
    fields = ["domain", "url", "final_url", "title", "alive", "status_code", "score", "free_evidence",
              "models_claimed", "api_compatible", "registration_url", "risk_flags", "checked_at"]
    w = csv.DictWriter(buf, fieldnames=fields); w.writeheader()
    for r in rows:
        x = {k: r.get(k, "") for k in fields}
        for k in ["free_evidence", "models_claimed", "risk_flags"]: x[k] = " | ".join(x[k])
        w.writerow(x)
    return buf.getvalue()

def api_base_url(r) -> str:
    """Best-effort OpenAI-compatible base URL for OmniRoute: origin + the
    prefix that actually served /models (e.g. https://host/v1)."""
    p = urlparse(r.get("final_url") or r["url"])
    origin = f"{p.scheme}://{p.netloc}"
    eps = r.get("public_endpoints") or {}
    for path in ("/v1/models", "/api/v1/models", "/api/models"):
        if eps.get(path) == 200:
            return origin + re.sub(r"models$", "", path)
    return origin

def export_omniroute(rows):
    """OmniRoute-ready JSON: alive OpenAI-compatible providers with discovered model ids."""
    out = []
    for r in sorted(rows, key=lambda x: -x["score"]):
        if not r.get("alive"): continue
        out.append({
            "name": r["domain"],
            "base_url": api_base_url(r),
            "platform": r.get("platform", ""),
            "api_compatible": bool(r.get("api_compatible")),
            "score": r["score"],
            "models": r.get("api_models", []),
            "models_claimed": r.get("models_claimed", []),
            "target_models": [m for m in TARGET_MODELS if m in r.get("models_claimed", [])],
            "free_evidence": r.get("free_evidence", []),
            "registration_url": r.get("registration_url", ""),
            "risk_flags": r.get("risk_flags", []),
            "checked_at": r.get("checked_at", ""),
            "note": "models are as listed by the provider's /models endpoint; identity unverified",
        })
    return json.dumps(out, ensure_ascii=False, indent=2)
