import json
import pytest
from fastapi.testclient import TestClient
from app.core import api_base_url, alias_groups, canonical_domain, extract_urls, normalize_url, export_omniroute
from app.main import app
from app.research import looks_like_gateway, research_report_md

def test_normalize():
    assert normalize_url("example.com") == "https://example.com/"
    assert canonical_domain("https://www.example.com/x") == "example.com"
    # test stripping loopback/private IPs
    assert normalize_url("http://127.0.0.1:8000") == ""
    assert normalize_url("http://192.168.1.1") == ""

def test_extract_dedupe():
    assert extract_urls("https://a.test/ https://a.test/") == ["https://a.test/"]
    assert len(extract_urls("Visit https://foo.ai and https://bar.ai")) == 2

def test_api_base_url():
    # Test fallback to origin
    r1 = {"url": "https://api.example.com", "public_endpoints": {}}
    assert api_base_url(r1) == "https://api.example.com"

    # Test /v1/models detection -> strips 'models' to yield https://api.example.com/v1/
    r2 = {"url": "https://api.example.com", "public_endpoints": {"/v1/models": 200}}
    assert api_base_url(r2) == "https://api.example.com/v1/"

    # Test /api/v1/models detection
    r3 = {"url": "https://api.example.com", "public_endpoints": {"/api/v1/models": 200}}
    assert api_base_url(r3) == "https://api.example.com/api/v1/"

def test_omniroute_export():
    rows = [{
        "domain": "test.ai",
        "url": "https://test.ai",
        "final_url": "https://test.ai",
        "alive": True,
        "score": 85,
        "platform": "New API",
        "api_compatible": True,
        "api_models": ["gpt-4", "claude-3"],
        "models_claimed": ["Claude Opus 5"],
        "free_evidence": ["免费"],
        "public_endpoints": {"/v1/models": 200},
        "registration_url": "https://test.ai/register",
        "risk_flags": [],
        "checked_at": "2026-09-06T12:00:00Z"
    }]
    exported_str = export_omniroute(rows)
    exported = json.loads(exported_str)
    assert len(exported) == 1
    assert exported[0]["name"] == "test.ai"
    assert exported[0]["base_url"] == "https://test.ai/v1/"
    assert "Claude Opus 5" in exported[0]["target_models"]

def test_looks_like_gateway():
    assert looks_like_gateway("https://api.relayhub.com", "api.relayhub.com") is True
    assert looks_like_gateway("https://github.com/mn-api", "github.com") is False
    assert looks_like_gateway("https://something.com/register?aff=123", "something.com") is True
    assert looks_like_gateway("https://randomsite.org/about", "randomsite.org") is False

def test_research_report_md():
    report = research_report_md()
    assert "Fleece Radar" in report or "薅羊毛雷达" in report
    assert "Target model coverage" in report
    assert "Top 20 providers by score" in report

def test_dashboard():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Fleece Radar" in r.text
    assert "JetBrains Mono" in r.text
    assert "stat-total" in r.text
    assert "stat-models" in r.text
    assert "btn-discover" in r.text
    assert "btn-deep" in r.text

def test_api_providers():
    client = TestClient(app)
    r = client.get("/api/providers?limit=10")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 10

def test_api_aliases():
    client = TestClient(app)
    r = client.get("/api/aliases")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)

def test_api_exports():
    client = TestClient(app)
    r_txt = client.get("/api/export.txt")
    assert r_txt.status_code == 200

    r_csv = client.get("/api/export.csv")
    assert r_csv.status_code == 200
    assert "domain,url" in r_csv.text

    r_omni = client.get("/api/export.omniroute")
    assert r_omni.status_code == 200
    assert isinstance(r_omni.json(), list)

    r_md = client.get("/api/research.md")
    assert r_md.status_code == 200
    assert "Fleece Radar" in r_md.text

def test_api_scan_validation():
    client = TestClient(app)
    r = client.post("/api/scan", json={"urls": []})
    assert r.status_code == 400
