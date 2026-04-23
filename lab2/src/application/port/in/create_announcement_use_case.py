from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CreateAnnouncementCommand:
    group_id: str
    author_id: str
    title: str
    content: str
    attachment_ids: Optional[List[str]] = None

class CreateAnnouncementUseCase(ABC):
    @abstractmethod
    def create_announcement(self, command: CreateAnnouncementCommand) -> str:
        pass
