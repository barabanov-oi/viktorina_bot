# Viktorina Bot (Flask + aiogram + MySQL)

Продакшн-ориентированный каркас Telegram-бота викторин с clean architecture:
- transport слой (`aiogram`, `Flask`) не работает напрямую с ORM;
- бизнес-логика в сервисах;
- доступ к БД через репозитории + `UnitOfWork`;
- MySQL 8+ как единственная БД;
- event ledger (`game_events`), prompt-логирование LLM (`prompt_logs`), кэш лидербордов (`leaderboards_cache`), jobs-воркер на MySQL.

## Стек
- Python 3.12
- Flask 3.x + Gunicorn
- aiogram 3.x
- MySQL 8+
- SQLAlchemy 2.x + Alembic
- PyMySQL
- Pydantic
- Pytest
- Docker Compose

## Быстрый старт
1. Скопируйте env:
```bash
cp .env.example .env
```
2. Поднимите инфраструктуру:
```bash
docker compose up -d --build
```
3. Примените миграции:
```bash
docker compose run --rm web alembic upgrade head
```
4. Заполните тестовые данные:
```bash
docker compose run --rm web python scripts/seed.py
```

## Сервисы
- `web` — Flask Admin API и `/health` на `:8000`
- `bot` — aiogram polling
- `worker` — MySQL jobs queue worker (`jobs` таблица)
- `mysql` — MySQL 8.4

## Команды бота
`/start`, `/help`, `/quiz`, `/topics`, `/groupquiz`, `/join`, `/duel @user`, `/duel_random`, `/rank`, `/top`, `/report`, `/admin_help`.

## Admin API
Требует заголовок `X-Admin-Token`.
- `GET /health`
- `GET /admin/prompt-logs?limit=50`
- `POST /admin/ban-user` `{ "tg_user_id": 123 }`
- `POST /admin/question/deactivate` `{ "question_id": 1 }`
- `POST /admin/moderation/resolve` `{ "flag_id": 1, "resolution": "resolved" }`

## Идемпотентность
Для каждого update Telegram используется уникальный ключ `telegram_update:{update_id}` и пишется событие в `game_events`.
`idempotency_key` имеет unique constraint — дубли игнорируются.

## Rate limit без Redis
Реализован in-memory rate limiter (`InMemoryRateLimiter`) с TTL и LRU-очисткой.
Ограничение: защита действует только в рамках одного процесса/контейнера.
Для кросс-процессного лимита добавлена таблица `rate_limits` (скелет).

## LLM режим
- Если `LLM_DISABLED=true` или не задан `LLM_API_KEY`, бот работает только на question bank.
- Строгий парсинг JSON ответа LLM + валидация DTO.
- Каждый LLM вызов логируется в `prompt_logs` с prompt/params/raw/parsed/status/latency.

## Тесты
```bash
pytest -q
```

## Важные директории
- `app/services` — scoring, anti-cheat, question service, leaderboard, moderation
- `app/persistence` — модели, репозитории, UoW
- `app/transport/telegram` — bot handlers/middleware
- `app/transport/web` — Flask API
- `app/workers` — MySQL jobs worker
- `migrations` — Alembic
