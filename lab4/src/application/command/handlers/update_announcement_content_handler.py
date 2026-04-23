from ...port.out.announcement_repository import AnnouncementRepository
from ..update_announcement_content_command import UpdateAnnouncementContentCommand


class UpdateAnnouncementContentHandler:
    """Обработчик команды обновления содержимого объявления"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, command: UpdateAnnouncementContentCommand) -> None:
        """
        Обновить содержимое объявления
        
        Шаги:
        1. Загрузить Announcement
        2. Вызвать метод update_content()
        3. Сохранить изменения
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        announcement.update_content(command.title, command.content)
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
