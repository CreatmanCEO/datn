# DATN Component Specifications

## 1. Sentiment Agent (FinBERT)

### Purpose
Analyzes financial news articles and social media posts to extract market sentiment for specific assets.

### Technology
- **Model:** ProsusAI/finbert (BERT fine-tuned on financial text)
- **Runtime:** PyTorch with HuggingFace Transformers
- **GPU:** Optional (CPU inference ~200ms/article, GPU ~30ms/article)

### Input
- News articles from Kafka topic `news.articles.*`
- Social media posts from `sentiment.social.*`
- Each message contains: `text`, `source`, `timestamp`, `symbols` (detected tickers)

### Processing Pipeline
```
Raw text
  → Preprocessing (clean HTML, normalize tickers, split sentences)
  → FinBERT inference (per-sentence sentiment: positive/negative/neutral + score)
  → Aggregation (weighted average by recency and source reliability)
  → Signal generation (direction + confidence for each symbol)
```

### Output Signal
```python
{
    "agent_id": "sentiment_finbert_v1",
    "symbol": "BTC/USDT",
    "direction": 0.72,        # bullish
    "confidence": 0.85,
    "horizon": "4h",
    "metadata": {
        "articles_analyzed": 47,
        "positive_ratio": 0.68,
        "negative_ratio": 0.15,
        "neutral_ratio": 0.17,
        "dominant_topics": ["ETF approval", "institutional buying"],
        "source_breakdown": {
            "news": {"count": 12, "avg_sentiment": 0.65},
            "twitter": {"count": 28, "avg_sentiment": 0.78},
            "reddit": {"count": 7, "avg_sentiment": 0.54}
        }
    },
    "reasoning": "Strong bullish sentiment across 47 sources. News coverage focused on ETF approval prospects (12 articles, avg sentiment 0.65). Social media sentiment notably higher (0.78) driven by institutional buying narratives."
}
```

### Configuration
```yaml
sentiment_agent:
  model: ProsusAI/finbert
  batch_size: 32
  max_sequence_length: 512
  min_articles_for_signal: 5
  recency_decay_hours: 24
  source_weights:
    news: 1.0
    twitter: 0.6
    reddit: 0.4
    stocktwits: 0.5
  update_interval_seconds: 300
```

---

## 2. Forecaster Agent (Chronos-T5)

### Purpose
Generates probabilistic time-series forecasts for asset prices using Amazon's Chronos-T5 foundation model.

### Technology
- **Model:** Amazon Chronos-T5 (T5 architecture adapted for time-series)
- **Runtime:** PyTorch
- **Approach:** Zero-shot forecasting — no fine-tuning needed per asset

### Input
- OHLCV price data from Kafka topic `market.prices.*`
- Supports multiple timeframes: 1m, 5m, 15m, 1h, 4h, 1d

### Processing Pipeline
```
Historical OHLCV (context window: 512 data points)
  → Feature engineering (returns, log prices, volatility)
  → Chronos-T5 inference (generates 20 sample trajectories)
  → Statistical analysis (median forecast, confidence intervals)
  → Trend detection (direction, magnitude, uncertainty)
  → Signal generation
```

### Output Signal
```python
{
    "agent_id": "forecaster_chronos_v1",
    "symbol": "BTC/USDT",
    "direction": 0.45,         # moderately bullish
    "confidence": 0.62,
    "horizon": "24h",
    "metadata": {
        "current_price": 67450.0,
        "forecast_median": 68200.0,
        "forecast_p10": 66100.0,   # 10th percentile
        "forecast_p90": 69800.0,   # 90th percentile
        "expected_return": 0.011,   # +1.1%
        "volatility_forecast": 0.032,
        "timeframe_used": "1h",
        "context_length": 512
    },
    "reasoning": "Chronos-T5 forecasts +1.1% move over 24h (median: $68,200). Wide confidence interval ($66,100-$69,800) indicates elevated uncertainty. Moderate bullish bias with high volatility expected."
}
```

### Configuration
```yaml
forecaster_agent:
  model: amazon/chronos-t5-large
  context_length: 512
  prediction_horizon: 24   # data points ahead
  num_samples: 20          # trajectory samples for confidence
  timeframes:
    - "1h"                 # primary
    - "4h"                 # confirmation
  update_interval_seconds: 3600
  min_data_points: 100
```

---

## 3. Technical Analysis Agent

### Purpose
Computes classical and modern technical indicators, detects chart patterns, and generates trading signals based on multi-indicator confluence.

### Technology
- **Libraries:** TA-Lib, pandas-ta, custom implementations
- **Runtime:** Pure Python/NumPy (no GPU needed)

### Indicators Computed

**Trend:**
- EMA (9, 21, 50, 200)
- MACD (12, 26, 9)
- ADX (14)
- Ichimoku Cloud

**Momentum:**
- RSI (14)
- Stochastic RSI
- Williams %R
- CCI (20)

**Volatility:**
- Bollinger Bands (20, 2)
- ATR (14)
- Keltner Channels

**Volume:**
- OBV (On-Balance Volume)
- VWAP
- Volume Profile
- CMF (Chaikin Money Flow)

**Patterns:**
- Support/Resistance levels (fractal-based)
- Double top/bottom
- Head & shoulders
- Divergences (RSI, MACD vs price)

### Signal Logic
```
For each indicator category:
  → Compute indicator value
  → Classify as bullish/neutral/bearish
  → Assign weight based on timeframe relevance

Confluence score = weighted sum of all indicator signals
Direction = normalized confluence score [-1, +1]
Confidence = agreement ratio among indicators
```

### Output Signal
```python
{
    "agent_id": "technical_indicators_v1",
    "symbol": "BTC/USDT",
    "direction": 0.35,
    "confidence": 0.71,
    "horizon": "4h",
    "metadata": {
        "trend": {"bias": "bullish", "strength": 0.6, "ema_alignment": "bullish"},
        "momentum": {"rsi": 58.3, "bias": "neutral", "divergence": null},
        "volatility": {"atr_pct": 2.1, "bb_position": 0.62, "squeeze": false},
        "volume": {"obv_trend": "rising", "vwap_position": "above"},
        "patterns": ["higher_low", "ema_golden_cross_pending"],
        "support": 65800.0,
        "resistance": 69200.0
    },
    "reasoning": "Moderate bullish setup: price above VWAP with rising OBV confirms buying pressure. RSI neutral at 58 with room to run. EMA 9/21 golden cross forming. Key resistance at $69,200. Support at $65,800."
}
```

---

## 4. Bayesian Consensus Engine

### Purpose
Aggregates signals from all agents into a single consensus recommendation using Bayesian inference for dynamic weight allocation.

### Algorithm

**Step 1: Signal Collection**
```python
signals = [
    sentiment_agent.latest_signal(symbol),
    forecaster_agent.latest_signal(symbol),
    technical_agent.latest_signal(symbol),
]
```

**Step 2: Weight Calculation**

Each agent has a prior weight based on historical performance:
```python
# Bayesian update after each resolved trade
def update_weight(agent, trade_outcome):
    likelihood = agent.accuracy_on(trade_outcome.conditions)
    agent.weight *= likelihood
    normalize_weights(all_agents)
```

**Step 3: Consensus Calculation**
```python
consensus_direction = sum(s.direction * s.confidence * w[s.agent_id] 
                          for s in signals) / total_weight

agreement = 1.0 - std([s.direction for s in signals])

consensus_confidence = mean([s.confidence for s in signals]) * agreement
```

**Step 4: Risk Flag Detection**
```python
risk_flags = []
if agreement < 0.4:
    risk_flags.append("LOW_AGREEMENT")
if any(s.confidence < 0.3 for s in signals):
    risk_flags.append("LOW_CONFIDENCE_AGENT")
if abs(consensus_direction) < 0.1:
    risk_flags.append("INDECISIVE")
```

### Performance Tracking

The engine maintains a rolling performance log per agent:
```sql
CREATE TABLE agent_performance (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64),
    symbol VARCHAR(20),
    signal_direction FLOAT,
    signal_confidence FLOAT,
    actual_outcome FLOAT,
    was_correct BOOLEAN,
    profit_loss FLOAT,
    timestamp TIMESTAMPTZ,
    market_conditions JSONB  -- volatility regime, trend state
);
```

---

## 5. Adaptive Digital Advisor

### Purpose
Translates consensus signals into personalized, risk-adjusted recommendations with natural language explanations.

### Risk Profiles

| Profile | Max Position Size | Max Portfolio Risk | Stop Loss | Leverage |
|---------|------------------|--------------------|-----------|----------|
| Conservative | 5% per trade | 10% drawdown | Tight (1.5% ATR) | None |
| Moderate | 10% per trade | 20% drawdown | Standard (2.5% ATR) | Up to 2x |
| Aggressive | 20% per trade | 35% drawdown | Wide (4% ATR) | Up to 5x |

### Position Sizing (Modified Kelly Criterion)
```python
def calculate_position_size(signal, user_profile, portfolio):
    # Kelly fraction
    win_rate = consensus_engine.historical_accuracy(signal.symbol)
    avg_win = consensus_engine.avg_win_size(signal.symbol)
    avg_loss = consensus_engine.avg_loss_size(signal.symbol)
    
    kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
    
    # Apply safety: use half-Kelly
    safe_fraction = kelly_fraction * 0.5
    
    # Apply risk profile limits
    max_size = user_profile.max_position_pct * portfolio.total_value
    
    # Check portfolio exposure
    current_exposure = portfolio.total_exposure()
    available = user_profile.max_risk - current_exposure
    
    return min(safe_fraction * portfolio.total_value, max_size, available)
```

### Explanation Generation

Uses Claude API to generate natural language explanations:
```python
prompt = f"""
You are a trading advisor. Explain this recommendation concisely.

Consensus: {signal.direction} ({signal.confidence} confidence)
Agent breakdown:
- Sentiment: {sentiment_signal.summary}
- Forecast: {forecast_signal.summary}
- Technical: {technical_signal.summary}

User risk profile: {user.risk_profile}
Recommended action: {action}
Position size: {size}

Explain in 2-3 sentences why this trade makes sense and what the risks are.
"""
```

### Telegram Bot Interface

Built with aiogram 3.x:
```
/start        — onboarding and risk profile setup
/portfolio    — current positions and P&L
/signals      — latest consensus signals
/subscribe    — auto-notifications for new signals
/performance  — agent accuracy and portfolio metrics
/settings     — risk profile, notification preferences
```

---

## 6. Data Pipeline

### Market Data Connectors

Using CCXT unified interface:
```python
async def price_feed(exchange: str, symbols: list[str]):
    client = ccxt_async.binance()  # or bybit, etc.
    while True:
        for symbol in symbols:
            ohlcv = await client.fetch_ohlcv(symbol, '1m', limit=1)
            await kafka_producer.send(
                f'market.prices.{exchange}.{symbol}',
                value=ohlcv
            )
        await asyncio.sleep(60)
```

### News Aggregation
```python
news_sources = [
    NewsAPIConnector(api_key=NEWS_API_KEY),
    FinnhubNewsConnector(api_key=FINNHUB_KEY),
    AlphaVantageNewsConnector(api_key=AV_KEY),
]

async def news_feed():
    for source in news_sources:
        articles = await source.fetch_latest()
        for article in articles:
            symbols = extract_tickers(article.text)
            await kafka_producer.send(
                f'news.articles.{source.name}',
                value={**article.dict(), 'symbols': symbols}
            )
```
