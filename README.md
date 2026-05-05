# DATN — Distributed AI Trading Network

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/CreatmanCEO/datn?style=social)](https://github.com/CreatmanCEO/datn/stargazers)
[![Validate](https://github.com/CreatmanCEO/datn/actions/workflows/validate.yml/badge.svg)](https://github.com/CreatmanCEO/datn/actions/workflows/validate.yml)
[![Status: Early Dev](https://img.shields.io/badge/status-early%20development-orange)](#status)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Docker Compose](https://img.shields.io/badge/docker-compose-2496ED?logo=docker&logoColor=white)](docker-compose.yml)

Multi-agent trading platform: FinBERT sentiment, Chronos-T5 forecasting, Bayesian consensus, and an adaptive advisor that explains every recommendation in natural language.

## Why this exists

Most retail trading bots run a single strategy and break the moment market regime shifts. DATN takes the opposite bet: several specialized agents (sentiment, forecasting, technical) vote on every signal, a Bayesian consensus engine weights them by historical accuracy, and an LLM-backed advisor turns the result into a recommendation a human can audit.

The goal is not "beat the market." The goal is a transparent, modular research stack where you can swap an agent, watch its weight evolve, and see why a position was suggested.

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                    DATN PLATFORM                        │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Sentiment   │  │  Forecaster │  │  Technical       │  │
│  │  Agent       │  │  Agent      │  │  Analysis Agent  │  │
│  │  (FinBERT)   │  │ (Chronos-T5)│  │  (Indicators)    │  │
│  └──────┬───────┘  └──────┬──────┘  └───────┬──────────┘  │
│         ▼                 ▼                  ▼             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Bayesian Consensus Engine                 │  │
│  │     (weighted signal aggregation + confidence)      │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            Adaptive Digital Advisor                 │  │
│  │   (risk profiling, position sizing, explanations)   │  │
│  └──────────────────────┬──────────────────────────────┘  │
│              ┌──────────┴──────────┐                      │
│              ▼                     ▼                      │
│        [REST API]           [Telegram Bot]                │
└───────────────────────────────────────────────────────────┘
```

1. **Agents** produce independent signals with confidence scores
2. **Consensus engine** combines them via Bayesian weighting (weights update from historical accuracy)
3. **Advisor** layer applies user risk profile, sizes positions, and asks Claude to explain the call
4. **Interfaces** — REST API and Telegram bot consume the advisor output

See [docs/architecture.md](docs/architecture.md) for full data flows and [docs/AGENTS.md](docs/AGENTS.md) for agent specs.

## Tech stack

| Layer | Tool |
|-------|------|
| Backend | Python 3.11+, FastAPI, Celery |
| ML | PyTorch, HuggingFace Transformers, Chronos-T5 (Amazon), FinBERT (ProsusAI) |
| Market data | ccxt, ta-lib, pandas, numpy |
| LLM advisor | Anthropic Claude API |
| Data plane | PostgreSQL + TimescaleDB, Redis, Apache Kafka (aiokafka) |
| Bot | aiogram 3.x |
| Config | pydantic-settings, structlog |
| Infra | Docker + docker-compose |
| Tests | pytest |

## Quick start

```bash
git clone https://github.com/CreatmanCEO/datn.git
cd datn
cp .env.example .env        # set API keys and DB credentials
docker-compose up -d

# Or local install
pip install -e .
python -m datn.main
```

## Project layout

```
datn/
├── agents/      # base.py + sentiment / forecaster / technical
├── consensus/   # Bayesian aggregation, weights, confidence
├── advisor/     # risk profile, position sizing, LLM explainer
├── data/        # market feeds, news, storage
├── api/         # FastAPI REST surface
├── bot/         # aiogram Telegram interface
├── config/      # env + settings
├── tests/       # pytest suite (consensus covered today)
├── docs/        # architecture, components, agents, API, roadmap
└── docker-compose.yml
```

## Status

Early development. Architecture is finalized; agent implementations are partial. Test coverage is currently focused on the consensus engine.

| Component | State |
|-----------|-------|
| Architecture & docs | Complete |
| Consensus engine | Implemented + tested |
| Sentiment agent (FinBERT) | Skeleton |
| Forecaster (Chronos-T5) | Skeleton |
| Technical agent | Skeleton |
| Advisor / risk profile | Skeleton |
| API | Skeleton |
| Telegram bot | Skeleton |

## Documentation

- [docs/architecture.md](docs/architecture.md) — system design, data flows
- [docs/components.md](docs/components.md) — per-module specs
- [docs/AGENTS.md](docs/AGENTS.md) — AI agent specifications
- [docs/API.md](docs/API.md) — REST API reference
- [docs/roadmap.md](docs/roadmap.md) — phased implementation plan
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute

## Limitations

- **Not financial advice.** This is a research and engineering project. Outputs are signals, not recommendations to trade.
- Most agents are skeletons today; do not expect production-quality signals
- Backtesting harness is not yet wired into the consensus engine
- LLM explanations require a paid Anthropic API key
- TimescaleDB and Kafka raise operational complexity; small deployments may want to swap for plain Postgres + Redis pub/sub
- No paper-trading bridge yet; broker integration is on the roadmap

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the priority list and PR checklist.

## Related — Claude Code ecosystem by the same author

- [claude-code-antiregression-setup](https://github.com/CreatmanCEO/claude-code-antiregression-setup) — guard rails against regressions in Claude Code sessions
- [ai-context-hierarchy](https://github.com/CreatmanCEO/ai-context-hierarchy) — Level 0/1/2 context layout for Claude projects
- [claude-statusline](https://github.com/CreatmanCEO/claude-statusline) — status bar for Claude Code
- [notebooklm-claude-workflows](https://github.com/CreatmanCEO/notebooklm-claude-workflows) — NotebookLM + Claude research loops
- [webtest-orch](https://github.com/CreatmanCEO/webtest-orch) — universal e2e test orchestrator
- [hydrowatch](https://github.com/CreatmanCEO/hydrowatch) — water/utility monitoring tooling
- [lingua-companion](https://github.com/CreatmanCEO/lingua-companion) — voice-first English learning
- [security-scanner](https://github.com/CreatmanCEO/security-scanner) — Telegram security scanning bot
- [diabot](https://github.com/CreatmanCEO/diabot) — KBJU-by-photo bot for type 1 diabetes
- [ghost-showcase](https://github.com/CreatmanCEO/ghost-showcase) — GHOST AI desktop overlay (paused)
- [cc-janitor](https://github.com/CreatmanCEO/cc-janitor) — Claude Code workspace janitor (in active development)

## Author

**Nick Podolyak**
- GitHub: [@CreatmanCEO](https://github.com/CreatmanCEO)
- Habr: [creatman](https://habr.com/ru/users/creatman/)
- dev.to: [@creatman](https://dev.to/creatman)
- Telegram: [@Creatman_it](https://t.me/Creatman_it)
- Site: [creatman.site](https://creatman.site)

## License

MIT — see [LICENSE](LICENSE).
