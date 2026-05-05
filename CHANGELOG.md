# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- README rewritten with badges row, why/how/limitations, and Related ecosystem block
- `CHANGELOG.md` reconstructed from git history
- `.github/workflows/validate.yml` — Python compile, meta-files presence, README sections, pyproject TOML validation
- Topics list and PR checklist consolidated in `CONTRIBUTING.md`

## [0.1.0] — Initial scaffold

### Added
- Project scaffold for Distributed AI Trading Network
- Initial README with project overview
- Architecture overview (`docs/architecture.md`)
- AI agents specification (`docs/AGENTS.md`)
- API documentation (`docs/API.md`)
- Components specification (`docs/components.md`)
- Development roadmap (`docs/roadmap.md`)
- `pyproject.toml` with full dependency set (FastAPI, PyTorch, Transformers, Chronos-T5, ccxt, ta-lib, aiogram, anthropic, structlog)
- `docker-compose.yml` for local stack
- Skeletons for `agents/` (sentiment, forecaster, technical), `consensus/`, `advisor/`, `data/`, `api/`, `bot/`, `config/`
- Initial `tests/test_consensus.py`
- MIT License
- `CONTRIBUTING.md`

[Unreleased]: https://github.com/CreatmanCEO/datn/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/CreatmanCEO/datn/releases/tag/v0.1.0
