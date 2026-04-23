from ....domain.models.announcement import Announcement
from ...port.out.announcement_repository import AnnouncementRepository
from ...dto.announcement_dto import AnnouncementDTO
from ...dto.attachment_dto import AttachmentDTO
from ..get_announcement_by_id_query import GetAnnouncementByIdQuery


class GetAnnouncementByIdHandler:
    """Обработчик запроса получения объявления по ID"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, query: GetAnnouncementByIdQuery) -> AnnouncementDTO:
        """
        Получить объявление по ID
        
        Шаги:
        1. Найти объявление в репозитории
        2. Преобразовать в DTO
        """
        announcement = self._repository.find_by_id(query.announcement_id)
        
        if not announcement:
            raise ValueError(f"Announcement not found: {query.announcement_id}")
        
        return self._to_dto(announcement)
    
    def _to_dto(self, announcement: Announcement) -> AnnouncementDTO:
        attachments = [
            AttachmentDTO(
                file_id=a.file_id,
                filename=a.filename,
                file_size=a.file_size,
                mime_type=a.mime_type
            )
            for a in announcement.attachments
        ]
        
        return AnnouncementDTO(
            id=announcement.id,
            group_id=announcement.group_id,
            author_id=announcement.author_id,
            title=announcement.title,
            content=announcement.content,
            status=announcement.status.value,
            attachments=attachments,
            created_at=announcement.created_at,
            published_at=announcement.published_at,
            scheduled_for=announcement.scheduled_for,
            updated_at=announcement.updated_at
        )
