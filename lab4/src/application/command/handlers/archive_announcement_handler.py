from ...port.out.announcement_repository import AnnouncementRepository
from ..archive_announcement_command import ArchiveAnnouncementCommand


class ArchiveAnnouncementHandler:
    """Обработчик команды архивации объявления"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, command: ArchiveAnnouncementCommand) -> None:
        """
        Архивировать объявление
        
        Шаги:
        1. Загрузить Announcement
        2. Вызвать метод archive()
        3. Сохранить изменения
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        announcement.archive()
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
