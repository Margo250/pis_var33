from datetime import datetime
from .domain_event import DomainEvent


class AnnouncementPublishedEvent(DomainEvent):
    """Событие: объявление опубликовано"""
    
    def __init__(self, announcement_id: str, group_id: str, published_at: datetime):
        self._announcement_id = announcement_id
        self._group_id = group_id
        self._occurred_at = published_at
    
    @property
    def announcement_id(self) -> str:
        return self._announcement_id
    
    @property
    def group_id(self) -> str:
        return self._group_id
    
    def occurred_at(self) -> datetime:
        return self._occurred_at
    
    def get_name(self) -> str:
        return "announcement.published"


class AnnouncementScheduledEvent(DomainEvent):
    """Событие: объявление запланировано"""
    
    def __init__(self, announcement_id: str, scheduled_for: datetime):
        self._announcement_id = announcement_id
        self._scheduled_for = scheduled_for
        self._occurred_at = datetime.now()
    
    @property
    def announcement_id(self) -> str:
        return self._announcement_id
    
    @property
    def scheduled_for(self) -> datetime:
        return self._scheduled_for
    
    def occurred_at(self) -> datetime:
        return self._occurred_at
    
    def get_name(self) -> str:
        return "announcement.scheduled"


class AnnouncementArchivedEvent(DomainEvent):
    """Событие: объявление архивировано"""
    
    def __init__(self, announcement_id: str):
        self._announcement_id = announcement_id
        self._occurred_at = datetime.now()
    
    @property
    def announcement_id(self) -> str:
        return self._announcement_id
    
    def occurred_at(self) -> datetime:
        return self._occurred_at
    
    def get_name(self) -> str:
        return "announcement.archived"


class AttachmentAddedEvent(DomainEvent):
    """Событие: вложение добавлено"""
    
    def __init__(self, announcement_id: str, file_id: str, filename: str):
        self._announcement_id = announcement_id
        self._file_id = file_id
        self._filename = filename
        self._occurred_at = datetime.now()
    
    @property
    def announcement_id(self) -> str:
        return self._announcement_id
    
    @property
    def file_id(self) -> str:
        return self._file_id
    
    @property
    def filename(self) -> str:
        return self._filename
    
    def occurred_at(self) -> datetime:
        return self._occurred_at
    
    def get_name(self) -> str:
        return "announcement.attachment.added"


class AttachmentRemovedEvent(DomainEvent):
    """Событие: вложение удалено"""
    
    def __init__(self, announcement_id: str, file_id: str):
        self._announcement_id = announcement_id
        self._file_id = file_id
        self._occurred_at = datetime.now()
    
    @property
    def announcement_id(self) -> str:
        return self._announcement_id
    
    @property
    def file_id(self) -> str:
        return self._file_id
    
    def occurred_at(self) -> datetime:
        return self._occurred_at
    
    def get_name(self) -> str:
        return "announcement.attachment.removed"
