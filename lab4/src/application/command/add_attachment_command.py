from dataclasses import dataclass


@dataclass(frozen=True)
class AddAttachmentCommand:
    """Команда: добавление вложения к объявлению"""
    
    announcement_id: str
    file_id: str
    filename: str
    file_size: int
    mime_type: str
    storage_path: str
    
    def __post_init__(self):
        if not self.announcement_id or not self.announcement_id.strip():
            raise ValueError("announcement_id не может быть пустым")
        
        if not self.file_id or not self.file_id.strip():
            raise ValueError("file_id не может быть пустым")
        
        if not self.filename or not self.filename.strip():
            raise ValueError("filename не может быть пустым")
        
        if self.file_size <= 0:
            raise ValueError(f"file_size должен быть положительным: {self.file_size}")
        
        if self.file_size > 10 * 1024 * 1024:
            raise ValueError(f"file_size не может превышать 10MB: {self.file_size}")
        
        if not self.mime_type or not self.mime_type.strip():
            raise ValueError("mime_type не может быть пустым")
        
        if not self.storage_path or not self.storage_path.strip():
            raise ValueError("storage_path не может быть пустым")
