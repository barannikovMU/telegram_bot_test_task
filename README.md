## Test task "Telegram bot for notifications of changes in exchange rate quotes"

## Problem statement:

It is necessary to develop a bot that has the following functions:

1. Выводить курсы валют на которые подписан пользователь
2. Возможность подписываться и отписываться от курса валюты
3. Добавлять уведомление о достижении заданного значения курса валюты
4. Присылать пользователю пуш-уведомление при достижении заданного значения
5. Удалять выставленные уведомления

## Команды бота:

- `/start` — greeting message
- `/help` — reference
- `/current` — show the current exchange rate
- `/subscribe` — subscribe to the exchange rate
- `/unsubscribe` — unsubscribe from the exchange rate
- `/list_notification` — display a list of notifications
- `/add_notification` — add a notification
- `/remove_notification` — remove notification
- `/remove_all_notification` — remove all notification
- `/cancel` — cancel current action

## Quick Start

1. Copy the settings file and change them

```
cp example.env .env
```

2. Use docker compose to build an image

```
docker-compose build
```

3. Run docker compose up to start the application

```
docker-compose up
```

## Access to postgres:

* **Address:** `127.0.0.1:6432`
* **Username:** postgres_user (as a default)
* **Password:** 1234 (as a default)

## Access to PgAdmin:

* **URL:** `http://localhost:5050`
* **Username:** admin@admin.com (as a default)
* **Password:** admin (as a default)

## Add a new server in PgAdmin:

* **Host name/address** `postgres`
* **Port** `5432`
* **Username** as `POSTGRES_USER`, by default: `postgres_user`
* **Password** as `POSTGRES_PASSWORD`, by default `1234`

## Logging

There are no easy way to configure pgadmin log verbosity and it can be overwhelming at times. It is possible to disable pgadmin logging on the container level.

Add the following to `pgadmin` service in the `docker-compose.yml`:

```
logging:
  driver: "none"
```

## Migrations

* Initialization of alembic: `alembic init -t async bot/migrations`
* Create a new migration: `alembic revision --autogenerate -m "migration name"`
* Get information about the current migration: `alembic current`
* Apply migration: `alembic upgrade head`
* Roll back migration: `alembic downgrade -1`
* Roll back migrations to the very beginning: `alembic downgrade base`
