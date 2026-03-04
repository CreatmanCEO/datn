# DATN API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Все запросы требуют API-ключ в заголовке:
```
Authorization: Bearer <your-api-key>
```

---

## REST Endpoints

### GET /signals/{symbol}
Получить текущий консенсусный сигнал по инструменту.

**Параметры:**
- `symbol` (path) — торговый инструмент (BTCUSDT, AAPL, SBER)
- `timeframe` (query, optional) — таймфрейм: 1h, 4h, 1d (default: 4h)

**Ответ (200):**
```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-03-02T12:00:00Z",
  "action": "BUY",
  "direction": 0.72,
  "confidence": 0.72,
  "recommendation": {
    "position_size_usd": 500.00,
    "position_pct": 5.0,
    "stop_loss_pct": 3.2,
    "take_profit_pct": 6.8,
    "risk_reward_ratio": 2.13
  },
  "agents": [
    {"agent": "sentiment", "direction": 0.45, "confidence": 0.65, "weight": 0.72, "contribution": 0.18},
    {"agent": "forecast", "direction": 0.80, "confidence": 0.78, "weight": 0.68, "contribution": 0.31},
    {"agent": "anomaly", "direction": 0.0, "confidence": 0.10, "weight": 0.55, "contribution": 0.0},
    {"agent": "technical", "direction": 0.60, "confidence": 0.70, "weight": 0.65, "contribution": 0.23}
  ]
}
```

### GET /signals/{symbol}/history
История сигналов с результатами.

**Параметры:**
- `limit` (query) — количество записей (default: 50, max: 500)
- `from` / `to` (query) — период (ISO 8601)

### GET /agents/status
Статус всех агентов: healthy/unhealthy, historical_accuracy, avg_latency_ms.

### GET /portfolio
Текущее состояние портфеля: позиции, PnL, available funds.

### POST /profile
Обновить профиль риска пользователя: risk_tolerance, max_position_pct, max_drawdown_pct, preferred_symbols.

---

## WebSocket

### /ws/signals
Real-time поток сигналов.
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/signals');
ws.send(JSON.stringify({ "subscribe": ["BTCUSDT", "ETHUSDT"] }));
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

---

## Telegram Bot Commands

| Команда | Описание |
|---------|----------|
| `/signal BTC` | Текущий сигнал по BTC |
| `/portfolio` | Состояние портфеля |
| `/risk` | Текущий профиль риска |
| `/risk moderate` | Изменить профиль |
| `/history BTC 7d` | История сигналов за 7 дней |
| `/agents` | Статус агентов |
| `/subscribe BTC ETH` | Подписаться на уведомления |

### Автоматические уведомления
Бот отправляет push при: сильном сигнале (confidence > threshold), срабатывании stop-loss/take-profit, обнаружении аномалии, изменении статуса агента.
