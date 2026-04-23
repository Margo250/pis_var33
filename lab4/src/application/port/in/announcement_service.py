from abc import ABC, abstractmethod
from typing import List
from ...command.create_announcement_command import CreateAnnouncementCommand
from ...command.publish_announcement_command import PublishAnnouncementCommand
from ...command.schedule_announcement_command import ScheduleAnnouncementCommand
from ...command.add_attachment_command import AddAttachmentCommand
from ...command.remove_attachment_command import RemoveAttachmentCommand
from ...command.archive_announcement_command import ArchiveAnnouncementCommand
from ...command.update_announcement_content_command import UpdateAnnouncementContentCommand
from ...query.get_announcement_by_id_query import GetAnnouncementByIdQuery
from ...query.list_announcements_by_group_query import ListAnnouncementsByGroupQuery
from ...query.list_announcements_by_author_query import ListAnnouncementsByAuthorQuery
from ...dto.announcement_dto import AnnouncementDTO


class AnnouncementService(ABC):
    """Входящий порт: сервис управления объявлениями"""
    
    # === Команды ===
    
    @abstractmethod
    def create_announcement(self, command: CreateAnnouncementCommand) -> str:
        """Создать объявление"""
        pass
    
    @abstractmethod
    def publish_announcement(self, command: PublishAnnouncementCommand) -> None:
        """Опубликовать объявление"""
        pass
    
    @abstractmethod
    def schedule_announcement(self, command: ScheduleAnnouncementCommand) -> None:
        """Запланировать публикацию"""
        pass
    
    @abstractmethod
    def add_attachment(self, command: AddAttachmentCommand) -> None:
        """Добавить вложение"""
        pass
    
    @abstractmethod
    def remove_attachment(self, command: RemoveAttachmentCommand) -> None:
        """Удалить вложение"""
        pass
    
    @abstractmethod
    def archive_announcement(self, command: ArchiveAnnouncementCommand) -> None:
        """Архивировать объявление"""
        pass
    
    @abstractmethod
    def update_announcement_content(self, command: UpdateAnnouncementContentCommand) -> None:
        """Обновить содержимое"""
        pass
    
    # === Запросы ===
    
    @abstractmethod
    def get_announcement_by_id(self, query: GetAnnouncementByIdQuery) -> AnnouncementDTO:
        """Получить объявление по ID"""
        pass
    
    @abstractmethod
    def list_announcements_by_group(self, query: ListAnnouncementsByGroupQuery) -> List[AnnouncementDTO]:
        """Список объявлений в группе"""
        pass
    
    @abstractmethod
    def list_announcements_by_author(self, query: ListAnnouncementsByAuthorQuery) -> List[AnnouncementDTO]:
        """Список объявлений автора"""
        pass
