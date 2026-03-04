"""Base agent interface for DATN.

All agents must implement this abstract class to participate
in the consensus engine.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass
class AgentSignal:
    """Standardized signal format produced by all agents."""

    agent_id: str
    symbol: str
    timestamp: datetime
    direction: float  # -1.0 (strong sell) to +1.0 (strong buy)
    confidence: float  # 0.0 to 1.0
    horizon: timedelta
    reasoning: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not -1.0 <= self.direction <= 1.0:
            raise ValueError(f"direction must be in [-1, 1], got {self.direction}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence}")


class BaseAgent(ABC):
    """Abstract base class for all DATN agents.

    Each agent:
    1. Subscribes to relevant Kafka topics for input data
    2. Processes data according to its specialization
    3. Produces standardized AgentSignal objects
    4. Publishes signals to its output Kafka topic
    """

    def __init__(self, agent_id: str, config: dict[str, Any]) -> None:
        self.agent_id = agent_id
        self.config = config
        self._is_running = False

    @abstractmethod
    async def initialize(self) -> None:
        """Load models, connect to data sources, prepare for processing."""
        ...

    @abstractmethod
    async def process(self, symbol: str) -> AgentSignal | None:
        """Analyze current data and produce a signal for the given symbol.

        Returns None if insufficient data or confidence too low.
        """
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        """Clean up resources."""
        ...

    @property
    @abstractmethod
    def input_topics(self) -> list[str]:
        """Kafka topics this agent subscribes to."""
        ...

    @property
    def output_topic(self) -> str:
        """Kafka topic this agent publishes signals to."""
        return f"signals.{self.agent_id}"

    async def health_check(self) -> bool:
        """Return True if agent is operational."""
        return self._is_running
