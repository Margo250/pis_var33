"""Основной файл приложения FastAPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config.dependency_injection import DependencyContainer
from infrastructure.adapter.in.announcement_controller import create_router
from infrastructure.config.database import init_db

# Инициализация БД
init_db()

# Создание DI контейнера
container = DependencyContainer(use_postgres=True, use_rabbitmq=False)

# Создание FastAPI приложения
app = FastAPI(
    title="Announcement Service",
    description="Сервис управления объявлениями для органайзера группы",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(create_router(container.get_announcement_service()))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
