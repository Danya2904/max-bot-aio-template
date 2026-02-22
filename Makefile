.PHONY: up down restart logs psql help

# Переменные окружения по умолчанию
DB_USER ?= bot_user
DB_NAME ?= bot_db

help: ## Показать этот help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Поднять инфраструктуру локально (в фоне)
	docker compose up -d

down: ## Остановить и удалить контейнеры
	docker compose down

restart: down up ## Перезапустить окружение

logs: ## Посмотреть логи базы данных
	docker compose logs -f postgres

psql: ## Зайти в консоль PostgreSQL внутри контейнера
	docker compose exec postgres psql -U $(DB_USER) -d $(DB_NAME)