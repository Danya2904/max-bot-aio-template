# ⚡️ MAX Bot AIO Template (Production Ready)

**Готовый асинхронный шаблон для разработки ботов под MAX Messenger API.**
Построен на базе `aiogram-like` архитектуры: Handlers, Middlewares, FSM (Redis), SQLAlchemy (Async).

## Почему этот шаблон?

Разработка под MAX API часто приводит к вложенным JSON, отсутствию нормальной документации, отсутствие готовых FSM.
Этот шаблон решает главные проблемы:

* **Нормализация данных:** Встроенный слой превращает кривые JSON от MAX в удобные объекты `NormalizedMessage`.
* **FSM (Машина состояний):** Готовая реализация на Redis (с fallback в память) для диалогов.
* **Clean Architecture:** Четкое разделение: Хендлеры → Сервисы → БД.
* **Docker-First:** Разворачивается одной командой `docker-compose up`.
* **Типизация:** Полностью на Python 3.10+ с Type Hints и Pydantic.

## Стек

* **Python 3.10+**
* **Aiohttp** (Асинхронные запросы)
* **SQLAlchemy 2.0 + Asyncpg** (База данных)
* **Redis** (Кэш и Состояния)
* **Pydantic Settings** (Конфигурация)

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ВАШ_ЮЗЕРНЕЙМ/max-bot-aio-template.git](https://github.com/ВАШ_ЮЗЕРНЕЙМ/max-bot-aio-template.git)
   cd max-bot-aio-template
Настройте окружение:
Скопируйте .env.example в .env и вставьте токен бота:

Ini, TOML
MAX_BOT_TOKEN=ваш_токен
# Остальное можно не менять для локального запуска
Запустите через Docker:

Bash
docker-compose up --build

## Справочник API (Real World Payloads)

В папке проекта лежит файл MAX_API_Real_Payloads_2026.md - **коллекцию реальных JSON-пейлоадов** MAX API 2026.
Это поможет вам понять структуру событий `message_created`, `callback`, `user_added` и написать правильные Pydantic-модели.

💬 Поддержка и Коммьюнити
Этот проект поддерживается энтузиастами. Мы собираем базу знаний по MAX API (Payloads, паттерны, хаки).

👉 \\Вступить в MAX API Devs | Разработка ботов — обсуждение, помощь, нетворкинг.