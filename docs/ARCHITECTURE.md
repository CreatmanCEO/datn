# Архитектура DATN

## Обзор

DATN построена по принципу **мультиагентной системы** (MAS), где каждый агент — независимый модуль со своей специализацией. Агенты не знают друг о друге и не зависят друг от друга. Их сигналы объединяются в **Consensus Engine** — центральном компоненте, который принимает финальное решение.

Такая архитектура даёт три ключевых преимущества:
1. **Отказоустойчивость** — если один агент упал или даёт мусор, остальные компенсируют
2. **Масштабируемость** — новый агент добавляется без переписывания системы
3. **Прозрачность** — видно, какой агент повлиял на решение и насколько

---

## 1. Data Layer (Слой данных)

### Источники данных

**Market Data:**
- Биржевые API (Binance, Bybit, MOEX) через WebSocket для real-time данных
- REST API для исторических данных (свечи, стакан, сделки)
- Интервалы: 1m, 5m, 15m, 1h, 4h, 1d

**News Feed:**
- RSS-агрегация финансовых новостей (Reuters, Bloomberg, RBC, Interfax)
- Telegram-каналы через Telethon (парсинг публичных каналов)
- Twitter/X API для отслеживания ключевых аккаунтов

**Social Signals:**
- Reddit API (r/wallstreetbets, r/cryptocurrency)
- Fear and Greed Index
- Google Trends для ключевых активов

### Хранение

**TimescaleDB** для временных рядов:
- Hypertables с автоматическим партиционированием по времени
- Retention policy: raw данные — 90 дней, агрегированные — без ограничений
- Continuous aggregates для быстрых запросов по интервалам

**Redis** для оперативных данных:
- Текущие позиции агентов
- Кэш последних сигналов
- Rate limiting для API
- Pub/Sub для real-time уведомлений

```sql
CREATE TABLE market_data (
    time        TIMESTAMPTZ NOT NULL,
    symbol      TEXT NOT NULL,
    open        DOUBLE PRECISION,
    high        DOUBLE PRECISION,
    low         DOUBLE PRECISION,
    close       DOUBLE PRECISION,
    volume      DOUBLE PRECISION,
    source      TEXT
);
SELECT create_hypertable('market_data', 'time');
```

---

## 2. Agent Layer (Слой агентов)

Каждый агент реализует интерфейс `BaseAgent`:

```python
class AgentSignal(BaseModel):
    agent_id: str              # Уникальный ID агента
    timestamp: datetime        # Время генерации сигнала
    symbol: str                # Торговый инструмент
    direction: float           # от -1.0 (продажа) до +1.0 (покупка)
    confidence: float          # от 0.0 до 1.0
    reasoning: str             # Человекочитаемое обоснование
    metadata: dict             # Дополнительные данные агента

class BaseAgent(ABC):
    @abstractmethod
    async def analyze(self, symbol: str, data: dict) -> AgentSignal: ...
    
    @abstractmethod
    async def health_check(self) -> bool: ...
    
    def update_accuracy(self, was_correct: bool):
        alpha = 0.1
        self.historical_accuracy = (
            alpha * (1.0 if was_correct else 0.0) 
            + (1 - alpha) * self.historical_accuracy
        )
```

### Агенты

| Агент | Модель | Вход | Выход | Latency |
|-------|--------|------|-------|---------|
| SentimentAgent | FinBERT | Новости, твиты, посты | direction + confidence | ~200ms |
| ForecastAgent | Chronos-T5 | OHLCV таймсерии | direction + confidence + price target | ~500ms |
| AnomalyAgent | IsoForest + Z-score | Volume, spread, order flow | anomaly flag + confidence | ~50ms |
| TechnicalAgent | TA-Lib | OHLCV | direction + confidence + levels | ~30ms |

---

## 3. Bayesian Consensus Engine

Сердце системы. Принимает сигналы от всех агентов и формирует единое решение.

### Принцип работы

1. **Сбор сигналов** — ждём ответа от всех агентов (timeout 5 сек)
2. **Взвешивание** — каждый сигнал умножается на вес агента (основан на исторической точности)
3. **Агрегация** — байесовское обновление prior → posterior
4. **Confidence filtering** — отбрасываем решения с confidence < threshold
5. **Output** — финальный сигнал с объяснением вклада каждого агента

### Адаптивные веса

Веса агентов обновляются после каждого торгового решения:
- Если агент был прав → вес растёт (EMA с alpha=0.1)
- Если ошибся → вес падает
- Минимальный вес: 0.1 (агент никогда полностью не исключается)
- Максимальный вес: 0.95

Это означает, что система **самообучается** — со временем точные агенты получают больше влияния.

---

## 4. Digital Advisor

Прослойка между консенсусом и пользователем. Учитывает:

- **Профиль риска** — консервативный / умеренный / агрессивный
- **Размер позиции** — Kelly Criterion с модификацией
- **Текущий портфель** — корреляция с существующими позициями
- **Рыночный режим** — trending / ranging / high-volatility

---

## 5. Orchestrator (Координатор)

Управляет жизненным циклом агентов через Celery:

- **Scheduling** — запуск агентов по расписанию или по событию
- **Health monitoring** — проверка здоровья агентов, автоматический restart
- **Timeout management** — если агент не ответил за 5 сек, пропускаем его
- **Resource management** — ограничение параллельных GPU-задач

---

## 6. API Layer

### REST API (FastAPI)
- `GET /api/v1/signals/{symbol}` — текущий сигнал
- `GET /api/v1/portfolio` — состояние портфеля
- `POST /api/v1/profile` — обновить профиль риска
- `GET /api/v1/agents/status` — здоровье агентов

### WebSocket
- `/ws/signals` — real-time поток сигналов
- `/ws/agents` — статусы агентов в реальном времени

### Telegram Bot
- Основной пользовательский интерфейс
- Команды: `/signal BTC`, `/portfolio`, `/risk`, `/history`
- Push-уведомления при сильных сигналах

---

## 7. Deployment

Минимальные требования: 2 vCPU, 4GB RAM, 20GB SSD (без GPU для inference — используем cloud API или quantized модели).

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    depends_on: [redis, timescaledb]
  
  celery-worker:
    build: .
    command: celery -A src.core.orchestrator worker
    deploy:
      replicas: 2
  
  redis:
    image: redis:7-alpine
  
  timescaledb:
    image: timescale/timescaledb:latest-pg15
  
  telegram-bot:
    build: .
    command: python -m src.api.telegram
```
