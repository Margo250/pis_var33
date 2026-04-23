from ...port.out.announcement_repository import AnnouncementRepository
from ..schedule_announcement_command import ScheduleAnnouncementCommand


class ScheduleAnnouncementHandler:
    """Обработчик команды планирования публикации"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, command: ScheduleAnnouncementCommand) -> None:
        """
        Запланировать публикацию объявления
        
        Шаги:
        1. Загрузить Announcement
        2. Вызвать метод schedule()
        3. Сохранить изменения
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        announcement.schedule(command.scheduled_for)
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
