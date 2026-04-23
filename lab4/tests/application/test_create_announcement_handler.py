import pytest
from unittest.mock import Mock
from src.application.command.create_announcement_command import CreateAnnouncementCommand
from src.application.command.handlers.create_announcement_handler import CreateAnnouncementHandler


class TestCreateAnnouncementHandler:
    
    def setup_method(self):
        self.mock_repository = Mock()
        self.handler = CreateAnnouncementHandler(self.mock_repository)
    
    def test_handle_creates_announcement_success(self):
        command = CreateAnnouncementCommand(
            group_id="group-1",
            author_id="user-1",
            title="Test Title",
            content="Test Content"
        )
        
        announcement_id = self.handler.handle(command)
        
        assert announcement_id is not None
        assert self.mock_repository.save.called
    
    def test_handle_with_empty_group_id_raises_error(self):
        with pytest.raises(ValueError, match="group_id не может быть пустым"):
            CreateAnnouncementCommand(
                group_id="",
                author_id="user-1",
                title="Title",
                content="Content"
            )
    
    def test_handle_with_empty_title_raises_error(self):
        with pytest.raises(ValueError, match="title не может быть пустым"):
            CreateAnnouncementCommand(
                group_id="group-1",
                author_id="user-1",
                title="",
                content="Content"
            )
