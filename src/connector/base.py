from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """连接器基类"""

    name: str = "base"
    description: str = "基础连接器"

    @abstractmethod
    def connect(self, **kwargs) -> Any:
        """建立连接"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass

    @abstractmethod
    def send(self, message: str) -> str:
        """发送消息"""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name})>"
