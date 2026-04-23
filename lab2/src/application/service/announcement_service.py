from ..port.in.create_announcement_use_case import CreateAnnouncementUseCase, CreateAnnouncementCommand
from ..port.in.get_announcement_use_case import GetAnnouncementUseCase
from ..port.out.announcement_repository import AnnouncementRepository
from ..port.out.notification_service import NotificationService

class AnnouncementService(CreateAnnouncementUseCase, GetAnnouncementUseCase):
    def __init__(self, repository: AnnouncementRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service
    
    def create_announcement(self, command: CreateAnnouncementCommand) -> str:
        # TODO: реализовать в Lab #4
        raise NotImplementedError("Будет реализовано в Lab #4")
    
    def get_announcement(self, announcement_id: str):
        # TODO: реализовать в Lab #4
        raise NotImplementedError("Будет реализовано в Lab #4")
