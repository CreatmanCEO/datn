"""Tests for the Bayesian consensus engine."""

from datetime import datetime, timedelta

from agents.base import AgentSignal
from consensus.engine import ConsensusEngine


def _make_signal(
    agent_id: str,
    direction: float,
    confidence: float,
    symbol: str = "BTC/USDT",
) -> AgentSignal:
    return AgentSignal(
        agent_id=agent_id,
        symbol=symbol,
        timestamp=datetime.utcnow(),
        direction=direction,
        confidence=confidence,
        horizon=timedelta(hours=4),
        reasoning="test signal",
    )


def test_equal_weight_consensus() -> None:
    engine = ConsensusEngine(["agent_a", "agent_b", "agent_c"])
    signals = [
        _make_signal("agent_a", 0.8, 0.9),
        _make_signal("agent_b", 0.6, 0.8),
        _make_signal("agent_c", 0.7, 0.85),
    ]
    result = engine.compute_consensus(signals)
    assert result.direction > 0, "Should be bullish"
    assert result.confidence > 0.5
    assert result.agreement_score > 0.8, "Agents mostly agree"
    assert len(result.risk_flags) == 0


def test_disagreement_flags() -> None:
    engine = ConsensusEngine(["agent_a", "agent_b"])
    signals = [
        _make_signal("agent_a", 0.9, 0.9),
        _make_signal("agent_b", -0.8, 0.9),
    ]
    result = engine.compute_consensus(signals)
    assert "LOW_AGREEMENT" in result.risk_flags


def test_low_confidence_flag() -> None:
    engine = ConsensusEngine(["agent_a", "agent_b"])
    signals = [
        _make_signal("agent_a", 0.5, 0.2),  # low confidence
        _make_signal("agent_b", 0.6, 0.9),
    ]
    result = engine.compute_consensus(signals)
    assert "LOW_CONFIDENCE_AGENT" in result.risk_flags


def test_weight_update() -> None:
    engine = ConsensusEngine(["agent_a", "agent_b"])
    initial_a = engine.weights["agent_a"]
    engine.update_weights("agent_a", was_correct=True)
    assert engine.weights["agent_a"] > initial_a


def test_indecisive_flag() -> None:
    engine = ConsensusEngine(["agent_a", "agent_b"])
    signals = [
        _make_signal("agent_a", 0.05, 0.9),
        _make_signal("agent_b", -0.05, 0.9),
    ]
    result = engine.compute_consensus(signals)
    assert "INDECISIVE" in result.risk_flags
