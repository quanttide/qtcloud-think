from importlib.metadata import entry_points
import sys
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from connector.base import BaseConnector

from connector.base import BaseConnector


class ConnectorRegistry:
    """连接器注册器"""

    _instance = None
    _connectors: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_connectors()
        return cls._instance

    def _load_connectors(self) -> None:
        """从 entry points 加载所有连接器"""
        try:
            if sys.version_info >= (3, 10):
                eps = entry_points(group="qtcloud.connectors")
            else:
                eps = entry_points().get("qtcloud.connectors", [])
        except TypeError:
            eps = []

        for ep in eps:
            try:
                connector_class = ep.load()
                self._connectors[ep.name] = connector_class
            except Exception as e:
                print(f"Warning: Failed to load connector '{ep.name}': {e}")

    def register(self, name: str, connector_class: Type[BaseConnector]) -> None:
        """手动注册连接器"""
        self._connectors[name] = connector_class

    def get(self, name: str) -> Type[BaseConnector] | None:
        """获取连接器类"""
        return self._connectors.get(name)

    def list_all(self) -> dict[str, Type[BaseConnector]]:
        """列出所有已注册的连接器"""
        return self._connectors.copy()

    def names(self) -> list[str]:
        """列出所有连接器名称"""
        return list(self._connectors.keys())


def get_registry() -> ConnectorRegistry:
    """获取连接器注册器单例"""
    return ConnectorRegistry()
