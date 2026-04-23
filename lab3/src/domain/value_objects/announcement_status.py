from enum import Enum


class AnnouncementStatus(Enum):
    """Value Object: Статус объявления"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    
    def __str__(self) -> str:
        return self.value
