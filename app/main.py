from __future__ import annotations
import asyncio, json, logging, os, uuid
from pathlib import Path
from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .core import alias_groups, discover_directory, discover_search, export_csv, export_omniroute, extract_urls, init_db, list_findings, scan_many
from .research import deep_research, research_report_md

app = FastAPI(title="Fleece Radar — 薅羊毛雷达", version="1.0.0")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
jobs = {}
REFRESH_HOURS = float(os.getenv("REFRESH_HOURS", "0"))  # 0 = disabled

async def refresh_loop():
    """Periodic re-scan of all known providers to keep health/data fresh."""
    while True:
        await asyncio.sleep(REFRESH_HOURS * 3600)
        try:
            domains = [r["url"] or f"https://{r['domain']}" for r in list_findings(limit=5000)]
            await scan_many(domains, "refresh")
        except Exception:
            logging.getLogger("uvicorn.error").exception("refresh_loop scan failed")

class ScanRequest(BaseModel):
    urls: list[str]
    source: str = "api"

class DiscoverRequest(BaseModel):
    directory_urls: list[str] = []
    queries: list[str] = []
    scan: bool = True

@app.get("/", response_class=HTMLResponse)
def home():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/api/providers")
def providers(q: str = "", model: str = "", alive: bool = False, limit: int = Query(500, le=5000)):
    return list_findings(q, model, alive, limit)

@app.post("/api/scan")
async def scan(req: ScanRequest, background_tasks: BackgroundTasks):
    urls = list(dict.fromkeys(filter(None, (u.strip() for u in req.urls))))
    if not urls: raise HTTPException(400, "No URLs supplied")
    jid = str(uuid.uuid4()); jobs[jid] = {"state": "queued", "total": len(urls), "done": 0}
    async def run():
        jobs[jid]["state"] = "running"
        result = await scan_many(urls, req.source)
        jobs[jid].update(state="complete", done=len(result), alive=sum(x.alive for x in result))
    background_tasks.add_task(run)
    return {"job_id": jid, "queued": len(urls)}

@app.post("/api/scan-text")
async def scan_text(text: str = Form(...)):
    urls = extract_urls(text); result = await scan_many(urls, "pasted")
    return {"found": len(urls), "alive": sum(x.alive for x in result)}

@app.post("/api/discover")
async def discover(req: DiscoverRequest):
    log = logging.getLogger("uvicorn.error")
    found = []
    for u in req.directory_urls:
        try: found.extend(await discover_directory(u))
        except Exception: log.exception("discover_directory failed: %s", u)
    for q in req.queries:
        try: found.extend(await discover_search(q))
        except Exception: log.exception("discover_search failed: %s", q)
    found = list(dict.fromkeys(found))
    if req.scan and found: await scan_many(found, "discovery")
    return {"count": len(found), "urls": found}

@app.get("/api/jobs/{job_id}")
def job(job_id: str):
    if job_id not in jobs: raise HTTPException(404, "Unknown job")
    return jobs[job_id]

@app.get("/api/aliases")
def aliases():
    return alias_groups()

@app.post("/api/scan-seeds")
async def scan_seeds(background_tasks: BackgroundTasks):
    """Scan everything in data/seeds.txt (used by UI button and refresh loop bootstrap)."""
    seeds = Path("data/seeds.txt")
    if not seeds.exists(): seeds = Path(__file__).parent.parent / "data" / "seeds.txt"
    urls = [l.strip() for l in seeds.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    urls = list(dict.fromkeys(urls))
    jid = str(uuid.uuid4()); jobs[jid] = {"state": "queued", "total": len(urls), "done": 0}
    async def run():
        jobs[jid]["state"] = "running"
        result = await scan_many(urls, "seed")
        jobs[jid].update(state="complete", done=len(result), alive=sum(x.alive for x in result))
    background_tasks.add_task(run)
    return {"job_id": jid, "queued": len(urls)}

@app.post("/api/deep-research")
async def deep_research_api():
    """Free keyless deep-research pass: search backends + community feeds +
    directory crawls + one-hop page expansion, then scans all new candidates.
    May take 1-3 minutes."""
    return await deep_research()

@app.get("/api/research.md")
def research_md():
    return PlainTextResponse(research_report_md(), media_type="text/markdown",
                             headers={"Content-Disposition": "attachment; filename=fleece-radar-report.md"})

@app.get("/api/export.csv")
def csv_export():
    data = export_csv(list_findings(limit=100000))
    return PlainTextResponse(data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=providers.csv"})

@app.get("/api/export.txt")
def txt_export():
    rows = list_findings(alive_only=True, limit=100000)
    return PlainTextResponse("\n".join(r["final_url"] or r["url"] for r in rows) + "\n",
                             headers={"Content-Disposition": "attachment; filename=providers.txt"})

@app.get("/api/export.omniroute")
def omniroute_export():
    data = export_omniroute(list_findings(limit=100000))
    return PlainTextResponse(data, media_type="application/json",
                             headers={"Content-Disposition": "attachment; filename=omniroute-providers.json"})
