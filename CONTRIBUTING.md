# Contributing to DATN

## Development Setup

```bash
# Clone
git clone https://github.com/CreatmanCEO/datn.git
cd datn

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Start infrastructure
docker-compose up -d postgres redis kafka

# Run tests
pytest

# Run linters
ruff check .
mypy .
```

## Code Style

- Python 3.11+
- Type hints on all functions
- Docstrings (Google style)
- Ruff for linting and formatting
- mypy strict mode

## Branch Strategy

- `main` — stable, deployable
- `develop` — integration branch
- `feature/*` — new features
- `fix/*` — bug fixes

## Commit Messages

Follow Conventional Commits:
```
feat(agent): add RSI divergence detection
fix(consensus): correct weight normalization
docs(api): update endpoint descriptions
test(forecaster): add backtest for BTC/USDT
```

## Adding a New Agent

1. Create a new directory under `agents/`
2. Implement the `BaseAgent` interface
3. Define Kafka input/output topics
4. Add configuration to `config/agents.yaml`
5. Write tests with sample data
6. Update docs/components.md
7. Submit PR with description of agent's strategy

## Priority list

1. Wire backtesting harness into the consensus engine
2. Flesh out FinBERT sentiment agent with live news feed
3. Chronos-T5 forecaster — first working pipeline + caching
4. Risk profile and position sizing in `advisor/`
5. REST API surface + OpenAPI doc generation
6. Telegram bot MVP commands
7. Increase test coverage beyond `consensus/`

## PR checklist

- [ ] Branch follows `feature/*` or `fix/*` naming
- [ ] `ruff check .` passes
- [ ] `mypy .` passes
- [ ] `pytest` passes locally
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No secrets, model checkpoints, or large fixtures committed
- [ ] PR description explains the *why*, not just the *what*
