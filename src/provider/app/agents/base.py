from abc import ABC, abstractmethod
from typing import Any


class Agent(ABC):
    """智能体基类"""

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass
