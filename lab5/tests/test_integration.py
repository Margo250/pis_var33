import pytest
from fastapi.testclient import TestClient


class TestAnnouncementAPI:
    
    def test_create_announcement_success(self, client: TestClient):
        response = client.post("/api/announcements/", json={
            "group_id": "group-123",
            "author_id": "user-456",
            "title": "Test Announcement",
            "content": "This is a test announcement"
        })
        
        assert response.status_code == 201
        assert "announcement_id" in response.json()
    
    def test_create_announcement_empty_title(self, client: TestClient):
        response = client.post("/api/announcements/", json={
            "group_id": "group-123",
            "author_id": "user-456",
            "title": "",
            "content": "Content"
        })
        
        assert response.status_code == 400
        assert "title" in response.json()["detail"].lower()
    
    def test_get_announcement_not_found(self, client: TestClient):
        response = client.get("/api/announcements/non-existent-id")
        
        assert response.status_code == 404
    
    def test_publish_announcement(self, client: TestClient):
        # Сначала создаём
        create_resp = client.post("/api/announcements/", json={
            "group_id": "group-123",
            "author_id": "user-456",
            "title": "To Publish",
            "content": "Content"
        })
        announcement_id = create_resp.json()["announcement_id"]
        
        # Потом публикуем
        response = client.post("/api/announcements/publish", json={
            "announcement_id": announcement_id
        })
        
        assert response.status_code == 200
        assert "published" in response.json()["message"]
    
    def test_list_by_group(self, client: TestClient):
        # Создаём несколько объявлений
        for i in range(3):
            client.post("/api/announcements/", json={
                "group_id": "group-test",
                "author_id": "user-456",
                "title": f"Title {i}",
                "content": f"Content {i}"
            })
        
        response = client.get("/api/announcements/?group_id=group-test&limit=10")
        
        assert response.status_code == 200
        assert len(response.json()) == 3
