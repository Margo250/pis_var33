from ...port.out.announcement_repository import AnnouncementRepository
from ..remove_attachment_command import RemoveAttachmentCommand


class RemoveAttachmentHandler:
    """Обработчик команды удаления вложения"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, command: RemoveAttachmentCommand) -> None:
        """
        Удалить вложение из объявления
        
        Шаги:
        1. Загрузить Announcement
        2. Вызвать метод remove_attachment()
        3. Сохранить изменения
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        announcement.remove_attachment(command.file_id)
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
