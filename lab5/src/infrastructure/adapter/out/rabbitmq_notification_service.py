"""Реализация NotificationService с RabbitMQ"""

import json
import pika
from typing import Optional
from ....application.port.out.notification_service import NotificationService


class RabbitMQNotificationService(NotificationService):
    """RabbitMQ реализация сервиса уведомлений"""
    
    def __init__(self, host: str = "localhost", queue_name: str = "announcement_notifications"):
        self._host = host
        self._queue_name = queue_name
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.Channel] = None
    
    def _connect(self) -> None:
        """Установить соединение с RabbitMQ"""
        if not self._connection or self._connection.is_closed:
            parameters = pika.ConnectionParameters(host=self._host)
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue_name, durable=True)
    
    def _publish(self, message: dict) -> None:
        """Опубликовать сообщение в очередь"""
        self._connect()
        self._channel.basic_publish(
            exchange="",
            routing_key=self._queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent message
            )
        )
    
    def send_announcement_published(self, announcement_id: str, group_id: str) -> None:
        """Отправить уведомление о публикации объявления"""
        message = {
            "event_type": "announcement.published",
            "announcement_id": announcement_id,
            "group_id": group_id,
            "timestamp": None  # добавить datetime
        }
        self._publish(message)
    
    def close(self) -> None:
        """Закрыть соединение"""
        if self._connection and not self._connection.is_closed:
            self._connection.close()
