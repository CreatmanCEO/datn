# DATN Development Roadmap

## Phase 0: Foundation (Weeks 1-2)

**Goal:** Project scaffolding, development environment, CI/CD

- [ ] Project structure with pyproject.toml, pre-commit hooks
- [ ] Docker Compose setup (PostgreSQL, Redis, Kafka, Zookeeper)
- [ ] Database schema and migrations (Alembic)
- [ ] Configuration management (Pydantic Settings)
- [ ] Logging infrastructure (structlog)
- [ ] GitHub Actions CI pipeline (lint, type-check, tests)
- [ ] Base agent abstract class and signal dataclasses

**Deliverable:** Running dev environment with empty agent pipeline

---

## Phase 1: Data Layer (Weeks 3-4)

**Goal:** Reliable market data ingestion and storage

- [ ] CCXT price feed connector (Binance WebSocket)
- [ ] Kafka producer/consumer wrappers
- [ ] TimescaleDB hypertable for OHLCV data
- [ ] News API connector (NewsAPI + Finnhub)
- [ ] Social media connectors (Twitter API v2, Reddit PRAW)
- [ ] Ticker extraction from text (NER or regex-based)
- [ ] Data validation and deduplication
- [ ] Backfill script for historical data

**Deliverable:** Continuous data ingestion with 1-week historical backfill

---

## Phase 2: Agents — MVP (Weeks 5-8)

**Goal:** Three working agents producing standardized signals

### Sentiment Agent (Week 5-6)
- [ ] FinBERT model integration
- [ ] Text preprocessing pipeline
- [ ] Batch inference with sentence-level scoring
- [ ] Source-weighted aggregation
- [ ] Signal generation and Kafka publishing
- [ ] Unit tests with sample articles

### Forecaster Agent (Week 6-7)
- [ ] Chronos-T5 model integration
- [ ] Multi-timeframe data preparation
- [ ] Probabilistic forecast generation (20 samples)
- [ ] Confidence interval calculation
- [ ] Signal generation and Kafka publishing
- [ ] Backtesting framework for forecast accuracy

### Technical Agent (Week 7-8)
- [ ] Core indicators: EMA, RSI, MACD, Bollinger, ATR
- [ ] Volume indicators: OBV, VWAP
- [ ] Support/resistance detection
- [ ] Multi-indicator confluence scoring
- [ ] Signal generation and Kafka publishing
- [ ] Validation against known chart setups

**Deliverable:** Three agents independently producing signals for BTC/USDT

---

## Phase 3: Consensus Engine (Weeks 9-10)

**Goal:** Bayesian aggregation of agent signals

- [ ] Signal collector (subscribes to all agent topics)
- [ ] Initial equal-weight consensus calculation
- [ ] Agreement score computation
- [ ] Risk flag detection (low agreement, conflicting signals)
- [ ] Agent performance tracking table
- [ ] Bayesian weight update after trade resolution
- [ ] Consensus signal publishing to Kafka
- [ ] Dashboard endpoint for agent weights visualization

**Deliverable:** Working consensus engine with self-adjusting weights

---

## Phase 4: Advisor + Interfaces (Weeks 11-13)

**Goal:** User-facing recommendation system

### Digital Advisor (Week 11-12)
- [ ] Risk profile system (conservative/moderate/aggressive)
- [ ] Position sizing with modified Kelly Criterion
- [ ] Portfolio tracking (positions, P&L, exposure)
- [ ] Claude API integration for explanations
- [ ] Trade journal with outcome tracking

### Telegram Bot (Week 12-13)
- [ ] Onboarding flow with risk assessment
- [ ] Signal notification system
- [ ] Portfolio overview command
- [ ] Performance reporting
- [ ] Settings management

### REST API (Week 13)
- [ ] FastAPI endpoints for signals, portfolio, performance
- [ ] JWT authentication
- [ ] WebSocket for real-time signal streaming
- [ ] API documentation (auto-generated OpenAPI)

**Deliverable:** Complete user-facing system with Telegram and API access

---

## Phase 5: Production Hardening (Weeks 14-16)

**Goal:** Stability, monitoring, and performance optimization

- [ ] Prometheus metrics for all components
- [ ] Grafana dashboards (agent performance, system health, P&L)
- [ ] Error handling and graceful degradation
- [ ] Agent health checks and auto-restart
- [ ] Rate limiting for external APIs
- [ ] Backtest mode (replay Kafka topics with historical data)
- [ ] Paper trading mode (simulated execution)
- [ ] Load testing (target: 10 symbols, 3 agents, <5s consensus cycle)
- [ ] Security audit (API keys, auth, input validation)
- [ ] Documentation: deployment guide, API reference

**Deliverable:** Production-ready system running in paper trading mode

---

## Phase 6: Scale & Extend (Post-MVP)

**Goal:** Multi-asset support, new agents, live trading

- [ ] Multi-symbol support (top 20 crypto pairs)
- [ ] New agent: Macro Economic Agent (FRED data, yield curves)
- [ ] New agent: On-chain Analytics Agent (whale tracking, exchange flows)
- [ ] Live trading integration (exchange API order execution)
- [ ] Multi-exchange arbitrage detection
- [ ] Web dashboard (React frontend)
- [ ] Mobile app (React Native)
- [ ] Multi-user system with subscription tiers
- [ ] Agent marketplace (community-contributed agents)

---

## Timeline Summary

| Phase | Duration | Milestone |
|-------|----------|----------|
| 0. Foundation | 2 weeks | Dev environment ready |
| 1. Data Layer | 2 weeks | Data flowing |
| 2. Agents MVP | 4 weeks | Three agents producing signals |
| 3. Consensus | 2 weeks | Bayesian engine working |
| 4. Advisor | 3 weeks | Telegram bot live |
| 5. Production | 3 weeks | Paper trading |
| **Total MVP** | **16 weeks** | **Paper trading with 3 agents** |
| 6. Scale | Ongoing | Live trading, multi-asset |

---

## Technical Debt Rules

1. No feature without tests (minimum 70% coverage)
2. Type hints everywhere (mypy strict mode)
3. Docstrings on all public functions
4. Weekly dependency updates
5. Monthly architecture review
