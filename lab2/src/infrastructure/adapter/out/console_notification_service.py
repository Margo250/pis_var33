from ....application.port.out.notification_service import NotificationService

class ConsoleNotificationService(NotificationService):
    def send_announcement_published(self, announcement_id: str, group_id: str) -> None:
        print(f"[NOTIFICATION] Announcement {announcement_id} published to group {group_id}")
