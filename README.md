<p align="center">
  <img src="assets/%F0%9F%90%91%20Fleece%20Radar%20%E2%80%94%20%E8%96%85%E7%BE%8A%E6%AF%9B%E9%9B%B7%E8%BE%BE%20landscape%20banner.png" alt="Fleece Radar Banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/your-org/china-ai-provider-finder"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://sqlite.org/"><img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"></a>
  <a href="#-omniroute-integration"><img src="https://img.shields.io/badge/OmniRoute-Compatible-8A2BE2?style=for-the-badge" alt="OmniRoute Compatible"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License"></a>
</p>

<h3 align="center">
  <img src="assets/%F0%9F%90%91%20Fleece%20Radar%20%E2%80%94%20%E8%96%85%E7%BE%8A%E6%AF%9B%E9%9B%B7%E8%BE%BE.png" width="36" height="36" align="center" alt="Logo"> <b>Fleece Radar — 薅羊毛雷达</b>
</h3>

<p align="center">
  <b>Free AI API provider finder & monitor for OmniRoute.</b><br>
  <i>Scans a list of (mostly Chinese) AI relay / reseller sites, checks which ones expose an OpenAI-compatible <code>/v1/models</code> endpoint, what models they list, which ones are <b>free</b>, and optionally fires a 1-token live completion to prove tokens flow. It also discovers new providers from the web.</i>
</p>

---

## 🌟 Why Fleece Radar?

Chinese AI API relay gateways (中转站 / 公益站) pop up, rotate domains, offer promotional credits (注册送/签到), and die weekly. Manually hunting for active endpoints, checking if they support frontier models (**Claude Opus 5, Claude Fable 5, GPT-6 Astra, GPT-5.6 Sol, DeepSeek V4 Flash, GLM-5.3 Flash, Qwen**), and configuring upstreams is tedious and error-prone.

**Fleece Radar** automates this entire lifecycle:
1. **Discovers** gateway endpoints keylessly from search engines, community forums (`linux.do`), GitHub hubs, and directory networks.
2. **Probes** public endpoints (`/v1/models`) passively without requiring credentials or creating accounts.
3. **Separates Fact from Marketing** — measures actual JSON models returned vs. promotional landing-page claims.
4. **Groups Mirrors** — resolves alternative domains pointing to the same backend gateway (e.g. DawCode, SheAPI, HCNSEC/IAMHC).
5. **Exports directly** to **OmniRoute**, `.env` configuration files, CSV datasets, and Markdown research digests.

---

## 🧠 Philosophy & Value Proposition

> **Yes. Fleece Radar is a specialized intelligence pipeline designed to aggregate and verify candidate upstream gateways for OmniRoute. It is not an inferencer, but a passive monitor that builds an evidence-based inventory of relay potential.**

### Value Proposition
Connecting OmniRoute directly to volatile third-party AI gateways requires continuous, empirical market intelligence. Fleece Radar operates upstream of your routing layer: it searches the public web, filters out dead sites, isolates mirrors, and verifies active `/v1/models` catalogs without burning authentication tokens or creating dummy accounts.

### Technical Pipeline
* **Source Discovery (`app/research.py`):** Deep searches across Bing, DuckDuckGo Lite, SearXNG cluster, Mojeek, `linux.do` Discourse feeds, GitHub keyhubs, and 8+ directory aggregators.
* **Data Normalization (`app/core.py`):** Canonicalizes hostnames, strips private/loopback IP ranges, and links alias domains via redirect chains and HTML structure matching.
* **Evidence-Based Scoring:** Balances positive latency/endpoint signals against marketing exaggeration markers to calculate a reliable 0–100 confidence score.
* **Export Logic (`app/cli.py`):** Emits structured OmniRoute JSON configurations, environment variable bundles (`providers.env`), and standard CSV tables.
* **Orchestration (`app/main.py`):** Real-time async FastAPI dashboard backed by a SQLite ledger and background task pool.

### Operational Philosophy

| What the Public Web Claims | What Fleece Radar Listens For | What OmniRoute Receives |
|---|---|---|
| *"Unlimited free pure-blood Claude Opus 5 and GPT-6 Astra, 100% stable!"* | *Passive HTTP check: HTTP 200, `/v1/models` live with 42 models, marketing flag detected.* | *A sanitized, score-weighted upstream candidate ready for selective 1-token validation.* |

---

## 📡 Live Provider Radar (206 Tracked Gateways)

Below is a live-tracked inventory of **206 Chinese AI API gateways and community relays** monitored by Fleece Radar:

| Provider Gateway | Provider Gateway | Provider Gateway |
|---|---|---|
| <img src="https://www.google.com/s2/favicons?domain=0168.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [0168.cn](https://0168.cn/) | <img src="https://www.google.com/s2/favicons?domain=100t.xiaomimimo.com&sz=32" width="16" height="16" alt="" valign="middle" /> [100t.xiaomimimo.com](https://100t.xiaomimimo.com/) | <img src="https://www.google.com/s2/favicons?domain=52mx.net&sz=32" width="16" height="16" alt="" valign="middle" /> [52mx.net](https://52mx.net/) |
| <img src="https://www.google.com/s2/favicons?domain=52mxw.com&sz=32" width="16" height="16" alt="" valign="middle" /> [52mxw.com](https://52mxw.com/) | <img src="https://www.google.com/s2/favicons?domain=688.qzz.io&sz=32" width="16" height="16" alt="" valign="middle" /> [688.qzz.io](https://688.qzz.io/) | <img src="https://www.google.com/s2/favicons?domain=756777.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [756777.xyz](https://756777.xyz/) |
| <img src="https://www.google.com/s2/favicons?domain=8s.hk&sz=32" width="16" height="16" alt="" valign="middle" /> [8s.hk](https://8s.hk/) | <img src="https://www.google.com/s2/favicons?domain=aerolink.lat&sz=32" width="16" height="16" alt="" valign="middle" /> [aerolink.lat](https://aerolink.lat/register?ref=7KR4BGK) | <img src="https://www.google.com/s2/favicons?domain=agentrouter.org&sz=32" width="16" height="16" alt="" valign="middle" /> [agentrouter.org](https://agentrouter.org/register?aff=O5p1) |
| <img src="https://www.google.com/s2/favicons?domain=ai-pixel.online&sz=32" width="16" height="16" alt="" valign="middle" /> [ai-pixel.online](https://ai-pixel.online/) | <img src="https://www.google.com/s2/favicons?domain=ai-router.dev&sz=32" width="16" height="16" alt="" valign="middle" /> [ai-router.dev](https://ai-router.dev/) | <img src="https://www.google.com/s2/favicons?domain=ai.121628.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.121628.xyz](https://ai.121628.xyz/) |
| <img src="https://www.google.com/s2/favicons?domain=ai.962831.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.962831.xyz](https://ai.962831.xyz/) | <img src="https://www.google.com/s2/favicons?domain=ai.baicloud.org&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.baicloud.org](https://ai.baicloud.org/) | <img src="https://www.google.com/s2/favicons?domain=ai.furry.vg&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.furry.vg](https://ai.furry.vg/) |
| <img src="https://www.google.com/s2/favicons?domain=ai.godsun.pro&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.godsun.pro](https://ai.godsun.pro/) | <img src="https://www.google.com/s2/favicons?domain=ai.kscsnkli.site&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.kscsnkli.site](https://ai.kscsnkli.site/) | <img src="https://www.google.com/s2/favicons?domain=ai.soulecho.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.soulecho.cc](https://ai.soulecho.cc/) |
| <img src="https://www.google.com/s2/favicons?domain=ai.t1qq.com&sz=32" width="16" height="16" alt="" valign="middle" /> [ai.t1qq.com](https://ai.t1qq.com/) | <img src="https://www.google.com/s2/favicons?domain=aiapi1.cc.cd&sz=32" width="16" height="16" alt="" valign="middle" /> [aiapi1.cc.cd](https://aiapi1.cc.cd/) | <img src="https://www.google.com/s2/favicons?domain=aihubmix.com&sz=32" width="16" height="16" alt="" valign="middle" /> [aihubmix.com](https://aihubmix.com/model/coding-glm-5.3-flash-free) |
| <img src="https://www.google.com/s2/favicons?domain=aimeot.com&sz=32" width="16" height="16" alt="" valign="middle" /> [aimeot.com](https://aimeot.com/) | <img src="https://www.google.com/s2/favicons?domain=aiwahaha.lol&sz=32" width="16" height="16" alt="" valign="middle" /> [aiwahaha.lol](https://aiwahaha.lol/) | <img src="https://www.google.com/s2/favicons?domain=anymodel.org&sz=32" width="16" height="16" alt="" valign="middle" /> [anymodel.org](https://anymodel.org/) |
| <img src="https://www.google.com/s2/favicons?domain=anyrouter.top&sz=32" width="16" height="16" alt="" valign="middle" /> [anyrouter.top](https://anyrouter.top/) | <img src="https://www.google.com/s2/favicons?domain=api.aisz.mom&sz=32" width="16" height="16" alt="" valign="middle" /> [api.aisz.mom](https://api.aisz.mom/) | <img src="https://www.google.com/s2/favicons?domain=api.aiwanai.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [api.aiwanai.cc](https://api.aiwanai.cc/) |
| <img src="https://www.google.com/s2/favicons?domain=api.astrdark.cyou&sz=32" width="16" height="16" alt="" valign="middle" /> [api.astrdark.cyou](https://api.astrdark.cyou/) | <img src="https://www.google.com/s2/favicons?domain=api.azx.us&sz=32" width="16" height="16" alt="" valign="middle" /> [api.azx.us](https://api.azx.us/) | <img src="https://www.google.com/s2/favicons?domain=api.badtheorylabs.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.badtheorylabs.com](https://api.badtheorylabs.com/) |
| <img src="https://www.google.com/s2/favicons?domain=api.bluesminds.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.bluesminds.com](https://api.bluesminds.com/register?aff=lBwr) | <img src="https://www.google.com/s2/favicons?domain=api.bybing.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [api.bybing.cc](https://api.bybing.cc/) | <img src="https://www.google.com/s2/favicons?domain=api.camel-hub.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.camel-hub.com](https://api.camel-hub.com/) |
| <img src="https://www.google.com/s2/favicons?domain=api.cheapcodex.online&sz=32" width="16" height="16" alt="" valign="middle" /> [api.cheapcodex.online](https://api.cheapcodex.online/) | <img src="https://www.google.com/s2/favicons?domain=api.denxio.top&sz=32" width="16" height="16" alt="" valign="middle" /> [api.denxio.top](https://api.denxio.top/) | <img src="https://www.google.com/s2/favicons?domain=api.fri5.top&sz=32" width="16" height="16" alt="" valign="middle" /> [api.fri5.top](https://api.fri5.top/) |
| <img src="https://www.google.com/s2/favicons?domain=api.futureppo.top&sz=32" width="16" height="16" alt="" valign="middle" /> [api.futureppo.top](https://api.futureppo.top/) | <img src="https://www.google.com/s2/favicons?domain=api.gemai.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [api.gemai.cc](https://api.gemai.cc/) | <img src="https://www.google.com/s2/favicons?domain=api.gmi-serving.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.gmi-serving.com](https://api.gmi-serving.com/) |
| <img src="https://www.google.com/s2/favicons?domain=api.h5sky.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [api.h5sky.cn](https://api.h5sky.cn/) | <img src="https://www.google.com/s2/favicons?domain=api.hcnsec.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [api.hcnsec.cn](https://api.hcnsec.cn/) | <img src="https://www.google.com/s2/favicons?domain=api.iamhc.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [api.iamhc.cn](https://api.iamhc.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=api.jeniya.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [api.jeniya.cn](https://api.jeniya.cn/) | <img src="https://www.google.com/s2/favicons?domain=api.jinkundong.store&sz=32" width="16" height="16" alt="" valign="middle" /> [api.jinkundong.store](https://api.jinkundong.store/) | <img src="https://www.google.com/s2/favicons?domain=api.justworker.icu&sz=32" width="16" height="16" alt="" valign="middle" /> [api.justworker.icu](https://api.justworker.icu) |
| <img src="https://www.google.com/s2/favicons?domain=api.lingxiaihub.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.lingxiaihub.com](https://api.lingxiaihub.com/) | <img src="https://www.google.com/s2/favicons?domain=api.muzeai.top&sz=32" width="16" height="16" alt="" valign="middle" /> [api.muzeai.top](https://api.muzeai.top/) | <img src="https://www.google.com/s2/favicons?domain=api.rua.chat&sz=32" width="16" height="16" alt="" valign="middle" /> [api.rua.chat](https://api.rua.chat/) |
| <img src="https://www.google.com/s2/favicons?domain=api.siliconflow.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [api.siliconflow.cn](https://api.siliconflow.cn/) | <img src="https://www.google.com/s2/favicons?domain=api.usora.net&sz=32" width="16" height="16" alt="" valign="middle" /> [api.usora.net](https://api.usora.net/) | <img src="https://www.google.com/s2/favicons?domain=api.wanapis.com&sz=32" width="16" height="16" alt="" valign="middle" /> [api.wanapis.com](https://api.wanapis.com/) |
| <img src="https://www.google.com/s2/favicons?domain=api.yufish.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [api.yufish.cc](https://api.yufish.cc/) | <img src="https://www.google.com/s2/favicons?domain=api.zeekai.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [api.zeekai.cc](https://api.zeekai.cc/) | <img src="https://www.google.com/s2/favicons?domain=apiindex.me&sz=32" width="16" height="16" alt="" valign="middle" /> [apiindex.me](https://apiindex.me/) |
| <img src="https://www.google.com/s2/favicons?domain=apipaths.com&sz=32" width="16" height="16" alt="" valign="middle" /> [apipaths.com](https://apipaths.com/) | <img src="https://www.google.com/s2/favicons?domain=apiranking.com&sz=32" width="16" height="16" alt="" valign="middle" /> [apiranking.com](https://apiranking.com/) | <img src="https://www.google.com/s2/favicons?domain=apisou.com&sz=32" width="16" height="16" alt="" valign="middle" /> [apisou.com](https://apisou.com/) |
| <img src="https://www.google.com/s2/favicons?domain=apizh.net&sz=32" width="16" height="16" alt="" valign="middle" /> [apizh.net](https://apizh.net/) | <img src="https://www.google.com/s2/favicons?domain=baipiao.org&sz=32" width="16" height="16" alt="" valign="middle" /> [baipiao.org](https://baipiao.org/) | <img src="https://www.google.com/s2/favicons?domain=beizhi.sylu.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [beizhi.sylu.cc](https://beizhi.sylu.cc/) |
| <img src="https://www.google.com/s2/favicons?domain=build.nvidia.com&sz=32" width="16" height="16" alt="" valign="middle" /> [build.nvidia.com](https://build.nvidia.com/deepseek-ai/deepseek-v4-flash) | <img src="https://www.google.com/s2/favicons?domain=cavoti.com&sz=32" width="16" height="16" alt="" valign="middle" /> [cavoti.com](https://cavoti.com/) | <img src="https://www.google.com/s2/favicons?domain=ccswitch.io&sz=32" width="16" height="16" alt="" valign="middle" /> [ccswitch.io](https://ccswitch.io/) |
| <img src="https://www.google.com/s2/favicons?domain=chain888.vip&sz=32" width="16" height="16" alt="" valign="middle" /> [chain888.vip](https://chain888.vip/) | <img src="https://www.google.com/s2/favicons?domain=chat-api4-3.087654.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [chat-api4-3.087654.xyz](https://chat-api4-3.087654.xyz/) | <img src="https://www.google.com/s2/favicons?domain=chat.b.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [chat.b.ai](https://chat.b.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=chat.z.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [chat.z.ai](https://chat.z.ai/) | <img src="https://www.google.com/s2/favicons?domain=chat01.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [chat01.ai](https://chat01.ai/) | <img src="https://www.google.com/s2/favicons?domain=chuan.sylu.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [chuan.sylu.cc](https://chuan.sylu.cc/) |
| <img src="https://www.google.com/s2/favicons?domain=claudefa.st&sz=32" width="16" height="16" alt="" valign="middle" /> [claudefa.st](https://claudefa.st/) | <img src="https://www.google.com/s2/favicons?domain=cli.999554.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [cli.999554.xyz](https://cli.999554.xyz/) | <img src="https://www.google.com/s2/favicons?domain=code.phanthy.com&sz=32" width="16" height="16" alt="" valign="middle" /> [code.phanthy.com](https://code.phanthy.com/) |
| <img src="https://www.google.com/s2/favicons?domain=console.flatkey.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [console.flatkey.ai](https://console.flatkey.ai/) | <img src="https://www.google.com/s2/favicons?domain=cow.g201.com&sz=32" width="16" height="16" alt="" valign="middle" /> [cow.g201.com](https://cow.g201.com/) | <img src="https://www.google.com/s2/favicons?domain=dawclaudecode.com&sz=32" width="16" height="16" alt="" valign="middle" /> [dawclaudecode.com](https://dawclaudecode.com/) |
| <img src="https://www.google.com/s2/favicons?domain=dawcode.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [dawcode.ai](https://dawcode.ai/) | <img src="https://www.google.com/s2/favicons?domain=dawcode.com&sz=32" width="16" height="16" alt="" valign="middle" /> [dawcode.com](https://dawcode.com/) | <img src="https://www.google.com/s2/favicons?domain=deeprouter.top&sz=32" width="16" height="16" alt="" valign="middle" /> [deeprouter.top](https://deeprouter.top/) |
| <img src="https://www.google.com/s2/favicons?domain=developer.puter.com&sz=32" width="16" height="16" alt="" valign="middle" /> [developer.puter.com](https://developer.puter.com/ai/) | <img src="https://www.google.com/s2/favicons?domain=docode.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [docode.cc](https://docode.cc/) | <img src="https://www.google.com/s2/favicons?domain=docs.apiyi.com&sz=32" width="16" height="16" alt="" valign="middle" /> [docs.apiyi.com](https://docs.apiyi.com/) |
| <img src="https://www.google.com/s2/favicons?domain=eggstriker.com&sz=32" width="16" height="16" alt="" valign="middle" /> [eggstriker.com](https://eggstriker.com/) | <img src="https://www.google.com/s2/favicons?domain=emtf.aipm9527.online&sz=32" width="16" height="16" alt="" valign="middle" /> [emtf.aipm9527.online](https://emtf.aipm9527.online/) | <img src="https://www.google.com/s2/favicons?domain=en.jiekou.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [en.jiekou.ai](https://en.jiekou.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=ergouzi.life&sz=32" width="16" height="16" alt="" valign="middle" /> [ergouzi.life](https://ergouzi.life/) | <img src="https://www.google.com/s2/favicons?domain=factory.pub&sz=32" width="16" height="16" alt="" valign="middle" /> [factory.pub](https://factory.pub/) | <img src="https://www.google.com/s2/favicons?domain=fapi.leileihog.top&sz=32" width="16" height="16" alt="" valign="middle" /> [fapi.leileihog.top](https://fapi.leileihog.top/) |
| <img src="https://www.google.com/s2/favicons?domain=fast.qianxing.pro&sz=32" width="16" height="16" alt="" valign="middle" /> [fast.qianxing.pro](https://fast.qianxing.pro/) | <img src="https://www.google.com/s2/favicons?domain=forge-gateway-api.fly.dev&sz=32" width="16" height="16" alt="" valign="middle" /> [forge-gateway-api.fly.dev](https://forge-gateway-api.fly.dev/) | <img src="https://www.google.com/s2/favicons?domain=free.empero.org&sz=32" width="16" height="16" alt="" valign="middle" /> [free.empero.org](https://free.empero.org/) |
| <img src="https://www.google.com/s2/favicons?domain=free.supxh.xin&sz=32" width="16" height="16" alt="" valign="middle" /> [free.supxh.xin](https://free.supxh.xin/) | <img src="https://www.google.com/s2/favicons?domain=freeaiapi.org&sz=32" width="16" height="16" alt="" valign="middle" /> [freeaiapi.org](https://freeaiapi.org/) | <img src="https://www.google.com/s2/favicons?domain=freeapi.dgbmc.top&sz=32" width="16" height="16" alt="" valign="middle" /> [freeapi.dgbmc.top](https://freeapi.dgbmc.top/) |
| <img src="https://www.google.com/s2/favicons?domain=freeapi.ybapi.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [freeapi.ybapi.xyz](https://freeapi.ybapi.xyz/) | <img src="https://www.google.com/s2/favicons?domain=freellm.net&sz=32" width="16" height="16" alt="" valign="middle" /> [freellm.net](https://freellm.net/) | <img src="https://www.google.com/s2/favicons?domain=freellmapihub.com&sz=32" width="16" height="16" alt="" valign="middle" /> [freellmapihub.com](https://freellmapihub.com/) |
| <img src="https://www.google.com/s2/favicons?domain=freemodel.dev&sz=32" width="16" height="16" alt="" valign="middle" /> [freemodel.dev](https://freemodel.dev/) | <img src="https://www.google.com/s2/favicons?domain=freetokenfaucet.com&sz=32" width="16" height="16" alt="" valign="middle" /> [freetokenfaucet.com](https://freetokenfaucet.com/) | <img src="https://www.google.com/s2/favicons?domain=gemai.huchan.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [gemai.huchan.cn](https://gemai.huchan.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=gorouter.app&sz=32" width="16" height="16" alt="" valign="middle" /> [gorouter.app](https://gorouter.app/) | <img src="https://www.google.com/s2/favicons?domain=guxiaomo.site&sz=32" width="16" height="16" alt="" valign="middle" /> [guxiaomo.site](https://guxiaomo.site/) | <img src="https://www.google.com/s2/favicons?domain=hcnote.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [hcnote.cn](https://hcnote.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=helpcoder.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [helpcoder.cc](https://helpcoder.cc/) | <img src="https://www.google.com/s2/favicons?domain=htai91.com&sz=32" width="16" height="16" alt="" valign="middle" /> [htai91.com](https://htai91.com/) | <img src="https://www.google.com/s2/favicons?domain=jianzhile.vip&sz=32" width="16" height="16" alt="" valign="middle" /> [jianzhile.vip](https://jianzhile.vip/) |
| <img src="https://www.google.com/s2/favicons?domain=jucodex.com&sz=32" width="16" height="16" alt="" valign="middle" /> [jucodex.com](https://jucodex.com/) | <img src="https://www.google.com/s2/favicons?domain=kapibala.asia&sz=32" width="16" height="16" alt="" valign="middle" /> [kapibala.asia](https://kapibala.asia/) | <img src="https://www.google.com/s2/favicons?domain=kelen.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [kelen.cc](https://kelen.cc/) |
| <img src="https://www.google.com/s2/favicons?domain=kiraai.vn&sz=32" width="16" height="16" alt="" valign="middle" /> [kiraai.vn](https://kiraai.vn/) | <img src="https://www.google.com/s2/favicons?domain=kktoken.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [kktoken.cc](https://kktoken.cc/sign-in) | <img src="https://www.google.com/s2/favicons?domain=lastapi.cccyc.com.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [lastapi.cccyc.com.cn](https://lastapi.cccyc.com.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=llm24.net&sz=32" width="16" height="16" alt="" valign="middle" /> [llm24.net](https://llm24.net/) | <img src="https://www.google.com/s2/favicons?domain=llmbase.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [llmbase.ai](https://llmbase.ai/) | <img src="https://www.google.com/s2/favicons?domain=lmspeed.net&sz=32" width="16" height="16" alt="" valign="middle" /> [lmspeed.net](https://lmspeed.net/) |
| <img src="https://www.google.com/s2/favicons?domain=loveapi.top&sz=32" width="16" height="16" alt="" valign="middle" /> [loveapi.top](https://loveapi.top/) | <img src="https://www.google.com/s2/favicons?domain=lzhiyu.ccwu.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [lzhiyu.ccwu.cc](https://lzhiyu.ccwu.cc/) | <img src="https://www.google.com/s2/favicons?domain=mad.myddns.me&sz=32" width="16" height="16" alt="" valign="middle" /> [mad.myddns.me](https://mad.myddns.me/) |
| <img src="https://www.google.com/s2/favicons?domain=modeloc.com&sz=32" width="16" height="16" alt="" valign="middle" /> [modeloc.com](https://modeloc.com/) | <img src="https://www.google.com/s2/favicons?domain=models.dev&sz=32" width="16" height="16" alt="" valign="middle" /> [models.dev](https://models.dev/) | <img src="https://www.google.com/s2/favicons?domain=modelscope.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [modelscope.ai](https://modelscope.ai/models?filter=inference_type&page=1&tabKey=task) |
| <img src="https://www.google.com/s2/favicons?domain=modelverify.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [modelverify.ai](https://modelverify.ai/) | <img src="https://www.google.com/s2/favicons?domain=monkeycode-ai.com&sz=32" width="16" height="16" alt="" valign="middle" /> [monkeycode-ai.com](https://monkeycode-ai.com/) | <img src="https://www.google.com/s2/favicons?domain=motomoto.lol&sz=32" width="16" height="16" alt="" valign="middle" /> [motomoto.lol](https://motomoto.lol/) |
| <img src="https://www.google.com/s2/favicons?domain=moyuu.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [moyuu.cc](https://moyuu.cc/) | <img src="https://www.google.com/s2/favicons?domain=muyuan.do&sz=32" width="16" height="16" alt="" valign="middle" /> [muyuan.do](https://muyuan.do/) | <img src="https://www.google.com/s2/favicons?domain=myclaw.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [myclaw.ai](https://myclaw.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=nailao.biz&sz=32" width="16" height="16" alt="" valign="middle" /> [nailao.biz](https://nailao.biz/) | <img src="https://www.google.com/s2/favicons?domain=napi.kid1412.qzz.io&sz=32" width="16" height="16" alt="" valign="middle" /> [napi.kid1412.qzz.io](https://napi.kid1412.qzz.io/) | <img src="https://www.google.com/s2/favicons?domain=new.jinshi.xin&sz=32" width="16" height="16" alt="" valign="middle" /> [new.jinshi.xin](https://new.jinshi.xin/) |
| <img src="https://www.google.com/s2/favicons?domain=new.xinjianya.top&sz=32" width="16" height="16" alt="" valign="middle" /> [new.xinjianya.top](https://new.xinjianya.top/) | <img src="https://www.google.com/s2/favicons?domain=newapi.nki.pw&sz=32" width="16" height="16" alt="" valign="middle" /> [newapi.nki.pw](https://newapi.nki.pw/) | <img src="https://www.google.com/s2/favicons?domain=nikoapi.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [nikoapi.xyz](https://nikoapi.xyz/) |
| <img src="https://www.google.com/s2/favicons?domain=nofx.one&sz=32" width="16" height="16" alt="" valign="middle" /> [nofx.one](https://nofx.one/) | <img src="https://www.google.com/s2/favicons?domain=nova.vcrauo.com&sz=32" width="16" height="16" alt="" valign="middle" /> [nova.vcrauo.com](https://nova.vcrauo.com/) | <img src="https://www.google.com/s2/favicons?domain=oai2api.com&sz=32" width="16" height="16" alt="" valign="middle" /> [oai2api.com](https://oai2api.com/) |
| <img src="https://www.google.com/s2/favicons?domain=obvps.com&sz=32" width="16" height="16" alt="" valign="middle" /> [obvps.com](https://obvps.com/) | <img src="https://www.google.com/s2/favicons?domain=ofox.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [ofox.ai](https://ofox.ai/) | <img src="https://www.google.com/s2/favicons?domain=once.novai.su&sz=32" width="16" height="16" alt="" valign="middle" /> [once.novai.su](https://once.novai.su/) |
| <img src="https://www.google.com/s2/favicons?domain=open.bigmodel.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [open.bigmodel.cn](https://open.bigmodel.cn/) | <img src="https://www.google.com/s2/favicons?domain=open.selart.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [open.selart.cc](https://open.selart.cc/) | <img src="https://www.google.com/s2/favicons?domain=opencode.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [opencode.ai](https://opencode.ai/zen/) |
| <img src="https://www.google.com/s2/favicons?domain=openrouter.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [openrouter.ai](https://openrouter.ai/models?fmt=cards&max_price=0) | <img src="https://www.google.com/s2/favicons?domain=orevx.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [orevx.ai](https://orevx.ai/) | <img src="https://www.google.com/s2/favicons?domain=ourchat.shop&sz=32" width="16" height="16" alt="" valign="middle" /> [ourchat.shop](https://ourchat.shop/) |
| <img src="https://www.google.com/s2/favicons?domain=pai.zaiduyu.top&sz=32" width="16" height="16" alt="" valign="middle" /> [pai.zaiduyu.top](https://pai.zaiduyu.top/) | <img src="https://www.google.com/s2/favicons?domain=platform.ai.hixinghai.top&sz=32" width="16" height="16" alt="" valign="middle" /> [platform.ai.hixinghai.top](https://platform.ai.hixinghai.top/) | <img src="https://www.google.com/s2/favicons?domain=platform.moonshot.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [platform.moonshot.cn](https://platform.moonshot.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=pro.agentrouter.org&sz=32" width="16" height="16" alt="" valign="middle" /> [pro.agentrouter.org](https://pro.agentrouter.org/) | <img src="https://www.google.com/s2/favicons?domain=ps.air-outer.com&sz=32" width="16" height="16" alt="" valign="middle" /> [ps.air-outer.com](https://ps.air-outer.com/) | <img src="https://www.google.com/s2/favicons?domain=qwen.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [qwen.ai](https://qwen.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=remail.aishop6.com&sz=32" width="16" height="16" alt="" valign="middle" /> [remail.aishop6.com](https://remail.aishop6.com/) | <img src="https://www.google.com/s2/favicons?domain=rntm.sh&sz=32" width="16" height="16" alt="" valign="middle" /> [rntm.sh](https://rntm.sh/) | <img src="https://www.google.com/s2/favicons?domain=router.bynara.id&sz=32" width="16" height="16" alt="" valign="middle" /> [router.bynara.id](https://router.bynara.id/) |
| <img src="https://www.google.com/s2/favicons?domain=runtime.badtheorylabs.com&sz=32" width="16" height="16" alt="" valign="middle" /> [runtime.badtheorylabs.com](https://runtime.badtheorylabs.com/) | <img src="https://www.google.com/s2/favicons?domain=runtimewire.com&sz=32" width="16" height="16" alt="" valign="middle" /> [runtimewire.com](https://runtimewire.com/) | <img src="https://www.google.com/s2/favicons?domain=savriko.com&sz=32" width="16" height="16" alt="" valign="middle" /> [savriko.com](https://savriko.com/) |
| <img src="https://www.google.com/s2/favicons?domain=seekai.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [seekai.cc](https://seekai.cc/register?aff=O5p1) | <img src="https://www.google.com/s2/favicons?domain=shenwenai.com&sz=32" width="16" height="16" alt="" valign="middle" /> [shenwenai.com](https://shenwenai.com/) | <img src="https://www.google.com/s2/favicons?domain=shep-api.com&sz=32" width="16" height="16" alt="" valign="middle" /> [shep-api.com](https://shep-api.com/) |
| <img src="https://www.google.com/s2/favicons?domain=starkrelay.bond&sz=32" width="16" height="16" alt="" valign="middle" /> [starkrelay.bond](https://starkrelay.bond/) | <img src="https://www.google.com/s2/favicons?domain=straitapi.com&sz=32" width="16" height="16" alt="" valign="middle" /> [straitapi.com](https://straitapi.com/) | <img src="https://www.google.com/s2/favicons?domain=sub.vcnovb.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [sub.vcnovb.cn](https://sub.vcnovb.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=superapi.buzz&sz=32" width="16" height="16" alt="" valign="middle" /> [superapi.buzz](https://superapi.buzz/) | <img src="https://www.google.com/s2/favicons?domain=synterolink.com&sz=32" width="16" height="16" alt="" valign="middle" /> [synterolink.com](https://synterolink.com/) | <img src="https://www.google.com/s2/favicons?domain=tabitoken.com&sz=32" width="16" height="16" alt="" valign="middle" /> [tabitoken.com](https://tabitoken.com/) |
| <img src="https://www.google.com/s2/favicons?domain=teamorouter.com&sz=32" width="16" height="16" alt="" valign="middle" /> [teamorouter.com](https://teamorouter.com/) | <img src="https://www.google.com/s2/favicons?domain=token-plan-cn.xiaomimimo.com&sz=32" width="16" height="16" alt="" valign="middle" /> [token-plan-cn.xiaomimimo.com](https://token-plan-cn.xiaomimimo.com/) | <img src="https://www.google.com/s2/favicons?domain=tokenbom.com&sz=32" width="16" height="16" alt="" valign="middle" /> [tokenbom.com](https://tokenbom.com/) |
| <img src="https://www.google.com/s2/favicons?domain=tokenrhythm.studio&sz=32" width="16" height="16" alt="" valign="middle" /> [tokenrhythm.studio](https://tokenrhythm.studio/) | <img src="https://www.google.com/s2/favicons?domain=true-sota.com&sz=32" width="16" height="16" alt="" valign="middle" /> [true-sota.com](https://true-sota.com/home) | <img src="https://www.google.com/s2/favicons?domain=us-3.nianhuaapi.com&sz=32" width="16" height="16" alt="" valign="middle" /> [us-3.nianhuaapi.com](https://us-3.nianhuaapi.com/) |
| <img src="https://www.google.com/s2/favicons?domain=user.zmodel.top&sz=32" width="16" height="16" alt="" valign="middle" /> [user.zmodel.top](https://user.zmodel.top/) | <img src="https://www.google.com/s2/favicons?domain=v4flash.com&sz=32" width="16" height="16" alt="" valign="middle" /> [v4flash.com](https://v4flash.com/) | <img src="https://www.google.com/s2/favicons?domain=vibex.iflow.cn&sz=32" width="16" height="16" alt="" valign="middle" /> [vibex.iflow.cn](https://vibex.iflow.cn/) |
| <img src="https://www.google.com/s2/favicons?domain=vip.j3gb.com&sz=32" width="16" height="16" alt="" valign="middle" /> [vip.j3gb.com](https://vip.j3gb.com/) | <img src="https://www.google.com/s2/favicons?domain=vsllm.com&sz=32" width="16" height="16" alt="" valign="middle" /> [vsllm.com](https://vsllm.com/) | <img src="https://www.google.com/s2/favicons?domain=vyceai.com&sz=32" width="16" height="16" alt="" valign="middle" /> [vyceai.com](https://vyceai.com/) |
| <img src="https://www.google.com/s2/favicons?domain=wudaolu.com&sz=32" width="16" height="16" alt="" valign="middle" /> [wudaolu.com](https://wudaolu.com/) | <img src="https://www.google.com/s2/favicons?domain=www.80aj.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.80aj.com](https://www.80aj.com/) | <img src="https://www.google.com/s2/favicons?domain=www.aaaapi.fun&sz=32" width="16" height="16" alt="" valign="middle" /> [www.aaaapi.fun](https://www.aaaapi.fun/) |
| <img src="https://www.google.com/s2/favicons?domain=www.arityflow.top&sz=32" width="16" height="16" alt="" valign="middle" /> [www.arityflow.top](https://www.arityflow.top/) | <img src="https://www.google.com/s2/favicons?domain=www.baaaai.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.baaaai.com](https://www.baaaai.com/) | <img src="https://www.google.com/s2/favicons?domain=www.bigmodel.ltd&sz=32" width="16" height="16" alt="" valign="middle" /> [www.bigmodel.ltd](https://www.bigmodel.ltd/) |
| <img src="https://www.google.com/s2/favicons?domain=www.cun.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.cun.ai](https://www.cun.ai/) | <img src="https://www.google.com/s2/favicons?domain=www.forge-ai.space&sz=32" width="16" height="16" alt="" valign="middle" /> [www.forge-ai.space](https://www.forge-ai.space/) | <img src="https://www.google.com/s2/favicons?domain=www.getcheapai.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.getcheapai.com](https://www.getcheapai.com/) |
| <img src="https://www.google.com/s2/favicons?domain=www.getunikey.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.getunikey.ai](https://www.getunikey.ai/) | <img src="https://www.google.com/s2/favicons?domain=www.hiapi.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.hiapi.ai](https://www.hiapi.ai/) | <img src="https://www.google.com/s2/favicons?domain=www.hvoy.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.hvoy.ai](https://www.hvoy.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=www.kskys.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.kskys.com](https://www.kskys.com/) | <img src="https://www.google.com/s2/favicons?domain=www.kuraa.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [www.kuraa.cc](https://www.kuraa.cc/) | <img src="https://www.google.com/s2/favicons?domain=www.mcgrox.top&sz=32" width="16" height="16" alt="" valign="middle" /> [www.mcgrox.top](https://www.mcgrox.top/) |
| <img src="https://www.google.com/s2/favicons?domain=www.nexusvai.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [www.nexusvai.xyz](https://www.nexusvai.xyz/chat/api/) | <img src="https://www.google.com/s2/favicons?domain=www.orcarouter.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.orcarouter.ai](https://www.orcarouter.ai/) | <img src="https://www.google.com/s2/favicons?domain=www.orcarouter.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.orcarouter.ai](https://www.orcarouter.ai/models/deepseek/deepseek-v4-flash-free) |
| <img src="https://www.google.com/s2/favicons?domain=www.routescope.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.routescope.ai](https://www.routescope.ai/) | <img src="https://www.google.com/s2/favicons?domain=www.sheapi.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [www.sheapi.cc](https://www.sheapi.cc/) | <img src="https://www.google.com/s2/favicons?domain=www.sheapi.top&sz=32" width="16" height="16" alt="" valign="middle" /> [www.sheapi.top](https://www.sheapi.top/) |
| <img src="https://www.google.com/s2/favicons?domain=www.univibe.cc&sz=32" width="16" height="16" alt="" valign="middle" /> [www.univibe.cc](https://www.univibe.cc/) | <img src="https://www.google.com/s2/favicons?domain=www.uselunora.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.uselunora.com](https://www.uselunora.com/) | <img src="https://www.google.com/s2/favicons?domain=www.whatstoken.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [www.whatstoken.ai](https://www.whatstoken.ai/) |
| <img src="https://www.google.com/s2/favicons?domain=www.wyy22.com&sz=32" width="16" height="16" alt="" valign="middle" /> [www.wyy22.com](https://www.wyy22.com/) | <img src="https://www.google.com/s2/favicons?domain=xingya.site&sz=32" width="16" height="16" alt="" valign="middle" /> [xingya.site](https://xingya.site/) | <img src="https://www.google.com/s2/favicons?domain=xxs.l.cd&sz=32" width="16" height="16" alt="" valign="middle" /> [xxs.l.cd](https://xxs.l.cd/) |
| <img src="https://www.google.com/s2/favicons?domain=yaoheqi.xyz&sz=32" width="16" height="16" alt="" valign="middle" /> [yaoheqi.xyz](https://yaoheqi.xyz/) | <img src="https://www.google.com/s2/favicons?domain=zenmux.ai&sz=32" width="16" height="16" alt="" valign="middle" /> [zenmux.ai](https://zenmux.ai/) |  |

---

<p align="center">
  <img src="assets/%F0%9F%90%91%20Fleece%20Radar%20%E2%80%94%20%E8%96%85%E7%BE%8A%E6%AF%9B%E9%9B%B7%E8%BE%BE%20banner%201.png" width="500" alt="Fleece Radar Capabilities & Model Coverage">
</p>

## ⚡ Core Features

### 1. 🌐 Keyless Multi-Source Deep Research
* **5 Search Engines:** Bing HTML, DuckDuckGo Lite, 8-instance SearXNG failover cluster, Mojeek, and optional Brave Search API.
* **Community Feeds:** Instant parsing of `linux.do` Discourse forum JSON (where freebie relay deals get posted daily) and GitHub keyhubs (`awesome-ai-proxy`, `FreeLLM-API-KeyHub`, `FreeToken`).
* **Directory Crawlers:** Automated scrapers for `apiindex.me`, `apisou.com`, `baipiao.org`, `getcheapai.com`, `freellm.net`, `freeaiapi.org`, `kelen.cc`, and `apiranking.com`.
* **One-Hop Expansion:** Fetches linked blog posts, gists, and discussion threads to uncover hidden relay links.

### 2. 🔍 Real Data vs. Marketing Copy
Relays often claim support for non-existent or expensive models. Fleece Radar checks both:
* **Marketing Claims:** Regex detection on homepages for `Claude Fable 5`, `Claude Opus 5`, `GPT-6 Astra`, `GPT-5.6 Sol`, `DeepSeek V4`, `GLM-5.3 Flash`, `Qwen`, `Kimi`, `MiniMax`, `Gemini`, `Grok`.
* **Verified Models:** Queries unauthenticated `/v1/models` JSON responses to extract real, active model IDs.

### 3. 🔗 Mirror & Alias Resolution
Identifies redirect chains and matching HTML fingerprints to group mirror domains into unified provider profiles (e.g. `api.iamhc.cn` → `api.hcnsec.cn`, DawCode mirrors, SheAPI, Runtime).

### 4. 📊 Evidence-Based Scoring System (0–100)
* **+ Points:** HTTP 200 response, low latency, verified `/v1/models` endpoint, free-tier evidence keywords (`免费`, `公益`, `白嫖`, `注册送`, `签到`, `0倍率`), valid registration URL.
* **- Points:** Exaggerated marketing flags (`无限`, `满血`, `破解`, `unlimited`, `永久不限量`), offline status.

---

## 🛡️ Safety & Ethics Boundary

This project is strictly **passive and defensive**:
* **No Account Creation:** Does **not** register accounts, generate referral links, farm tokens, or solve CAPTCHAs.
* **No Credential Access:** Does **not** harvest or store user API keys.
* **No Authenticated Probing:** Probes unauthenticated endpoints (`/v1/models`, `/api/status`) exclusively.
* **Privacy Warning:** Never send sensitive, private, or confidential data through third-party relays.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/your-org/china-ai-provider-finder.git
cd china-ai-provider-finder

# Create & activate virtual environment
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Launch the Web Dashboard

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **`http://127.0.0.1:8000`** in your browser.

---

## 🖥️ Dashboard Controls

| Action Button | Function |
|---|---|
| **Scan URLs** | Parses and scans raw text or URL lists pasted into the console. |
| **Scan seeds** | Probes all seed targets in `data/seeds.txt` (~200+ gateways). |
| **Discover directories** | Crawls 8+ curated directory hubs for newly posted relay links. |
| **🔬 Deep research** | Runs the full multi-phase search + feed + directory + link expansion pipeline (1–3 mins). |
| **OmniRoute JSON ⬇** | Downloads `omniroute-providers.json` formatted directly for OmniRoute upstreams. |
| **Report MD ⬇** | Downloads an aggregated Markdown intelligence digest summarizing model coverage. |

---

## 🛠️ CLI Guide

Run headless scanning and export pipelines directly via `python -m app.cli`:

```bash
# 1. Scan seeds or custom files
python -m app.cli scan data/seeds.txt
python -m app.cli scan https://example.com https://another.example

# 2. Crawl a specific directory URL or run search discovery
python -m app.cli discover https://apiindex.me/zh/self-publish
python -m app.cli discover --query '免费 大模型 API 公益站'

# 3. Export provider datasets
python -m app.cli export export/omniroute.json --format omniroute --alive
python -m app.cli export export/providers.csv --format csv
python -m app.cli export export/providers.txt --format txt --alive

# 4. Build complete export package (omniroute.json + providers.env + providers.csv)
python -m app.cli export-build

# 5. Deduplicate and append new URLs into data/seeds.txt
python -m app.cli merge-seeds new_candidates.txt
```

---

## 📦 OmniRoute Integration

Fleece Radar formats alive, OpenAI-compatible upstreams directly into OmniRoute-compatible schema:

```json
[
  {
    "name": "example-relay.ai",
    "base_url": "https://example-relay.ai/v1/",
    "platform": "New API",
    "api_compatible": true,
    "score": 85,
    "models": ["gpt-4o", "claude-3-5-sonnet-20241022", "deepseek-chat"],
    "target_models": ["Claude Opus 5"],
    "free_evidence": ["注册送", "公益"],
    "registration_url": "https://example-relay.ai/register",
    "risk_flags": []
  }
]
```

Build all export formats in one command: `python -m app.cli export-build`.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web dashboard single-page interface. |
| `GET` | `/api/providers` | Query findings with filters (`?q=`, `?model=`, `?alive=true`, `?limit=500`). |
| `POST` | `/api/scan` | Trigger async background scan of a URL list. |
| `POST` | `/api/scan-text` | Multipart form text scan (automatically extracts URLs). |
| `POST` | `/api/scan-seeds` | Trigger async background scan of `data/seeds.txt`. |
| `POST` | `/api/discover` | Crawl directory URLs or search queries for candidate gateways. |
| `POST` | `/api/deep-research` | Execute full multi-backend deep research pass. |
| `GET` | `/api/aliases` | Fetch detected mirror and alias domain groups. |
| `GET` | `/api/jobs/{id}` | Poll background job progress and completion status. |
| `GET` | `/api/export.omniroute`| Export JSON formatted for OmniRoute upstreams. |
| `GET` | `/api/export.csv` | Download full provider dataset as CSV. |
| `GET` | `/api/export.txt` | Download alive provider URLs as plain text. |
| `GET` | `/api/research.md` | Download detailed Markdown intelligence report. |

---

## ⚙️ Configuration & Environment

Environment settings can be placed in `.env`:

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_PATH` | `data/providers.db` | Path to SQLite database file |
| `SCAN_CONCURRENCY` | `12` | Maximum parallel HTTP probes |
| `REQUEST_TIMEOUT` | `12` | Per-request timeout in seconds |
| `REFRESH_HOURS` | `0` | Automated background re-scan interval (hours; `0` = off) |
| `BRAVE_SEARCH_API_KEY` | *(None)* | Optional Brave Search API key (free 2k req/mo) |
| `USER_AGENT` | `FleeceRadar/1.0...` | Custom HTTP User-Agent header |

---

## ⏰ Cron & Automated Background Monitoring

Relay nodes come and go constantly. Set up automatic daily refreshes:

```bash
# Trigger seed rescan daily at 09:00 UTC
0 9 * * * curl -s -X POST http://127.0.0.1:8000/api/scan-seeds > /dev/null
```

Or set `REFRESH_HOURS=6` in `.env` to enable continuous in-process re-checks.

---

## 🧪 Test Suite

Run unit and integration tests with pytest:

```bash
pytest tests/ -v
```

---

## 🧩 Extend It

- **Directory Adapters:** Add source-specific directory adapters in `discover_directory()` inside `app/core.py`.
- **Model Patterns:** Add more frontier model regexes to `MODEL_PATTERNS` in `app/core.py`.
- **Search Backends:** Drop additional search providers into `app/research.py`.
- **Authenticated Verification:** Perform 1-token test completions using **your own manually supplied provider keys** in a separate secrets store. Do not automate account creation or promotional-credit farming.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

