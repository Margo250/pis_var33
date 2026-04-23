from abc import ABC, abstractmethod
from datetime import datetime


class DomainEvent(ABC):
    """Базовый интерфейс для доменных событий"""
    
    @abstractmethod
    def occurred_at(self) -> datetime:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
