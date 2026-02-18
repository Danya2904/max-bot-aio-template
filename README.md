# ⚡️ MAX Bot AIO Template (Production Ready)

**Готовый асинхронный шаблон для разработки ботов под MAX Messenger API.**
Построен на базе `aiogram-like` архитектуры: Handlers, Middlewares, FSM (Redis), SQLAlchemy (Async).

> **Cообщество разработчиков:**
> У вас вопросы по API? Присоединяйтесь к чату **[MAX API Devs | Разработка ботов](https://max.ru/join/xuOCxEvbn0nKepqaooBlHt35UZyvtwWwJoJLdeMzhy4)**.

## Почему этот шаблон?

Разработка под MAX API часто приводит к вложенным JSON, отсутствию нормальной документации, отсутствие готовых FSM.
Этот шаблон решает главные проблемы:

**Нормализация данных:** Встроенный слой превращает кривые JSON от MAX в удобные объекты `NormalizedMessage`.
**FSM (Машина состояний):** Готовая реализация на Redis (с fallback в память) для диалогов.
**Clean Architecture:** Четкое разделение: Хендлеры → Сервисы → БД.
**Docker-First:** Разворачивается одной командой `docker-compose up`.
**Типизация:** Полностью на Python 3.10+ с Type Hints и Pydantic.

## Стек

**Python 3.10+**
**Aiohttp** (Асинхронные запросы)
**SQLAlchemy 2.0 + Asyncpg** (База данных)
**Redis** (Кэш и Состояния)
**Pydantic Settings** (Конфигурация)

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ВАШ_ЮЗЕРНЕЙМ/max-bot-aio-template.git](https://github.com/ВАШ_ЮЗЕРНЕЙМ/max-bot-aio-template.git)
   cd max-bot-aio-template