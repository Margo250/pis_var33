from ...port.out.announcement_repository import AnnouncementRepository
from ...port.out.notification_service import NotificationService
from ..publish_announcement_command import PublishAnnouncementCommand


class PublishAnnouncementHandler:
    """Обработчик команды публикации объявления"""
    
    def __init__(
        self,
        repository: AnnouncementRepository,
        notification_service: NotificationService
    ):
        self._repository = repository
        self._notification_service = notification_service
    
    def handle(self, command: PublishAnnouncementCommand) -> None:
        """
        Опубликовать объявление
        
        Шаги:
        1. Загрузить Announcement из репозитория
        2. Вызвать метод publish() 
        3. Сохранить изменения
        4. Отправить уведомления
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        announcement.publish()
        
        self._repository.save(announcement)
        
        # Отправить уведомления участникам группы
        self._notification_service.send_announcement_published(
            announcement_id=announcement.id,
            group_id=announcement.group_id
        )
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
