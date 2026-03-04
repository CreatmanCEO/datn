# DATN — Дорожная карта разработки

## Фаза 0: Фундамент (1-2 недели)

**Цель:** Рабочий скелет проекта, CI/CD, базовая инфраструктура.

- [ ] Структура проекта (pyproject.toml, src layout)
- [ ] Docker Compose: Redis + TimescaleDB + API
- [ ] GitHub Actions: lint + test + build
- [ ] Базовые модели Pydantic (AgentSignal, UserProfile, etc.)
- [ ] BaseAgent интерфейс
- [ ] Логирование (structlog)
- [ ] Конфигурация через .env

**Результат:** `docker-compose up` запускает пустую платформу с API и БД.

---

## Фаза 1: Data Pipeline (2-3 недели)

**Цель:** Надёжный сбор и хранение рыночных данных.

- [ ] Коннектор Binance WebSocket (real-time OHLCV)
- [ ] Коннектор MOEX (REST, через ISS API)
- [ ] News aggregator (RSS + Telegram parser)
- [ ] TimescaleDB schema + migrations (Alembic)
- [ ] Data validation и дедупликация
- [ ] Historical data backfill script
- [ ] Health checks для каждого источника

**Результат:** В базе копится market data в реальном времени.

---

## Фаза 2: Агенты (3-4 недели)

**Цель:** Все 4 агента работают и генерируют сигналы.

- [ ] TechnicalAgent (TA-Lib) — самый простой, начинаем с него
- [ ] AnomalyAgent (Isolation Forest + Z-score)
- [ ] SentimentAgent (FinBERT) — требует GPU или cloud inference
- [ ] ForecastAgent (Chronos-T5) — самый тяжёлый
- [ ] Unit tests для каждого агента
- [ ] Backtesting framework (прогон на исторических данных)
- [ ] Метрики агентов: accuracy, latency, signal distribution

**Результат:** Агенты анализируют live данные и генерируют сигналы.

---

## Фаза 3: Consensus + Advisor (2-3 недели)

**Цель:** Консенсус-движок объединяет сигналы, советник даёт рекомендации.

- [ ] Bayesian Consensus Engine
- [ ] Адаптивные веса (EMA accuracy tracking)
- [ ] Digital Advisor с Kelly Criterion
- [ ] Risk management (max drawdown, position limits)
- [ ] Orchestrator (Celery + Redis)
- [ ] Backtesting всего pipeline end-to-end
- [ ] Performance dashboard (Grafana)

**Результат:** Полный pipeline от данных до рекомендации.

---

## Фаза 4: Интерфейсы (2-3 недели)

**Цель:** Пользователи могут взаимодействовать с системой.

- [ ] FastAPI REST endpoints
- [ ] WebSocket для real-time сигналов
- [ ] Telegram Bot (aiogram 3)
- [ ] User profiles + authentication
- [ ] Signal history + analytics
- [ ] Push-уведомления через Telegram

**Результат:** Рабочий продукт, доступный через Telegram бота.

---

## Фаза 5: Продакшн (2-3 недели)

**Цель:** Стабильная работа 24/7.

- [ ] Мониторинг (Prometheus + Grafana)
- [ ] Alerting (агент упал, данные не приходят, etc.)
- [ ] Rate limiting + API keys
- [ ] Database backup strategy
- [ ] Graceful degradation (работа при отказе агентов)
- [ ] Load testing
- [ ] Documentation site (MkDocs)

**Результат:** Production-ready платформа.

---

## Фаза 6: Расширение (ongoing)

- Новые агенты: OrderFlow Agent, Options Agent, Correlation Agent
- Paper trading → live trading integration
- Multi-exchange support
- Web dashboard (React/Next.js)
- Mobile app
- Multi-user SaaS
- Marketplace агентов (пользователи создают своих)

---

## Оценка ресурсов

| Фаза | Время | Основные риски |
|------|-------|----------------|
| 0. Фундамент | 1-2 нед | — |
| 1. Data Pipeline | 2-3 нед | API rate limits, парсинг новостей |
| 2. Агенты | 3-4 нед | GPU для FinBERT/Chronos, точность |
| 3. Consensus | 2-3 нед | Калибровка весов, overfitting |
| 4. Интерфейсы | 2-3 нед | — |
| 5. Продакшн | 2-3 нед | Стабильность 24/7 |
| **Итого до MVP** | **~12-16 нед** | |

**Минимальная инфраструктура:**
- VPS: 2 vCPU, 4GB RAM, 40GB SSD (~$15/мес)
- GPU inference: HF Inference Endpoints или Replicate (~$5-20/мес)
- Binance API: бесплатно
- Telegram Bot: бесплатно
