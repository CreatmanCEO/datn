# DATN Architecture

## System Design Philosophy

DATN is built on three principles:

1. **Specialization over generalization** — each agent does one thing well
2. **Consensus over authority** — no single agent makes the final call
3. **Transparency over black-box** — every decision is explainable

The system is designed as a distributed pipeline where independent agents analyze market data from their unique perspective, then a Bayesian consensus engine synthesizes their outputs into actionable signals.

---

## Data Flow

### 1. Ingestion Layer

Market data enters the system through multiple connectors:

- **Price feeds** — WebSocket connections to exchanges (Binance, Bybit) via CCXT
- **News feeds** — Financial news APIs (NewsAPI, Finnhub, Alpha Vantage news)
- **Social sentiment** — Twitter/X API, Reddit API (r/wallstreetbets, r/stocks), StockTwits
- **Macro data** — FRED API for economic indicators, Treasury yields, CPI

All incoming data is published to **Apache Kafka** topics, providing:
- Decoupled producers and consumers
- Message replay for backtesting
- Horizontal scaling of data processing

**Kafka Topic Structure:**
```
market.prices.{exchange}.{symbol}    # Real-time OHLCV
market.orderbook.{exchange}.{symbol} # Order book snapshots
news.articles.{source}               # News articles
sentiment.social.{platform}          # Social media posts
macro.indicators.{series}            # Economic indicators
```

### 2. Agent Processing Layer

Each agent subscribes to relevant Kafka topics and produces signals:

```
                    Kafka Topics
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │Sentiment │  │Forecaster│  │Technical │
   │  Agent   │  │  Agent   │  │  Agent   │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │              │              │
        ▼              ▼              ▼
   signals.sentiment  signals.forecast  signals.technical
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              Consensus Engine
                       │
                       ▼
              signals.consensus
                       │
                       ▼
              Adaptive Advisor
```

**Signal Format (standardized across all agents):**
```python
@dataclass
class AgentSignal:
    agent_id: str           # e.g. "sentiment_finbert_v1"
    symbol: str             # e.g. "BTC/USDT"
    timestamp: datetime
    direction: float        # -1.0 (strong sell) to +1.0 (strong buy)
    confidence: float       # 0.0 to 1.0
    horizon: timedelta      # signal validity window
    metadata: dict          # agent-specific details
    reasoning: str          # human-readable explanation
```

### 3. Consensus Layer

The Bayesian Consensus Engine receives signals from all agents and produces a unified recommendation:

**Weight Update Formula:**
```
w_i(t+1) = w_i(t) * P(correct | agent_i) / P(correct)
```

Where:
- `w_i(t)` — current weight for agent i
- `P(correct | agent_i)` — historical accuracy of agent i
- `P(correct)` — base rate of correct predictions

Weights are updated after each trade outcome is known, creating a self-improving system where more accurate agents gain more influence over time.

**Consensus Output:**
```python
@dataclass
class ConsensusSignal:
    symbol: str
    timestamp: datetime
    direction: float           # weighted average direction
    confidence: float          # combined confidence
    agreement_score: float     # how much agents agree (0-1)
    agent_contributions: dict  # per-agent signal breakdown
    risk_flags: list[str]      # conflicting signals, low confidence, etc.
```

### 4. Advisor Layer

The Adaptive Digital Advisor translates consensus signals into user-specific recommendations:

- Applies user's **risk profile** (conservative / moderate / aggressive)
- Calculates **position size** using modified Kelly Criterion with risk limits
- Generates **natural language explanations** via Claude API
- Tracks portfolio exposure and enforces diversification rules

---

## Agent Communication Protocol

Agents communicate exclusively through Kafka topics — no direct agent-to-agent calls. This ensures:

- Agents can be deployed, scaled, and updated independently
- New agents can be added without modifying existing ones
- Agent failures don't cascade
- All communications are logged and replayable

**Agent Lifecycle:**
```
1. REGISTER   → Agent announces capabilities to registry
2. SUBSCRIBE  → Agent subscribes to relevant data topics
3. PROCESS    → Agent analyzes incoming data
4. PUBLISH    → Agent publishes signals to its output topic
5. HEARTBEAT  → Agent sends periodic health checks
6. FEEDBACK   → Agent receives outcome data for self-evaluation
```

---

## State Management

| Store | Purpose | Technology |
|-------|---------|------------|
| Hot state | Current prices, active signals, session data | Redis |
| Warm state | Recent trades, agent metrics, user portfolios | PostgreSQL |
| Time-series | Historical prices, signal history | TimescaleDB (PostgreSQL extension) |
| Event log | All agent communications, audit trail | Kafka (persistent topics) |
| Model artifacts | Trained model weights, configs | Local filesystem + S3 |

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│              Docker Compose              │
│                                          │
│  ┌────────┐ ┌────────┐ ┌─────────────┐  │
│  │ Kafka  │ │ Redis  │ │ PostgreSQL  │  │
│  │ + Zoo  │ │        │ │ +TimescaleDB│  │
│  └────────┘ └────────┘ └─────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │         Agent Workers (Celery)     │  │
│  │  sentiment · forecaster · technical│  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │  Consensus   │  │    Advisor      │  │
│  │  Engine      │  │    Service      │  │
│  └──────────────┘  └─────────────────┘  │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │  FastAPI     │  │  Telegram Bot   │  │
│  │  (REST API)  │  │  (aiogram 3.x)  │  │
│  └──────────────┘  └─────────────────┘  │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │ Prometheus   │  │    Grafana      │  │
│  └──────────────┘  └─────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │           Nginx (reverse proxy)    │  │
│  └────────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

Minimum requirements: 4 CPU cores, 16 GB RAM, 100 GB SSD  
Recommended for production: 8 CPU cores, 32 GB RAM, 500 GB NVMe

---

## Security Considerations

- API keys stored in environment variables, never in code
- All external API calls through rate-limited proxy
- Database connections via connection pooling (asyncpg)
- Telegram bot webhook with IP whitelist
- JWT authentication for REST API
- Agent-to-Kafka communication over TLS in production
