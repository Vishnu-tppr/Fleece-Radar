import asyncio
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path
from fastapi.testclient import TestClient
from app.core import Finding, save_finding, list_findings, alias_groups, export_csv
from app.main import app
import app.cli as cli
import app.research as research

def test_db_save_and_query(tmp_path):
    f = Finding(
        url="https://test-unique-provider.ai",
        domain="test-unique-provider.ai",
        final_url="https://test-unique-provider.ai",
        title="Test Provider - Free Tier",
        status_code=200,
        alive=True,
        free_evidence=["免费", "注册送"],
        models_claimed=["Claude Opus 5"],
        api_compatible=True,
        score=90,
        source="test"
    )
    save_finding(f)

    # query by q
    res_q = list_findings(q="test-unique-provider")
    assert any(r["domain"] == "test-unique-provider.ai" for r in res_q)

    # query by model
    res_m = list_findings(model="Opus")
    assert any(r["domain"] == "test-unique-provider.ai" for r in res_m)

    # query alive
    res_a = list_findings(alive_only=True)
    assert any(r["domain"] == "test-unique-provider.ai" for r in res_a)

    # export csv
    csv_text = export_csv([res_q[0]])
    assert "test-unique-provider.ai" in csv_text

def test_alias_groups_filtering():
    groups = alias_groups()
    assert isinstance(groups, dict)
    # verify that generic names like "New API" or "One API" are filtered out
    for k in groups.keys():
        assert k not in {"new api", "one api", "new-api", "one-api"}
        assert len(k) >= 3

def test_cli_load_seeds(tmp_path, monkeypatch):
    seeds_file = tmp_path / "seeds.txt"
    seeds_file.write_text("https://foo.com\n# comment\nhttps://bar.com\nhttps://foo.com\n")
    monkeypatch.setattr(cli, "SEEDS", seeds_file)

    loaded = cli.load_seeds()
    assert loaded == ["https://foo.com", "https://bar.com"]

def test_cli_export(tmp_path, monkeypatch):
    out_csv = tmp_path / "out.csv"
    monkeypatch.setattr("sys.argv", ["fleece-radar", "export", str(out_csv), "--format", "csv"])
    cli.main()
    assert out_csv.exists()
    assert "domain,url" in out_csv.read_text(encoding="utf-8")

    out_omni = tmp_path / "out.json"
    monkeypatch.setattr("sys.argv", ["fleece-radar", "export", str(out_omni), "--format", "omniroute"])
    cli.main()
    assert out_omni.exists()
    assert json.loads(out_omni.read_text(encoding="utf-8"))

    out_txt = tmp_path / "out.txt"
    monkeypatch.setattr("sys.argv", ["fleece-radar", "export", str(out_txt), "--format", "txt", "--alive"])
    cli.main()
    assert out_txt.exists()

def test_cli_merge_seeds(tmp_path, monkeypatch):
    seeds_file = tmp_path / "seeds.txt"
    seeds_file.write_text("https://foo.com\n")
    monkeypatch.setattr(cli, "SEEDS", seeds_file)

    monkeypatch.setattr("sys.argv", ["fleece-radar", "merge-seeds", "https://foo.com", "https://bar.com"])
    cli.main()

    content = seeds_file.read_text(encoding="utf-8")
    assert "https://bar.com" in content

@pytest.mark.asyncio
async def test_deep_research_mocked():
    with patch("app.research.QUERIES", ["test query"]):
        with patch("app.research.DIRECTORIES", []):
            with patch("app.research.bing_search", new_callable=AsyncMock) as m_bing:
                m_bing.return_value = ["https://new-found-gateway.ai"]
                with patch("app.research.ddg_search", new_callable=AsyncMock) as m_ddg:
                    m_ddg.return_value = []
                with patch("app.research.searxng_search", new_callable=AsyncMock) as m_searx:
                    m_searx.return_value = []
                with patch("app.research.mojeek_search", new_callable=AsyncMock) as m_moj:
                    m_moj.return_value = []
                with patch("app.research.brave_search", new_callable=AsyncMock) as m_brave:
                    m_brave.return_value = []
                with patch("app.research.github_feed", new_callable=AsyncMock) as m_gh:
                    m_gh.return_value = []
                with patch("app.research.linuxdo_feed", new_callable=AsyncMock) as m_ld:
                    m_ld.return_value = []
                with patch("app.core.scan_many", new_callable=AsyncMock) as m_scan:
                    m_scan.return_value = [
                        Finding(url="https://new-found-gateway.ai", domain="new-found-gateway.ai", alive=True)
                    ]

                    res = await research.deep_research(max_context_pages=0, max_scan=5)
                    assert res["raw_hits"] >= 1
                    assert "new-found-gateway.ai" in res["new_domains"]

def test_api_jobs_not_found():
    client = TestClient(app)
    r = client.get("/api/jobs/nonexistent-id")
    assert r.status_code == 404

def test_api_scan_seeds():
    client = TestClient(app)
    with patch("app.main.scan_many", new_callable=AsyncMock) as m_scan:
        m_scan.return_value = []
        r = client.post("/api/scan-seeds")
        assert r.status_code == 200
        assert "job_id" in r.json()
