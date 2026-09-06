# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Existing codebase: Python 3 + FastAPI backend, SQLite storage, single-file vanilla JS/HTML/CSS frontend (`app/static/index.html`). FastAPI serves both the JSON API and the UI.

## Users

A single technical operator (the owner) running this locally on their own machine. They hunt for Chinese/community AI API gateways ("中转站", New API / One API style public instances) that advertise free tiers, so they can plug candidates into OmniRoute as upstream providers. Expert user; comfortable with raw data, JSON, and CLI workflows.

## Product Purpose

Passively discover, scan, score, and monitor candidate AI API gateway providers. It fetches directory listings and seed URLs, probes provider homepages and unauthenticated public endpoints (`/v1/models`, `/api/status`), extracts evidence of free tiers, claimed models, platform type, and risk signals, then stores, scores, deduplicates (mirror/alias grouping), and exposes the results via a dashboard UI plus JSON/TXT/CSV exports. Success = the operator can, in minutes, pick trustworthy-looking free-tier candidates for a target model and export them into OmniRoute.

## Positioning

Passive, evidence-labeling discovery: it records what providers *claim* (models, free tiers, "unlimited" promises) and what public endpoints expose, never asserting model authenticity or real quota — a distinction no simple directory site makes.

## Operating Context

- Local single-service FastAPI deployment on Windows; SQLite in `data/providers.db`; seed list in `data/seeds.txt`.
- Background scan jobs with progress polling; optional periodic auto-refresh via `REFRESH_HOURS`.
- Data sources: Chinese gateway directories (apiindex.me, apisou.com, apiranking.com, awesome-ai-proxy lists) and pasted URL lists.
- Output feeds OmniRoute: JSON export with `base_url`, `platform`, `models`, `target_models`, `risk_flags`.
- Content is bilingual (Chinese gateway pages, English UI); model names include Claude Fable 5, Claude Opus 5, GPT-6 Astra, GPT-5.6 Sol, DeepSeek V4 Flash, GLM-5.3 Flash, Qwen.

## Capabilities and Constraints

- Capabilities: URL/seed scanning with concurrency limits; homepage claim extraction (free-tier terms, model names, platform detection, risk flags); unauthenticated `/v1/models` JSON parsing for concrete model IDs; redirect resolution and re-keying to final domain; mirror grouping by normalized page title; scoring; TXT/CSV/OmniRoute JSON export; background jobs.
- Constraints: passive only — no account creation, no credentials, no authenticated inference, no quota evasion. Never sends API keys. Scans are rate-limited (default concurrency 12) to stay polite.
- Trust model: marketing claims are labeled as claims. Risk flags (e.g. "无限", "满血", "破解") mark suspect providers rather than being hidden.
- Undecided: none material at this time.

## Brand Commitments

None recorded. Name "China AI Provider Finder" is the working title.

## Evidence on Hand

- Working scanner, DB, API, and dashboard (`app/`), seed list (`data/seeds.txt`), research notes (`perplexity-deepresearch.md`, project `claude.md`).
- No marketing assets, testimonials, or fabricated proof may be added; all data is real scan output.

## Product Principles

1. Evidence over assertion — every displayed claim traces to a scan observation; uncertainty stays visible.
2. Safety first — passive probing only, politeness-limited, no credentials ever.
3. Speed to decision — the operator's job is picking candidates fast; surfaces optimize scan/filter/export loops.
4. Handle the mirror mess — deduplication and alias grouping are first-class, not an afterthought.

## Accessibility & Inclusion

No product-specific requirements recorded; standard web accessibility baseline applies.
