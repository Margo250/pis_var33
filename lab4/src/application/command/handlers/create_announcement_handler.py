import uuid
from typing import Optional, List
from ....domain.models.announcement import Announcement
from ....domain.value_objects.file_attachment import FileAttachment
from ....domain.exceptions.domain_exception import DomainException
from ...port.out.announcement_repository import AnnouncementRepository
from ...port.out.notification_service import NotificationService
from ..create_announcement_command import CreateAnnouncementCommand


class CreateAnnouncementHandler:
    """Обработчик команды создания объявления"""
    
    def __init__(
        self,
        repository: AnnouncementRepository,
        notification_service: Optional[NotificationService] = None
    ):
        self._repository = repository
        self._notification_service = notification_service
    
    def handle(self, command: CreateAnnouncementCommand) -> str:
        """
        Создать объявление
        
        Шаги:
        1. Сгенерировать ID
        2. Создать доменный объект Announcement
        3. Сохранить в репозиторий
        4. Вернуть ID
        """
        announcement_id = str(uuid.uuid4())
        
        announcement = Announcement(
            announcement_id=announcement_id,
            group_id=command.group_id,
            author_id=command.author_id,
            title=command.title,
            content=command.content
        )
        
        # Добавить вложения, если есть
        if command.attachment_ids:
            # TODO: загрузить файлы по ID из файлового сервиса
            pass
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            # В Lab #5 добавить EventBus.publish(event)
            pass
        announcement.clear_events()
        
        return announcement_id
