# Restaurant Search 

Проект для поиска ресторанов по предпочтениям с AI помощником, сохранения избранного и получения данных из локальной базы и внешних источников.

## Цель проекта

Backend-проект, в котором я развиваю и демонстрирую свои навыки владения frameworks и инструментами для разработки:
- async Python;
- aiogram;
- PostgreSQL;
- SQLAlchemy;
- Alembic;
- FastAPI;
- Redis
- Kafka
- Celery
- CI/CD
- ML&LLM;
- архитектуры Repository/Service;
- интеграции с внешними API;
- тестирования.
- UI/UX;

## Текущий функционал

- Регистрация пользователя при /start
- Меню команд Telegram
- Просмотр ресторанов из базы
- Поиск ресторанов по названию/городу
- Фильтрация по рейтингу и среднему чеку
- Добавление ресторанов в избранное
- Удаление из избранного
- Внешний fallback-поиск через OpenStreetMap/Overpass
- Защита от дублей внешних ресторанов
- Базовые тесты

## Стек

Используется сейчас: 

- Python 3.12+
- aiogram 3.x
- PostgreSQL
- SQLAlchemy async
- Alembic
- Docker Compose
- httpx
- pytest
- pydantic-settings
- logging

Планируется:  

- FastAPI
- Redis
- JWT
- Google Places / 2GIS
- AI assistant
- background tasks
- CI/CD
- web UI

## Архитектура

Проект разделён на слои:

- `bot/handlers` - обработчики Telegram-команд
- `repositories` - работа с базой данных
- `services` - бизнес-логика
- `integrations` - внешние сервисы
- `db/models` - SQLAlchemy-модели
- `bot/formatters` - форматирование сообщений
- `bot/keyboards` - клавиатуры Telegram
- `tests` - тесты

## Статус проекта

Проект находится на стадии первой Telegram bot MVP-версии.

Сейчас фокус:
- улучшение UX;
- устойчивость bot handlers и подготовка API;

## Roadmap 

### v0.1.x - Telegram bot MVP
- [x] База данных и миграции
- [x] Пользователи
- [x] Рестораны
- [x] Избранное
- [x] Поиск по базе
- [x] Фильтры поиска
- [x] Интеграция с Overpass
- [x] Тесты fallback-поиска
- [x] Релиз v0.1.0
- [x] Улучшение UX сообщений
- [x] Telegram command menu
- [ ] Валидация пользовательского ввода
- [ ] Улучшение обработки ошибок в bot handlers
- [ ] Релиз v0.1.1
### v0.2.0 - API
- [ ] FastAPI-приложение
- [ ] API для ресторанов
- [ ] API для поиска
- [ ] API для избранного
- [ ] JWT-авторизация
- [ ] Pydantic-схемы для API
- [ ] Релиз v0.2.0
### v0.3.0 - External data improvements
- [ ] Кэширование внешнего поиска через Redis
- [ ] Интеграция Google Places / 2GIS
- [ ] Нормализация данных из разных источников
- [ ] Улучшение дедупликации ресторанов
- [ ] Релиз v0.3.0
### v0.4.0 - AI and recommendations
- [ ] AI-помощник для подбора ресторанов
- [ ] Рекомендации по предпочтениям пользователя
- [ ] История поиска
- [ ] Релиз v0.4.0
### Later
- [ ] Background tasks
- [ ] Celery/RabbitMQ или RQ
- [ ] Kafka?
- [ ] Web UI
- [ ] CI/CD
- [ ] MVP-релиз v1.0.0

