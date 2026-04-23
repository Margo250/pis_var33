from typing import List, Optional, Set
from datetime import datetime
from ..value_objects.announcement_status import AnnouncementStatus
from ..value_objects.file_attachment import FileAttachment
from ..exceptions.domain_exception import DomainException


class Announcement:
    """Aggregate Root: Объявление в группе"""
    
    MAX_ATTACHMENTS = 5
    MAX_TITLE_LENGTH = 200
    MAX_CONTENT_LENGTH = 5000
    
    def __init__(
        self,
        announcement_id: str,
        group_id: str,
        author_id: str,
        title: str,
        content: str
    ):
        self._id = announcement_id
        self._group_id = group_id
        self._author_id = author_id
        self._status = AnnouncementStatus.DRAFT
        self._attachments: List[FileAttachment] = []
        self._created_at = datetime.now()
        self._published_at: Optional[datetime] = None
        self._scheduled_for: Optional[datetime] = None
        self._updated_at = datetime.now()
        self._events: List[DomainEvent] = []
        
        self._set_title(title)
        self._set_content(content)
    
    # === Бизнес-методы ===
    
    def publish(self) -> None:
        """Опубликовать объявление"""
        if self._status == AnnouncementStatus.PUBLISHED:
            raise DomainException("Объявление уже опубликовано")
        
        if self._status == AnnouncementStatus.ARCHIVED:
            raise DomainException("Нельзя опубликовать архивное объявление")
        
        if self._status == AnnouncementStatus.SCHEDULED:
            if self._scheduled_for and self._scheduled_for > datetime.now():
                raise DomainException(f"Время публикации ещё не наступило: {self._scheduled_for}")
        
        self._status = AnnouncementStatus.PUBLISHED
        self._published_at = datetime.now()
        self._updated_at = datetime.now()
        
        self._register_event(AnnouncementPublishedEvent(
            announcement_id=self._id,
            group_id=self._group_id,
            published_at=self._published_at
        ))
    
    def schedule(self, scheduled_time: datetime) -> None:
        """Запланировать публикацию на будущее время"""
        if self._status != AnnouncementStatus.DRAFT:
            raise DomainException(f"Нельзя запланировать объявление в статусе {self._status}")
        
        if scheduled_time <= datetime.now():
            raise DomainException("Время публикации должно быть в будущем")
        
        self._status = AnnouncementStatus.SCHEDULED
        self._scheduled_for = scheduled_time
        self._updated_at = datetime.now()
        
        self._register_event(AnnouncementScheduledEvent(
            announcement_id=self._id,
            scheduled_for=scheduled_time
        ))
    
    def add_attachment(self, attachment: FileAttachment) -> None:
        """Добавить вложение"""
        if self._status != AnnouncementStatus.DRAFT:
            raise DomainException(f"Нельзя добавить вложение в статусе {self._status}")
        
        if len(self._attachments) >= self.MAX_ATTACHMENTS:
            raise DomainException(f"Максимум {self.MAX_ATTACHMENTS} файлов на объявление")
        
        if any(a.file_id == attachment.file_id for a in self._attachments):
            raise DomainException(f"Файл {attachment.file_id} уже прикреплён")
        
        self._attachments.append(attachment)
        self._updated_at = datetime.now()
        
        self._register_event(AttachmentAddedEvent(
            announcement_id=self._id,
            file_id=attachment.file_id,
            filename=attachment.filename
        ))
    
    def remove_attachment(self, file_id: str) -> None:
        """Удалить вложение"""
        if self._status != AnnouncementStatus.DRAFT:
            raise DomainException(f"Нельзя удалить вложение в статусе {self._status}")
        
        original_count = len(self._attachments)
        self._attachments = [a for a in self._attachments if a.file_id != file_id]
        
        if len(self._attachments) == original_count:
            raise DomainException(f"Файл {file_id} не найден")
        
        self._updated_at = datetime.now()
        
        self._register_event(AttachmentRemovedEvent(
            announcement_id=self._id,
            file_id=file_id
        ))
    
    def archive(self) -> None:
        """Архивировать объявление"""
        if self._status == AnnouncementStatus.ARCHIVED:
            raise DomainException("Объявление уже в архиве")
        
        self._status = AnnouncementStatus.ARCHIVED
        self._updated_at = datetime.now()
        
        self._register_event(AnnouncementArchivedEvent(
            announcement_id=self._id
        ))
    
    def update_content(self, title: str, content: str) -> None:
        """Обновить содержимое (только для черновика)"""
        if self._status != AnnouncementStatus.DRAFT:
            raise DomainException(f"Нельзя изменить объявление в статусе {self._status}")
        
        self._set_title(title)
        self._set_content(content)
        self._updated_at = datetime.now()
    
    # === Приватные методы валидации ===
    
    def _set_title(self, title: str) -> None:
        if not title or not title.strip():
            raise DomainException("Заголовок не может быть пустым")
        
        if len(title) > self.MAX_TITLE_LENGTH:
            raise DomainException(f"Заголовок не может быть длиннее {self.MAX_TITLE_LENGTH} символов")
        
        self._title = title.strip()
    
    def _set_content(self, content: str) -> None:
        if not content or not content.strip():
            raise DomainException("Содержимое не может быть пустым")
        
        if len(content) > self.MAX_CONTENT_LENGTH:
            raise DomainException(f"Содержимое не может быть длиннее {self.MAX_CONTENT_LENGTH} символов")
        
        self._content = content.strip()
    
    # === Доменные события ===
    
    def _register_event(self, event: DomainEvent) -> None:
        self._events.append(event)
    
    def get_events(self) -> List[DomainEvent]:
        return self._events.copy()
    
    def clear_events(self) -> None:
        self._events.clear()
    
    # === Геттеры ===
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def group_id(self) -> str:
        return self._group_id
    
    @property
    def author_id(self) -> str:
        return self._author_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def status(self) -> AnnouncementStatus:
        return self._status
    
    @property
    def attachments(self) -> List[FileAttachment]:
        return self._attachments.copy()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def published_at(self) -> Optional[datetime]:
        return self._published_at
    
    @property
    def scheduled_for(self) -> Optional[datetime]:
        return self._scheduled_for
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    # === Равенство по ID ===
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Announcement):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
