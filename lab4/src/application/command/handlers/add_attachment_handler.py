from ....domain.value_objects.file_attachment import FileAttachment
from ...port.out.announcement_repository import AnnouncementRepository
from ..add_attachment_command import AddAttachmentCommand


class AddAttachmentHandler:
    """Обработчик команды добавления вложения"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, command: AddAttachmentCommand) -> None:
        """
        Добавить вложение к объявлению
        
        Шаги:
        1. Загрузить Announcement
        2. Создать FileAttachment (Value Object)
        3. Вызвать метод add_attachment()
        4. Сохранить изменения
        """
        announcement = self._repository.find_by_id(command.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {command.announcement_id}")
        
        attachment = FileAttachment(
            file_id=command.file_id,
            filename=command.filename,
            file_size=command.file_size,
            mime_type=command.mime_type,
            storage_path=command.storage_path
        )
        
        announcement.add_attachment(attachment)
        
        self._repository.save(announcement)
        
        # TODO: опубликовать доменные события
        events = announcement.get_events()
        for event in events:
            pass
        announcement.clear_events()
