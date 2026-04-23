from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send_announcement_published(self, announcement_id: str, group_id: str) -> None:
        pass
