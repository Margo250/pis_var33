from typing import List
from ...port.out.announcement_repository import AnnouncementRepository
from ...dto.announcement_dto import AnnouncementDTO
from ...dto.attachment_dto import AttachmentDTO
from ..list_announcements_by_author_query import ListAnnouncementsByAuthorQuery


class ListAnnouncementsByAuthorHandler:
    """Обработчик запроса списка объявлений автора"""
    
    def __init__(self, repository: AnnouncementRepository):
        self._repository = repository
    
    def handle(self, query: ListAnnouncementsByAuthorQuery) -> List[AnnouncementDTO]:
        """
        Получить список объявлений автора
        
        Шаги:
        1. Найти объявления в репозитории
        2. Преобразовать в DTO
        """
        # TODO: добавить метод find_by_author в репозиторий
        announcements = self._repository.find_by_author(
            author_id=query.author_id,
            limit=query.limit,
            offset=query.offset
        )
        
        return [self._to_dto(a) for a in announcements]
    
    def _to_dto(self, announcement) -> AnnouncementDTO:
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
