# DATN — Distributed AI Trading Network

**Мультиагентная торговая платформа с байесовским консенсусом и адаптивным цифровым советником**

## Что это

DATN — это распределённая система, где несколько AI-агентов независимо анализируют финансовые рынки, а затем приходят к общему решению через механизм байесовского консенсуса. Каждый агент специализируется на своём типе анализа: один читает новости, другой анализирует графики, третий отслеживает аномалии. Итоговое решение — не среднее арифметическое, а взвешенный консенсус с учётом исторической точности каждого агента.

Поверх агентов работает Digital Advisor — адаптивный советник, который учитывает профиль риска пользователя и переводит сигналы агентов в конкретные рекомендации.

## Ключевые компоненты

| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| Sentiment Agent | FinBERT | Анализ тональности финансовых новостей и соцсетей |
| Forecast Agent | Chronos-T5 | Прогнозирование временных рядов (цены, объёмы) |
| Anomaly Agent | Isolation Forest + Z-score | Детекция аномалий и нетипичных паттернов |
| Technical Agent | TA-Lib + Custom indicators | Классический технический анализ |
| Consensus Engine | Bayesian Aggregation | Взвешенное объединение сигналов агентов |
| Digital Advisor | Risk-adjusted recommendations | Персонализированные рекомендации для пользователя |
| Orchestrator | Celery + Redis | Координация агентов и управление задачами |

## Технологический стек

- **Python 3.11+** — основной язык
- **FastAPI** — REST API + WebSocket
- **Celery + Redis** — распределённые задачи и очередь сообщений
- **FinBERT** (ProsusAI/finbert) — анализ тональности финансовых текстов
- **Chronos-T5** (Amazon) — probabilistic time series forecasting
- **scikit-learn** — Isolation Forest для детекции аномалий
- **TA-Lib** — технические индикаторы
- **TimescaleDB** — хранение временных рядов
- **Docker + Docker Compose** — контейнеризация
- **Telegram Bot API** — пользовательский интерфейс

## Документация

- [Архитектура системы](docs/ARCHITECTURE.md)
- [AI-агенты](docs/AGENTS.md)
- [API](docs/API.md)
- [Дорожная карта](docs/ROADMAP.md)

## Быстрый старт

```bash
git clone https://github.com/CreatmanCEO/datn.git
cd datn
pip install -e ".[dev]"
cp .env.example .env
docker-compose up -d
python -m src.api.rest
```

## Лицензия

MIT

## Автор

**Nik Podolyak** — Python Developer & Digital Architect
[creatman.site](https://creatman.site) | [GitHub](https://github.com/CreatmanCEO)
