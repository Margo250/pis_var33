from abc import ABC, abstractmethod
from typing import Optional

class GetAnnouncementUseCase(ABC):
    @abstractmethod
    def get_announcement(self, announcement_id: str) -> Optional[dict]:
        pass
