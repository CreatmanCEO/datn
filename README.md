# DATN — Distributed AI Trading Network

**Multi-agent trading platform with FinBERT sentiment analysis, Chronos-T5 forecasting, Bayesian consensus engine, and adaptive digital advisor.**

---

## Overview

DATN is a distributed system where specialized AI agents collaborate to analyze financial markets, generate trading signals, and provide actionable recommendations through an adaptive advisor interface.

Unlike monolithic trading bots that rely on a single strategy, DATN employs a **multi-agent architecture** where each agent specializes in a specific domain (sentiment, technical analysis, macro signals, time-series forecasting) and contributes to a **Bayesian consensus engine** that weighs and aggregates their outputs.

The result: a system that thinks like a team of analysts, not a single algorithm.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATN PLATFORM                        │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Sentiment   │  │  Forecaster │  │  Technical       │  │
│  │  Agent       │  │  Agent      │  │  Analysis Agent  │  │
│  │  (FinBERT)   │  │ (Chronos-T5)│  │  (Indicators)    │  │
│  └──────┬───────┘  └──────┬──────┘  └───────┬──────────┘  │
│         │                 │                  │             │
│         ▼                 ▼                  ▼             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Bayesian Consensus Engine                 │  │
│  │     (weighted signal aggregation + confidence)      │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            Adaptive Digital Advisor                 │  │
│  │   (risk profiling, position sizing, explanations)   │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│              ┌──────────┴──────────┐                      │
│              ▼                     ▼                      │
│        [REST API]           [Telegram Bot]                │
│                                                           │
└───────────────────────────────────────────────────────────┘

         ┌──────────────────────────────┐
         │        Data Layer            │
         │  Market feeds · News APIs    │
         │  Social sentiment streams    │
         │  PostgreSQL · Redis · Kafka  │
         └──────────────────────────────┘
```

## Core Components

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Sentiment Agent** | FinBERT (ProsusAI/finbert) | Financial news & social media sentiment scoring |
| **Forecaster Agent** | Chronos-T5 (Amazon) | Probabilistic time-series forecasting |
| **Technical Agent** | Custom indicators engine | RSI, MACD, Bollinger, volume analysis, pattern detection |
| **Consensus Engine** | Bayesian inference | Weighted aggregation of agent signals with confidence intervals |
| **Digital Advisor** | LLM-powered (Claude API) | Natural language explanations, risk-adjusted recommendations |
| **Data Pipeline** | Kafka + Redis | Real-time market data ingestion and distribution |
| **Persistence** | PostgreSQL + TimescaleDB | Trade history, agent performance, user portfolios |

## Key Features

- **Multi-agent consensus** — no single point of failure in decision-making; agents vote with confidence weights
- **Explainable signals** — every recommendation comes with reasoning from each agent
- **Adaptive risk profiling** — advisor adjusts position sizing and asset allocation based on user risk tolerance
- **Agent performance tracking** — Bayesian weight updates based on historical accuracy per agent
- **Real-time processing** — Kafka-based event streaming for sub-second signal propagation
- **Extensible agent framework** — plug in new agents without modifying the consensus engine

## Tech Stack

**Backend:** Python 3.11+ · FastAPI · Celery  
**ML/AI:** PyTorch · HuggingFace Transformers · Amazon Chronos  
**Data:** PostgreSQL · TimescaleDB · Redis · Apache Kafka  
**Infrastructure:** Docker · Docker Compose · Nginx  
**Monitoring:** Prometheus · Grafana  
**Interfaces:** REST API · Telegram Bot (aiogram 3.x)  

## Project Structure

```
datn/
├── agents/                  # AI agent implementations
│   ├── base.py             # Abstract agent interface
│   ├── sentiment/          # FinBERT sentiment agent
│   ├── forecaster/         # Chronos-T5 forecasting agent
│   └── technical/          # Technical analysis agent
├── consensus/              # Bayesian consensus engine
│   ├── engine.py           # Core aggregation logic
│   ├── weights.py          # Dynamic weight management
│   └── confidence.py       # Confidence interval calculation
├── advisor/                # Adaptive digital advisor
│   ├── risk_profile.py     # User risk assessment
│   ├── position_sizing.py  # Kelly criterion + risk limits
│   └── explainer.py        # LLM-powered explanations
├── data/                   # Data ingestion & storage
│   ├── feeds/              # Market data connectors
│   ├── news/               # News API integrations
│   └── storage/            # Database models & migrations
├── api/                    # REST API (FastAPI)
├── bot/                    # Telegram bot interface
├── config/                 # Configuration & environment
├── tests/                  # Test suite
├── docs/                   # Documentation
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Quick Start

```bash
# Clone and configure
git clone https://github.com/CreatmanCEO/datn.git
cd datn
cp .env.example .env
# Edit .env with your API keys and database credentials

# Run with Docker
docker-compose up -d

# Or run locally
pip install -e .
python -m datn.main
```

## Documentation

- [Architecture Deep Dive](docs/architecture.md) — detailed system design and data flows
- [Component Specifications](docs/components.md) — technical specs for each module
- [Development Roadmap](docs/roadmap.md) — phased implementation plan
- [Contributing](CONTRIBUTING.md) — how to contribute

## Status

🔬 **In active development** — architecture finalized, core agents in implementation phase.

## Author

**Nik Podolyak** — Python developer & digital architect  
[creatman.site](https://creatman.site) · [GitHub](https://github.com/CreatmanCEO) · [LinkedIn](https://linkedin.com/in/creatman)

## License

MIT License — see [LICENSE](LICENSE) for details.
