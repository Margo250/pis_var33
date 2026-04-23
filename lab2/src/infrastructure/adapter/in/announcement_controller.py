from ....application.port.in.create_announcement_use_case import CreateAnnouncementUseCase, CreateAnnouncementCommand
from ....application.port.in.get_announcement_use_case import GetAnnouncementUseCase

class AnnouncementController:
    def __init__(self, create_use_case: CreateAnnouncementUseCase, get_use_case: GetAnnouncementUseCase):
        self.create_use_case = create_use_case
        self.get_use_case = get_use_case
    
    def create_announcement(self, request_data: dict) -> dict:
        # TODO: реализовать в Lab #4
        pass
    
    def get_announcement(self, announcement_id: str) -> dict:
        # TODO: реализовать в Lab #4
        pass
