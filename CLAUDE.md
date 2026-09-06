```markdown
You are an ECC assistant helping redesign and extend an existing Python + FastAPI project.

## Objective

Redesign and upgrade an existing AI gateway scraper + FastAPI web UI so it can:

- Discover and track **as many Chinese/community AI API gateways as reasonably possible**, especially ones with free signup credit, daily check-ins, or “公益站” style free tiers.
- Extract metadata about claimed access to frontier models (e.g., Claude Fable 5, Claude Opus 5, GPT‑5.6 Sol, GPT‑6 Astra, DeepSeek V4 Flash, GLM‑5.3 Flash, Qwen).
- Provide a clean UI and JSON API so I can plug these providers into **OmniRoute** as candidate upstreams.
- Handle mirrors and alternative domains correctly (e.g., `api.hcnsec.cn` vs `api.iamhc.cn`, DawCode’s multiple domains, SheApi mirrors).

**Important:** The scraper must treat “unlimited free frontier model access” as **marketing claims**, not facts. It should collect and label what providers *claim*, but never assume the model or quota are genuine.

---

## Project Context

- Tech stack: Python 3.x + FastAPI backend.
- Existing functionality: there is already a simple scraper that pulls some provider URLs and displays them on a FastAPI page.
- Target deployment: single service (FastAPI) with background jobs or scheduled tasks for scraping.
- You can assume a relational DB (e.g., PostgreSQL) is available; if you suggest schema changes, describe them.

If you need more project details (folder structure, current scraper implementation), ask me briefly, then continue.

---

## Data Sources & Discovery Strategy

Use the **search-first skill** to identify and inspect public directories and community lists of AI gateways, especially Chinese ones, such as:

- APIIndex (`apiindex.me`) user listings and “self‑publish” pages.
- mn-api/awesome-ai-proxy directory of main API relays.
- GetCheapAI or similar directories of third‑party AI API platforms.
- apisou, apiranking, and other Chinese “中转站排行榜/导航” sites.
- Any other relevant sources you find via search-first.

From these sources, design a discovery pipeline that can:

1. Fetch directory pages and extract candidate provider URLs.
2. Normalize them into canonical **providers** and **domain aliases** (e.g., multiple domains for the same gateway).
3. Optionally crawl each provider’s homepage to detect:
   - Language (Chinese vs international).
   - Mention of “免费”, “公益站”, “注册送”, “签到”, “白嫖”, “trial”, etc.
   - Mention of specific model names (Fable 5, Opus 5, GPT‑5.6 Sol, GPT‑6 Astra, DeepSeek V4 Flash, GLM‑5.3 Flash, Qwen).
   - Whether they expose an OpenAI‑style `/v1/models` or similar endpoint.

Do **not** send any real API keys or credentials. Only use anonymous HTTP requests for discovery.

---

## Data Model & Database Design (/plan)

Use `/plan` with the architect agent to propose and refine a data model. At minimum define:

- `Provider`:
  - `id`
  - `canonical_name`
  - `operator_name` (if known)
  - `homepage_url`
  - `is_chinese_operator` (bool or rating)
  - `source_tags` (which directories referenced it)
  - `risk_flags` (e.g., “unverified model identity”, “marketing-only unlimited”, “unknown operator”)
- `DomainAlias`:
  - `id`
  - `provider_id`
  - `domain`
  - `is_primary`
- `ModelClaim`:
  - `id`
  - `provider_id`
  - `model_name` (e.g., `claude-fable-5`, `claude-opus-5`, `gpt-5.6-sol`, `deepseek-v4-flash`)
  - `claim_type` (e.g., “marketing copy”, “directory listing”, “docs page”)
  - `is_frontier_model` (bool)
- `FreeTierMetadata`:
  - `id`
  - `provider_id`
  - `signup_bonus` (text, not trusted: e.g., “注册送 20 刀”)
  - `check_in_mechanism` (yes/no/description)
  - `per‑user_rate_limit` (if discoverable)
  - `notes` (manual curation)
- `HealthCheckResult`:
  - `id`
  - `provider_id`
  - `checked_at`
  - `status` (reachable / error)
  - `supports_v1_models` (yes/no/unknown)
  - `sample_latency_ms` (if measured)
  - `error_summary`

Plan how these entities are stored in PostgreSQL and how migrations will be handled.

---

## Scraper Architecture (/plan → /tdd → /refactor-clean)

Redesign the scraper into clear modules:

1. **DirectoryFetchers**:
   - Small Python modules that know how to fetch and parse each directory (APIIndex, awesome-ai-proxy, GetCheapAI, apisou, apiranking, etc.).
   - Each returns a list of raw provider URLs + metadata.
2. **ProviderNormalizer**:
   - Deduplicates and maps raw URLs into `Provider` + `DomainAlias`.
   - Recognizes obvious mirrors by redirects and identical HTML fingerprints.
3. **MetadataExtractor**:
   - For each provider, fetches the homepage and maybe one or two relevant subpages.
   - Uses simple heuristics (regex, keyword matching) to detect:
     - Whether the site claims to be Chinese.
     - Whether it claims free tiers and what kind.
     - What model names are mentioned.
4. **HealthChecker**:
   - Optional: probes `/v1/models` or an equivalent endpoint with a **no‑auth** request.
   - Records HTTP status and basic latency but does not attempt real inference.
5. **Scheduler**:
   - Runs periodic scraping and health checks (e.g., every 6–24 hours) to keep data fresh.

Use `/refactor-clean` on the existing scraper code to move toward this modular design without breaking current behavior.

Use `/tdd` and `tdd-workflow` to:

- Write tests for each module:
  - Parsing of directory HTML.
  - Provider normalization rules.
  - Simple metadata extraction logic.
- Ensure scrapers handle directory changes gracefully (e.g., failing fast with logs instead of silent breakage).

---

## FastAPI API & UI

Add or refine FastAPI endpoints:

- `GET /providers` — list providers with filters:
  - by `is_chinese_operator`
  - by `model_name` claimed (e.g., filter providers that mention `gpt-5.6-sol` or `deepseek-v4-flash`)
  - by `has_free_tier` (signup/check‑in keywords detected)
- `GET /providers/{id}` — full detail for one provider, including domain aliases, model claims, health check history.
- `GET /models/{model_name}/providers` — list providers that claim to support a given model.

Improve the UI using a simple, clean design (for example, FastAPI + Jinja2 templates + Tailwind CSS):

- A table view of providers with:
  - Name, primary domain, “Chinese?” flag
  - Badges for claimed frontier models (Fable 5, Opus 5, GPT‑5.6 Sol, GPT‑6 Astra, DeepSeek V4 Flash, GLM‑5.3 Flash, GLM‑5.3 Flash, Qwen, etc.)
  - Badges for free tiers (signup credit, daily check‑in).
  - Risk flags (unverified, high risk, unknown operator).
- Detail page with:
  - Raw text of marketing claims (so humans can judge).
  - Link to documents or directory entries used for discovery.
  - Health check results.
- An OmniRoute‑friendly JSON export (e.g., a “Download providers.json” button) with the fields you defined above.

Focus UI on:

- **Search and filters** so you can quickly find candidates for a given model.
- Clear disclaimers that:
  - No model authenticity is guaranteed.
  - “Unlimited free” is often marketing, not verified capacity.

---

## Workflow & Commands

Use this workflow:

1. `/plan` with the architect agent:
   - Analyze the existing Python + FastAPI project.
   - Propose the refactored scraper architecture, data model, and API + UI structure.
2. Use `search-first` skill:
   - Discover and document initial directories (APIIndex, awesome-ai-proxy, GetCheapAI, apisou, apiranking, etc.).
   - Prototype how each will be scraped.
3. `/tdd`:
   - Implement directory fetchers, provider normalizer, metadata extractor, and health checker with tests first.
4. `/refactor-clean`:
   - Integrate new modules into the existing project without breaking behavior.
5. `/code-review`:
   - Have the code-reviewer agent review Python, FastAPI routes, and templates.
6. `/verify`:
   - Run tests, linting, and a dry‑run scrape.
   - Confirm the API and UI behave as expected.

For large changes, split into multiple prompts:

- Prompt 1: `/plan` + data model + architecture.
- Prompt 2: `/tdd` for directory fetchers + normalization.
- Prompt 3: `/tdd` for metadata + health check + DB integration.
- Prompt 4: `/plan` + `/tdd` for FastAPI endpoints + UI.
- Prompt 5: `/code-review` + `/verify`.

---

| Type | Component | Purpose |
|------|-----------|---------|
| Command | `/plan` | High‑level architecture and data model for scraper + FastAPI UI |
| Command | `/tdd` | Build scraper modules and API endpoints with tests first |
| Command | `/refactor-clean` | Redesign existing scraper codebase safely |
| Command | `/code-review` | Review new scraper logic and security implications |
| Command | `/verify` | Run tests, linters, and health checks before “done” |
| Skill | `search-first` | Systematic research across Chinese AI gateway directories  [github](https://github.com/mn-api/awesome-ai-proxy) |
| Skill | `tdd-workflow` | Keep implementation under test and avoid regressions |
| Skill | `verification-loop` | Iterate until scraper outputs meet quality thresholds |
| Skill | `cost-aware-llm-pipeline` | Keep ECC token usage reasonable while iterating |
| Agent | `architect` | Choose architecture: modules, schedulers, database schema |
| Agent | `code-reviewer` | Review Python/FastAPI code and suggest improvements |
| Agent | `security-reviewer` | Flag privacy/security risks in using third‑party gateways |
| Model | `Sonnet 4.6` | Main coding and refactor work for Python/FastAPI |
| Model | `Opus 4.6` | Deeper planning for scraper architecture and heuristics |

---
## Acceptance Criteria

Consider the task “done enough” when:

- The scraper reliably pulls providers from multiple directories and normalizes them into unique Provider records.
- It detects obvious mirrors/alternative domains and groups them correctly.
- It flags providers that *claim* frontier models (Fable 5, Opus 5, GPT‑5.6 Sol, GPT‑6 Astra, DeepSeek V4 Flash, GLM‑5.3 Flash, Qwen) without asserting authenticity.
- The FastAPI UI lets you search, filter, and inspect providers, and export a JSON file to feed into OmniRoute.
- Tests cover scraper modules, normalization logic, and core API endpoints.

Do **not**:

- Attempt to prove model authenticity or real quota (this requires separate manual or automated benchmarking).
- Store or use any real API keys in scraper code.
- Promise legal or security guarantees about any provider.
