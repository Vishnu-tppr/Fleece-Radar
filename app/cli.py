import argparse, asyncio
from pathlib import Path
from .core import canonical_domain, discover_directory, discover_search, export_csv, export_omniroute, extract_urls, list_findings, scan_many

SEEDS = Path("data/seeds.txt")

def load_seeds():
    urls = []
    if SEEDS.exists():
        for line in SEEDS.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"): urls.append(line)
    return list(dict.fromkeys(urls))

def build_exports(out_dir: Path = Path("export")):
    """Mirror of legacy radar.py build_exports: write omniroute.json + providers.env + providers.csv to out_dir."""
    import re
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = list_findings(limit=100000)
    alive = [r for r in rows if r["alive"]]

    # omniroute.json
    provs = []
    for r in rows:
        if not r["alive"]:
            continue
        base = r.get("final_url") or r["url"]
        provs.append({
            "name": r["domain"].split(".")[0],
            "domain": r["domain"],
            "base_url": base,
            "api": "openai-compatible",
            "free": bool(r["free_evidence"]),
            "free_evidence": r["free_evidence"],
            "models": r["api_models"][:60] or r["models_claimed"][:60],
            "families": list(dict.fromkeys(f[0] for f in [] )),  # placeholder
            "title": r["title"],
            "url": r["url"],
            "score": r["score"],
        })
    (out_dir / "omniroute.json").write_text(
        _json({"generated": _now_iso(), "count": len(provs), "providers": provs}), encoding="utf-8")

    # providers.env
    lines = [f"# Fleece Radar export — {_now_iso()}", f"# {len(provs)} working providers", ""]
    for i, r in enumerate(alive, 1):
        slug = re.sub(r"[^A-Z0-9]", "_", r["domain"].split(".")[0].upper())
        models = ",".join(r["api_models"][:20] or r["models_claimed"][:20])
        lines += [
            f"PROV_{i}_{slug}_BASE_URL={r.get('final_url') or r['url']}",
            f"PROV_{i}_{slug}_FREE={'true' if r['free_evidence'] else 'false'}",
            f"PROV_{i}_{slug}_MODELS={models}",
            "",
        ]
    (out_dir / "providers.env").write_text("\n".join(lines), encoding="utf-8")

    # providers.csv
    (out_dir / "providers.csv").write_text(export_csv(alive), encoding="utf-8")
    return out_dir

def _now_iso():
    import datetime as dt
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")

def _json(obj):
    import json
    return json.dumps(obj, ensure_ascii=False, indent=1)

def main():
    p = argparse.ArgumentParser(prog="fleece-radar")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("export-build", help="Mirror legacy radar.py build_exports into export/")
    s = sub.add_parser("scan"); s.add_argument("inputs", nargs="+"); s.add_argument("--source", default="cli")
    d = sub.add_parser("discover"); d.add_argument("urls", nargs="*"); d.add_argument("--query", action="append", default=[]); d.add_argument("--no-scan", action="store_true")
    e = sub.add_parser("export"); e.add_argument("path"); e.add_argument("--format", choices=["txt", "csv", "omniroute"], default="txt"); e.add_argument("--alive", action="store_true")
    m = sub.add_parser("merge-seeds"); m.add_argument("inputs", nargs="+")
    args = p.parse_args()
    if args.cmd == "scan":
        urls = []
        for x in args.inputs:
            f = Path(x)
            urls += extract_urls(f.read_text(encoding="utf-8")) if f.is_file() else [x]
        out = asyncio.run(scan_many(list(dict.fromkeys(urls)), args.source)); print(f"scanned={len(out)} alive={sum(x.alive for x in out)}")
    elif args.cmd == "discover":
        async def run():
            found = []
            for u in args.urls: found.extend(await discover_directory(u))
            for q in args.query: found.extend(await discover_search(q))
            found = list(dict.fromkeys(found)); print("\n".join(found))
            if found and not args.no_scan: await scan_many(found, "discovery")
        asyncio.run(run())
    elif args.cmd == "merge-seeds":
        existing = {canonical_domain(u) for u in load_seeds()}
        new = []
        for x in args.inputs:
            f = Path(x)
            for u in (extract_urls(f.read_text(encoding="utf-8")) if f.is_file() else [x]):
                if canonical_domain(u) not in existing:
                    existing.add(canonical_domain(u)); new.append(u)
        if new:
            with SEEDS.open("a", encoding="utf-8") as fh: fh.write("\n".join(new) + "\n")
        print(f"added={len(new)}")
    elif args.cmd == "export-build":
        d = build_exports()
        print(f"exported to {d}")
    else:
        rows = list_findings(alive_only=args.alive, limit=100000)
        path = Path(args.path); path.parent.mkdir(parents=True, exist_ok=True)
        if args.format == "csv": path.write_text(export_csv(rows), encoding="utf-8")
        elif args.format == "omniroute": path.write_text(export_omniroute(rows), encoding="utf-8")
        else: path.write_text("\n".join(r["final_url"] or r["url"] for r in rows) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()