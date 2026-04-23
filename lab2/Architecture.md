# Архитектура Announcement Service

## Диаграмма

```plantuml
@startuml
!theme plain
allowmixing

title Архитектура Announcement Service

package "Domain Layer" {
  class "Announcement" as A
  class "Group" as G
  class "User" as U
  enum "AnnouncementStatus" as S
}

package "Application Layer" {
  
  package "Inbound Ports" {
    interface "CreateAnnouncementUseCase" as CreateUC
    interface "GetAnnouncementUseCase" as GetUC
  }
  
  package "Outbound Ports" {
    interface "AnnouncementRepository" as Repo
    interface "NotificationService" as Notif
  }
  
  component "AnnouncementService" as Service
}

package "Infrastructure Layer" {
  
  package "Inbound Adapters" {
    component "REST Controller" as REST
  }
  
  package "Outbound Adapters" {
    component "PostgreSQL Repository" as PG
    component "InMemory Repository" as InMem
    component "RabbitMQ Notifier" as MQ
  }
}

REST ..> CreateUC
REST ..> GetUC

Service ..|> CreateUC
Service ..|> GetUC

Service ..> Repo
Service ..> Notif

PG ..|> Repo
InMem ..|> Repo
MQ ..|> Notif

Service --> A

@enduml
```
<img width="2387" height="458" alt="architecture" src="https://github.com/user-attachments/assets/8acb3074-b7e0-4053-90be-044690eb0899" />


## Domain Layer
- Announcement — сущность объявления
- Group — сущность группы
- User — сущность пользователя
- AnnouncementStatus — статусы (DRAFT, SCHEDULED, PUBLISHED, ARCHIVED)

Не зависит от других слоёв.

## Application Layer
Входящие порты:
- CreateAnnouncementUseCase — создание объявления
- GetAnnouncementUseCase — получение объявления
Исходящие порты:
- AnnouncementRepository — сохранение и загрузка
- NotificationService — уведомления

Сервис: AnnouncementService реализует входящие порты, зависит от исходящих.

## Infrastructure Layer
Входящие адаптеры:
- REST Controller — HTTP-эндпоинты
Исходящие адаптеры:
- PostgreSQL Repository — реальная БД
- InMemory Repository — для тестов
- RabbitMQ Notifier — очередь уведомлений

## Dependency Rule
Infrastructure → Application → Domain

Домен не знает о внешнем мире.
