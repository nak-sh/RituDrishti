"""Real-source contract: one row per init × region × lead × hazard.

Raw proxies have explicit units. An operational adapter must also implement
availability time, version provenance and missing-value policy (no silent fill).
"""
from abc import ABC, abstractmethod
import pandas as pd

class ForecastAdapter(ABC):
    @abstractmethod
    def load(self, start: str, end: str) -> pd.DataFrame:
        """Return dated member/cycle/context proxies plus verifying observations."""
        raise NotImplementedError