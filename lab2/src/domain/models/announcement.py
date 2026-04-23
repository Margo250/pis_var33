class Announcement:
    def __init__(self, announcement_id: str, title: str, content: str, author_id: str):
        self.id = announcement_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.status = "DRAFT"
    
    def publish(self):
        self.status = "PUBLISHED"
