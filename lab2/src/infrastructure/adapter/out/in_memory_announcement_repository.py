from ....application.port.out.announcement_repository import AnnouncementRepository

class InMemoryAnnouncementRepository(AnnouncementRepository):
    def __init__(self):
        self._storage = {}
    
    def save(self, announcement) -> None:
        self._storage[announcement.id] = announcement
    
    def find_by_id(self, announcement_id: str):
        return self._storage.get(announcement_id)
