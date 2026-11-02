"""
Base driver interface for Gideon Agentic OS hardware/system abstractions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseDriver(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.is_active: bool = False

    @abstractmethod
    def initialize(self) -> bool:
        pass

    @abstractmethod
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        pass

    def shutdown(self):
        self.is_active = False
