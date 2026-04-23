from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveAttachmentCommand:
    """Команда: удаление вложения из объявления"""
    
    announcement_id: str
    file_id: str
    
    def __post_init__(self):
        if not self.announcement_id or not self.announcement_id.strip():
            raise ValueError("announcement_id не может быть пустым")
        
        if not self.file_id or not self.file_id.strip():
            raise ValueError("file_id не может быть пустым")
