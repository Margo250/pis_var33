"""DI-контейнер: связывание портов и адаптеров"""

from sqlalchemy.orm import Session
from ...application.service.announcement_service_impl import AnnouncementServiceImpl
from ...application.command.handlers.create_announcement_handler import CreateAnnouncementHandler
from ...application.command.handlers.publish_announcement_handler import PublishAnnouncementHandler
from ...application.command.handlers.schedule_announcement_handler import ScheduleAnnouncementHandler
from ...application.command.handlers.add_attachment_handler import AddAttachmentHandler
from ...application.command.handlers.remove_attachment_handler import RemoveAttachmentHandler
from ...application.command.handlers.archive_announcement_handler import ArchiveAnnouncementHandler
from ...application.command.handlers.update_announcement_content_handler import UpdateAnnouncementContentHandler
from ...application.query.handlers.get_announcement_by_id_handler import GetAnnouncementByIdHandler
from ...application.query.handlers.list_announcements_by_group_handler import ListAnnouncementsByGroupHandler
from ...application.query.handlers.list_announcements_by_author_handler import ListAnnouncementsByAuthorHandler
from ..adapter.out.postgres_announcement_repository import PostgresAnnouncementRepository
from ..adapter.out.rabbitmq_notification_service import RabbitMQNotificationService
from ..adapter.out.in_memory_announcement_repository import InMemoryAnnouncementRepository
from ..adapter.out.console_notification_service import ConsoleNotificationService
from .database import get_db


class DependencyContainer:
    """Конфигурация зависимостей"""
    
    def __init__(self, use_postgres: bool = True, use_rabbitmq: bool = True):
        self._use_postgres = use_postgres
        self._use_rabbitmq = use_rabbitmq
        self._session = None
        
        if use_postgres:
            # Для реального приложения - получаем сессию
            self._session = next(get_db())
            self.announcement_repository = PostgresAnnouncementRepository(self._session)
        else:
            # Для тестов
            self.announcement_repository = InMemoryAnnouncementRepository()
        
        if use_rabbitmq:
            self.notification_service = RabbitMQNotificationService()
        else:
            self.notification_service = ConsoleNotificationService()
        
        # Инициализация Command Handlers
        self._create_handler = CreateAnnouncementHandler(
            repository=self.announcement_repository,
            notification_service=self.notification_service
        )
        self._publish_handler = PublishAnnouncementHandler(
            repository=self.announcement_repository,
            notification_service=self.notification_service
        )
        self._schedule_handler = ScheduleAnnouncementHandler(self.announcement_repository)
        self._add_attachment_handler = AddAttachmentHandler(self.announcement_repository)
        self._remove_attachment_handler = RemoveAttachmentHandler(self.announcement_repository)
        self._archive_handler = ArchiveAnnouncementHandler(self.announcement_repository)
        self._update_content_handler = UpdateAnnouncementContentHandler(self.announcement_repository)
        
        # Инициализация Query Handlers
        self._get_by_id_handler = GetAnnouncementByIdHandler(self.announcement_repository)
        self._list_by_group_handler = ListAnnouncementsByGroupHandler(self.announcement_repository)
        self._list_by_author_handler = ListAnnouncementsByAuthorHandler(self.announcement_repository)
        
        # Application Service
        self.announcement_service = AnnouncementServiceImpl(
            create_handler=self._create_handler,
            publish_handler=self._publish_handler,
            schedule_handler=self._schedule_handler,
            add_attachment_handler=self._add_attachment_handler,
            remove_attachment_handler=self._remove_attachment_handler,
            archive_handler=self._archive_handler,
            update_content_handler=self._update_content_handler,
            get_by_id_handler=self._get_by_id_handler,
            list_by_group_handler=self._list_by_group_handler,
            list_by_author_handler=self._list_by_author_handler
        )
    
    def get_announcement_service(self) -> AnnouncementServiceImpl:
        return self.announcement_service
    
    def get_repository(self):
        return self.announcement_repository
    
    def close(self):
        if self._session:
            self._session.close()
        if hasattr(self.notification_service, 'close'):
            self.notification_service.close()
