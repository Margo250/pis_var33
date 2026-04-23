"""REST API контроллер для работы с объявлениями"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from ....application.port.in.announcement_service import AnnouncementService
from ....application.command.create_announcement_command import CreateAnnouncementCommand
from ....application.command.publish_announcement_command import PublishAnnouncementCommand
from ....application.command.schedule_announcement_command import ScheduleAnnouncementCommand
from ....application.command.add_attachment_command import AddAttachmentCommand
from ....application.command.remove_attachment_command import RemoveAttachmentCommand
from ....application.command.archive_announcement_command import ArchiveAnnouncementCommand
from ....application.command.update_announcement_content_command import UpdateAnnouncementContentCommand
from ....application.query.get_announcement_by_id_query import GetAnnouncementByIdQuery
from ....application.query.list_announcements_by_group_query import ListAnnouncementsByGroupQuery
from ....application.query.list_announcements_by_author_query import ListAnnouncementsByAuthorQuery
from ....domain.exceptions.domain_exception import DomainException

# Pydantic модели для запросов/ответов
class CreateAnnouncementRequest(BaseModel):
    group_id: str
    author_id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=5000)
    attachment_ids: Optional[List[str]] = None

class PublishAnnouncementRequest(BaseModel):
    announcement_id: str

class ScheduleAnnouncementRequest(BaseModel):
    announcement_id: str
    scheduled_for: datetime

class AddAttachmentRequest(BaseModel):
    announcement_id: str
    file_id: str
    filename: str
    file_size: int = Field(..., gt=0, le=10*1024*1024)
    mime_type: str
    storage_path: str

class RemoveAttachmentRequest(BaseModel):
    announcement_id: str
    file_id: str

class ArchiveAnnouncementRequest(BaseModel):
    announcement_id: str

class UpdateContentRequest(BaseModel):
    announcement_id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=5000)

class AnnouncementResponse(BaseModel):
    id: str
    group_id: str
    author_id: str
    title: str
    content: str
    status: str
    attachments: List[dict]
    created_at: datetime
    published_at: Optional[datetime]
    scheduled_for: Optional[datetime]
    updated_at: datetime


def create_router(service: AnnouncementService):
    """Создать роутер для FastAPI"""
    
    from fastapi import APIRouter
    router = APIRouter(prefix="/api/announcements", tags=["announcements"])
    
    @router.post("/", response_model=dict, status_code=201)
    async def create_announcement(request: CreateAnnouncementRequest):
        """Создать новое объявление"""
        try:
            command = CreateAnnouncementCommand(
                group_id=request.group_id,
                author_id=request.author_id,
                title=request.title,
                content=request.content,
                attachment_ids=request.attachment_ids
            )
            announcement_id = service.create_announcement(command)
            return {"announcement_id": announcement_id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.post("/publish", status_code=200)
    async def publish_announcement(request: PublishAnnouncementRequest):
        """Опубликовать объявление"""
        try:
            command = PublishAnnouncementCommand(announcement_id=request.announcement_id)
            service.publish_announcement(command)
            return {"message": "Announcement published successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.post("/schedule", status_code=200)
    async def schedule_announcement(request: ScheduleAnnouncementRequest):
        """Запланировать публикацию объявления"""
        try:
            command = ScheduleAnnouncementCommand(
                announcement_id=request.announcement_id,
                scheduled_for=request.scheduled_for
            )
            service.schedule_announcement(command)
            return {"message": "Announcement scheduled successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.post("/attachments", status_code=200)
    async def add_attachment(request: AddAttachmentRequest):
        """Добавить вложение к объявлению"""
        try:
            command = AddAttachmentCommand(
                announcement_id=request.announcement_id,
                file_id=request.file_id,
                filename=request.filename,
                file_size=request.file_size,
                mime_type=request.mime_type,
                storage_path=request.storage_path
            )
            service.add_attachment(command)
            return {"message": "Attachment added successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.delete("/attachments", status_code=200)
    async def remove_attachment(request: RemoveAttachmentRequest):
        """Удалить вложение из объявления"""
        try:
            command = RemoveAttachmentCommand(
                announcement_id=request.announcement_id,
                file_id=request.file_id
            )
            service.remove_attachment(command)
            return {"message": "Attachment removed successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.post("/archive", status_code=200)
    async def archive_announcement(request: ArchiveAnnouncementRequest):
        """Архивировать объявление"""
        try:
            command = ArchiveAnnouncementCommand(announcement_id=request.announcement_id)
            service.archive_announcement(command)
            return {"message": "Announcement archived successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.put("/content", status_code=200)
    async def update_content(request: UpdateContentRequest):
        """Обновить содержимое объявления"""
        try:
            command = UpdateAnnouncementContentCommand(
                announcement_id=request.announcement_id,
                title=request.title,
                content=request.content
            )
            service.update_announcement_content(command)
            return {"message": "Content updated successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DomainException as e:
            raise HTTPException(status_code=422, detail=str(e))
    
    @router.get("/{announcement_id}", response_model=AnnouncementResponse)
    async def get_announcement(announcement_id: str):
        """Получить объявление по ID"""
        try:
            query = GetAnnouncementByIdQuery(announcement_id=announcement_id)
            dto = service.get_announcement_by_id(query)
            return dto
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @router.get("/", response_model=List[AnnouncementResponse])
    async def list_by_group(group_id: str, limit: int = 50, offset: int = 0):
        """Список объявлений в группе"""
        try:
            query = ListAnnouncementsByGroupQuery(
                group_id=group_id,
                limit=limit,
                offset=offset
            )
            result = service.list_announcements_by_group(query)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.get("/author/{author_id}", response_model=List[AnnouncementResponse])
    async def list_by_author(author_id: str, limit: int = 50, offset: int = 0):
        """Список объявлений автора"""
        try:
            query = ListAnnouncementsByAuthorQuery(
                author_id=author_id,
                limit=limit,
                offset=offset
            )
            result = service.list_announcements_by_author(query)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    return router
