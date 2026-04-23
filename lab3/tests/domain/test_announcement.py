import pytest
from datetime import datetime, timedelta
from src.domain.models.announcement import Announcement
from src.domain.value_objects.announcement_status import AnnouncementStatus
from src.domain.value_objects.file_attachment import FileAttachment
from src.domain.exceptions.domain_exception import DomainException


class TestAnnouncement:
    
    def setup_method(self):
        self.announcement = Announcement(
            announcement_id="ann-1",
            group_id="group-1",
            author_id="user-1",
            title="Важное объявление",
            content="Текст объявления"
        )
    
    def test_create_announcement_success(self):
        assert self.announcement.id == "ann-1"
        assert self.announcement.group_id == "group-1"
        assert self.announcement.author_id == "user-1"
        assert self.announcement.title == "Важное объявление"
        assert self.announcement.content == "Текст объявления"
        assert self.announcement.status == AnnouncementStatus.DRAFT
    
    def test_create_announcement_empty_title_raises_error(self):
        with pytest.raises(DomainException, match="Заголовок не может быть пустым"):
            Announcement(
                announcement_id="ann-2",
                group_id="group-1",
                author_id="user-1",
                title="",
                content="Текст"
            )
    
    def test_create_announcement_title_too_long_raises_error(self):
        long_title = "a" * 201
        with pytest.raises(DomainException, match="Заголовок не может быть длиннее 200 символов"):
            Announcement(
                announcement_id="ann-2",
                group_id="group-1",
                author_id="user-1",
                title=long_title,
                content="Текст"
            )
    
    def test_publish_draft_success(self):
        self.announcement.publish()
        assert self.announcement.status == AnnouncementStatus.PUBLISHED
        assert self.announcement.published_at is not None
        
        events = self.announcement.get_events()
        assert len(events) == 1
        assert events[0].get_name() == "announcement.published"
    
    def test_publish_already_published_raises_error(self):
        self.announcement.publish()
        
        with pytest.raises(DomainException, match="Объявление уже опубликовано"):
            self.announcement.publish()
    
    def test_schedule_success(self):
        future_date = datetime.now() + timedelta(days=1)
        self.announcement.schedule(future_date)
        
        assert self.announcement.status == AnnouncementStatus.SCHEDULED
        assert self.announcement.scheduled_for == future_date
    
    def test_schedule_past_date_raises_error(self):
        past_date = datetime.now() - timedelta(days=1)
        
        with pytest.raises(DomainException, match="Время публикации должно быть в будущем"):
            self.announcement.schedule(past_date)
    
    def test_schedule_non_draft_raises_error(self):
        self.announcement.publish()
        future_date = datetime.now() + timedelta(days=1)
        
        with pytest.raises(DomainException, match="Нельзя запланировать объявление в статусе"):
            self.announcement.schedule(future_date)
    
    def test_add_attachment_success(self):
        attachment = FileAttachment(
            file_id="file-1",
            filename="document.pdf",
            file_size=1024,
            mime_type="application/pdf",
            storage_path="/files/file-1.pdf"
        )
        
        self.announcement.add_attachment(attachment)
        
        assert len(self.announcement.attachments) == 1
        assert self.announcement.attachments[0].file_id == "file-1"
        
        events = self.announcement.get_events()
        assert events[0].get_name() == "announcement.attachment.added"
    
    def test_add_attachment_exceeds_limit_raises_error(self):
        for i in range(5):
            attachment = FileAttachment(
                file_id=f"file-{i}",
                filename=f"file{i}.pdf",
                file_size=1024,
                mime_type="application/pdf",
                storage_path=f"/files/file-{i}.pdf"
            )
            self.announcement.add_attachment(attachment)
        
        extra_attachment = FileAttachment(
            file_id="file-5",
            filename="extra.pdf",
            file_size=1024,
            mime_type="application/pdf",
            storage_path="/files/extra.pdf"
        )
        
        with pytest.raises(DomainException, match="Максимум 5 файлов"):
            self.announcement.add_attachment(extra_attachment)
    
    def test_remove_attachment_success(self):
        attachment = FileAttachment(
            file_id="file-1",
            filename="document.pdf",
            file_size=1024,
            mime_type="application/pdf",
            storage_path="/files/file-1.pdf"
        )
        self.announcement.add_attachment(attachment)
        
        self.announcement.remove_attachment("file-1")
        
        assert len(self.announcement.attachments) == 0
        
        events = self.announcement.get_events()
        assert events[-1].get_name() == "announcement.attachment.removed"
    
    def test_archive_published_success(self):
        self.announcement.publish()
        self.announcement.archive()
        
        assert self.announcement.status == AnnouncementStatus.ARCHIVED
    
    def test_update_content_only_in_draft(self):
        self.announcement.update_content("Новый заголовок", "Новый текст")
        
        assert self.announcement.title == "Новый заголовок"
        assert self.announcement.content == "Новый текст"
    
    def test_update_content_in_published_raises_error(self):
        self.announcement.publish()
        
        with pytest.raises(DomainException, match="Нельзя изменить объявление в статусе"):
            self.announcement.update_content("Новый заголовок", "Новый текст")
    
    def test_equality_by_id(self):
        ann1 = Announcement("same-id", "group-1", "user-1", "Title", "Content")
        ann2 = Announcement("same-id", "group-2", "user-2", "Different", "Different")
        
        assert ann1 == ann2
        assert hash(ann1) == hash(ann2)
