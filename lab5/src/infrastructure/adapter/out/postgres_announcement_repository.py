"""Реализация AnnouncementRepository с PostgreSQL"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ....domain.models.announcement import Announcement
from ....domain.value_objects.announcement_status import AnnouncementStatus
from ....domain.value_objects.file_attachment import FileAttachment
from ....application.port.out.announcement_repository import AnnouncementRepository
from ...models.announcement_model import AnnouncementModel


class PostgresAnnouncementRepository(AnnouncementRepository):
    """PostgreSQL реализация репозитория объявлений"""
    
    def __init__(self, session: Session):
        self._session = session
    
    def save(self, announcement: Announcement) -> None:
        """Сохранить объявление (создать или обновить)"""
        model = self._session.query(AnnouncementModel).filter(
            AnnouncementModel.id == announcement.id
        ).first()
        
        attachments_json = [
            {
                "file_id": a.file_id,
                "filename": a.filename,
                "file_size": a.file_size,
                "mime_type": a.mime_type,
                "storage_path": a.storage_path
            }
            for a in announcement.attachments
        ]
        
        if model:
            # Обновление существующего
            model.title = announcement.title
            model.content = announcement.content
            model.status = announcement.status.value
            model.attachments = attachments_json
            model.published_at = announcement.published_at
            model.scheduled_for = announcement.scheduled_for
            model.updated_at = announcement.updated_at
        else:
            # Создание нового
            model = AnnouncementModel(
                id=announcement.id,
                group_id=announcement.group_id,
                author_id=announcement.author_id,
                title=announcement.title,
                content=announcement.content,
                status=announcement.status.value,
                attachments=attachments_json,
                created_at=announcement.created_at,
                published_at=announcement.published_at,
                scheduled_for=announcement.scheduled_for,
                updated_at=announcement.updated_at
            )
            self._session.add(model)
        
        self._session.commit()
    
    def find_by_id(self, announcement_id: str) -> Optional[Announcement]:
        """Найти объявление по ID"""
        model = self._session.query(AnnouncementModel).filter(
            AnnouncementModel.id == announcement_id
        ).first()
        
        if not model:
            return None
        
        return self._to_domain(model)
    
    def find_by_group(self, group_id: str, limit: int = 50, offset: int = 0) -> List[Announcement]:
        """Найти объявления в группе"""
        models = self._session.query(AnnouncementModel).filter(
            AnnouncementModel.group_id == group_id
        ).order_by(AnnouncementModel.created_at.desc()).offset(offset).limit(limit).all()
        
        return [self._to_domain(m) for m in models]
    
    def find_by_author(self, author_id: str, limit: int = 50, offset: int = 0) -> List[Announcement]:
        """Найти объявления автора"""
        models = self._session.query(AnnouncementModel).filter(
            AnnouncementModel.author_id == author_id
        ).order_by(AnnouncementModel.created_at.desc()).offset(offset).limit(limit).all()
        
        return [self._to_domain(m) for m in models]
    
    def delete(self, announcement_id: str) -> bool:
        """Удалить объявление"""
        model = self._session.query(AnnouncementModel).filter(
            AnnouncementModel.id == announcement_id
        ).first()
        
        if not model:
            return False
        
        self._session.delete(model)
        self._session.commit()
        return True
    
    def _to_domain(self, model: AnnouncementModel) -> Announcement:
        """Преобразовать ORM модель в доменный объект"""
        announcement = Announcement(
            announcement_id=model.id,
            group_id=model.group_id,
            author_id=model.author_id,
            title=model.title,
            content=model.content
        )
        
        # Восстановление статуса
        status_map = {
            "draft": AnnouncementStatus.DRAFT,
            "scheduled": AnnouncementStatus.SCHEDULED,
            "published": AnnouncementStatus.PUBLISHED,
            "archived": AnnouncementStatus.ARCHIVED
        }
        announcement._status = status_map.get(model.status, AnnouncementStatus.DRAFT)
        
        # Восстановление вложений
        for att in model.attachments:
            attachment = FileAttachment(
                file_id=att["file_id"],
                filename=att["filename"],
                file_size=att["file_size"],
                mime_type=att["mime_type"],
                storage_path=att["storage_path"]
            )
            announcement._attachments.append(attachment)
        
        announcement._created_at = model.created_at
        announcement._published_at = model.published_at
        announcement._scheduled_for = model.scheduled_for
        announcement._updated_at = model.updated_at
        
        return announcement
