from abc import ABC, abstractmethod

class AnnouncementRepository(ABC):
    @abstractmethod
    def save(self, announcement) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, announcement_id: str):
        pass
