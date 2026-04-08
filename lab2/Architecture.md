# Архитектура Announcement Service

## Гексагональная архитектура (Ports & Adapters)

### Диаграмма

```plantuml
@startuml architecture
!theme plain
allowmixing

title Архитектура Announcement Service

package "Domain Layer" {
  class "Announcement" as A
  class "Group" as G
  class "User" as U
  enum "AnnouncementStatus" as S
  note right of A : Чистая бизнес-логика\nНе знает о фреймворках
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
    component "InMemory Repository" as InMem
    component "PostgreSQL Repository" as PG
    component "Console Notifier" as Console
    component "RabbitMQ Notifier" as MQ
  }
}

' Зависимости
REST ..> CreateUC : вызывает
REST ..> GetUC : вызывает

Service ..|> CreateUC : реализует
Service ..|> GetUC : реализует

Service ..> Repo : зависит
Service ..> Notif : зависит

InMem ..|> Repo : реализует
PG ..|> Repo : реализует
Console ..|> Notif : реализует
MQ ..|> Notif : реализует

Service --> A : создаёт

note bottom of Service
  <b>Dependency Rule</b>
  Infrastructure → Application → Domain
end note

@enduml
```

========== ПОЯСНЕНИЯ ==========

note right of Service
  <b>Dependency Rule</b>
  Зависимости направлены ВНУТРЬ
  Infrastructure → Application → Domain
  Domain ничего не знает о внешнем мире
end note

note bottom of REST
  <b>Входящий адаптер</b>
  Преобразует HTTP-запросы
  в вызовы use-case
end note

note bottom of PG
  <b>Исходящий адаптер</b>
  Реализует интерфейс репозитория
  Работает с реальной БД
end note

@enduml
