from typing import List
from ..port.in.announcement_service import AnnouncementService
from ..command.create_announcement_command import CreateAnnouncementCommand
from ..command.publish_announcement_command import PublishAnnouncementCommand
from ..command.schedule_announcement_command import ScheduleAnnouncementCommand
from ..command.add_attachment_command import AddAttachmentCommand
from ..command.remove_attachment_command import RemoveAttachmentCommand
from ..command.archive_announcement_command import ArchiveAnnouncementCommand
from ..command.update_announcement_content_command import UpdateAnnouncementContentCommand
from ..command.handlers.create_announcement_handler import CreateAnnouncementHandler
from ..command.handlers.publish_announcement_handler import PublishAnnouncementHandler
from ..command.handlers.schedule_announcement_handler import ScheduleAnnouncementHandler
from ..command.handlers.add_attachment_handler import AddAttachmentHandler
from ..command.handlers.remove_attachment_handler import RemoveAttachmentHandler
from ..command.handlers.archive_announcement_handler import ArchiveAnnouncementHandler
from ..command.handlers.update_announcement_content_handler import UpdateAnnouncementContentHandler
from ..query.get_announcement_by_id_query import GetAnnouncementByIdQuery
from ..query.list_announcements_by_group_query import ListAnnouncementsByGroupQuery
from ..query.list_announcements_by_author_query import ListAnnouncementsByAuthorQuery
from ..query.handlers.get_announcement_by_id_handler import GetAnnouncementByIdHandler
from ..query.handlers.list_announcements_by_group_handler import ListAnnouncementsByGroupHandler
from ..query.handlers.list_announcements_by_author_handler import ListAnnouncementsByAuthorHandler
from ...dto.announcement_dto import AnnouncementDTO


class AnnouncementServiceImpl(AnnouncementService):
    """Реализация фасада прикладного слоя"""
    
    def __init__(
        self,
        # Command Handlers
        create_handler: CreateAnnouncementHandler,
        publish_handler: PublishAnnouncementHandler,
        schedule_handler: ScheduleAnnouncementHandler,
        add_attachment_handler: AddAttachmentHandler,
        remove_attachment_handler: RemoveAttachmentHandler,
        archive_handler: ArchiveAnnouncementHandler,
        update_content_handler: UpdateAnnouncementContentHandler,
        # Query Handlers
        get_by_id_handler: GetAnnouncementByIdHandler,
        list_by_group_handler: ListAnnouncementsByGroupHandler,
        list_by_author_handler: ListAnnouncementsByAuthorHandler
    ):
        self._create_handler = create_handler
        self._publish_handler = publish_handler
        self._schedule_handler = schedule_handler
        self._add_attachment_handler = add_attachment_handler
        self._remove_attachment_handler = remove_attachment_handler
        self._archive_handler = archive_handler
        self._update_content_handler = update_content_handler
        self._get_by_id_handler = get_by_id_handler
        self._list_by_group_handler = list_by_group_handler
        self._list_by_author_handler = list_by_author_handler
    
    # === Команды ===
    
    def create_announcement(self, command: CreateAnnouncementCommand) -> str:
        return self._create_handler.handle(command)
    
    def publish_announcement(self, command: PublishAnnouncementCommand) -> None:
        self._publish_handler.handle(command)
    
    def schedule_announcement(self, command: ScheduleAnnouncementCommand) -> None:
        self._schedule_handler.handle(command)
    
    def add_attachment(self, command: AddAttachmentCommand) -> None:
        self._add_attachment_handler.handle(command)
    
    def remove_attachment(self, command: RemoveAttachmentCommand) -> None:
        self._remove_attachment_handler.handle(command)
    
    def archive_announcement(self, command: ArchiveAnnouncementCommand) -> None:
        self._archive_handler.handle(command)
    
    def update_announcement_content(self, command: UpdateAnnouncementContentCommand) -> None:
        self._update_content_handler.handle(command)
    
    # === Запросы ===
    
    def get_announcement_by_id(self, query: GetAnnouncementByIdQuery) -> AnnouncementDTO:
        return self._get_by_id_handler.handle(query)
    
    def list_announcements_by_group(self, query: ListAnnouncementsByGroupQuery) -> List[AnnouncementDTO]:
        return self._list_by_group_handler.handle(query)
    
    def list_announcements_by_author(self, query: ListAnnouncementsByAuthorQuery) -> List[AnnouncementDTO]:
        return self._list_by_author_handler.handle(query)
