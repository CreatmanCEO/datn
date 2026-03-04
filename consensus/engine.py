"""Core Bayesian consensus engine.

Aggregates signals from multiple agents using dynamic Bayesian weights
that update based on historical agent accuracy.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from agents.base import AgentSignal


@dataclass
class ConsensusSignal:
    """Output of the consensus engine."""

    symbol: str
    timestamp: datetime
    direction: float
    confidence: float
    agreement_score: float
    agent_contributions: dict[str, dict[str, float]]
    risk_flags: list[str] = field(default_factory=list)


class ConsensusEngine:
    """Bayesian consensus engine for aggregating agent signals.

    Maintains per-agent weights that update based on prediction accuracy.
    Uses weighted averaging with agreement scoring and risk flag detection.
    """

    def __init__(self, agent_ids: list[str]) -> None:
        # Initialize with equal weights
        self.weights: dict[str, float] = {
            agent_id: 1.0 / len(agent_ids) for agent_id in agent_ids
        }
        self.performance_log: list[dict[str, Any]] = []

    def compute_consensus(self, signals: list[AgentSignal]) -> ConsensusSignal:
        """Aggregate multiple agent signals into a consensus."""
        if not signals:
            raise ValueError("Cannot compute consensus from empty signal list")

        # Weighted direction
        total_weight = sum(
            self.weights.get(s.agent_id, 0.0) * s.confidence for s in signals
        )
        if total_weight == 0:
            total_weight = 1.0

        consensus_direction = sum(
            s.direction * s.confidence * self.weights.get(s.agent_id, 0.0)
            for s in signals
        ) / total_weight

        # Agreement score (1.0 = perfect agreement, 0.0 = max disagreement)
        directions = [s.direction for s in signals]
        if len(directions) > 1:
            spread = max(directions) - min(directions)
            agreement = 1.0 - (spread / 2.0)  # normalize to [0, 1]
        else:
            agreement = 1.0

        # Combined confidence
        avg_confidence = sum(s.confidence for s in signals) / len(signals)
        consensus_confidence = avg_confidence * agreement

        # Risk flags
        risk_flags = self._detect_risk_flags(signals, agreement, consensus_direction)

        # Agent contributions
        contributions = {
            s.agent_id: {
                "direction": s.direction,
                "confidence": s.confidence,
                "weight": self.weights.get(s.agent_id, 0.0),
            }
            for s in signals
        }

        return ConsensusSignal(
            symbol=signals[0].symbol,
            timestamp=datetime.utcnow(),
            direction=consensus_direction,
            confidence=consensus_confidence,
            agreement_score=agreement,
            agent_contributions=contributions,
            risk_flags=risk_flags,
        )

    def update_weights(self, agent_id: str, was_correct: bool) -> None:
        """Bayesian weight update after trade outcome is known."""
        if agent_id not in self.weights:
            return

        # Simple multiplicative update
        if was_correct:
            self.weights[agent_id] *= 1.1
        else:
            self.weights[agent_id] *= 0.9

        # Normalize
        total = sum(self.weights.values())
        self.weights = {k: v / total for k, v in self.weights.items()}

    def _detect_risk_flags(
        self,
        signals: list[AgentSignal],
        agreement: float,
        direction: float,
    ) -> list[str]:
        """Detect potential risk conditions."""
        flags: list[str] = []

        if agreement < 0.4:
            flags.append("LOW_AGREEMENT")
        if any(s.confidence < 0.3 for s in signals):
            flags.append("LOW_CONFIDENCE_AGENT")
        if abs(direction) < 0.1:
            flags.append("INDECISIVE")
        if len(signals) < 2:
            flags.append("INSUFFICIENT_AGENTS")

        return flags
