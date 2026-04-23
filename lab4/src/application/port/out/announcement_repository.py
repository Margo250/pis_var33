from abc import ABC, abstractmethod
from typing import List, Optional


class AnnouncementRepository(ABC):
    """Исходящий порт: репозиторий объявлений"""
    
    @abstractmethod
    def save(self, announcement) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, announcement_id: str):
        pass
    
    @abstractmethod
    def find_by_group(self, group_id: str, limit: int = 50, offset: int = 0) -> List:
        """Найти объявления в группе"""
        pass
    
    @abstractmethod
    def find_by_author(self, author_id: str, limit: int = 50, offset: int = 0) -> List:
        """Найти объявления автора"""
        pass
    
    @abstractmethod
    def delete(self, announcement_id: str) -> bool:
        pass
