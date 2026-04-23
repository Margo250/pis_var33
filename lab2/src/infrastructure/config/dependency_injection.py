from ...application.service.announcement_service import AnnouncementService
from ..adapter.out.in_memory_announcement_repository import InMemoryAnnouncementRepository
from ..adapter.out.console_notification_service import ConsoleNotificationService

class DependencyContainer:
    def __init__(self):
        self.announcement_repository = InMemoryAnnouncementRepository()
        self.notification_service = ConsoleNotificationService()
        
        self.announcement_service = AnnouncementService(
            repository=self.announcement_repository,
            notification_service=self.notification_service
        )
    
    def get_announcement_service(self) -> AnnouncementService:
        return self.announcement_service
