include .env

.ONESHELL:
.DEFAULT_GOAL := default

tail := 200

# =================================================================================================
# Base
# =================================================================================================

default:help

help:
	@echo "aiogram bot"

# =================================================================================================
# Development
# =================================================================================================

shell:
	pipenv shell

setup:
	pipenv sync

lint:
	pipenv run lint

entrypoint:
	cd src
	pipenv run bash ../docker-entrypoint.sh ${args}

texts-update:
	pipenv run texts_update

texts-compile:
	pipenv run texts_compile

alembic:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic ${args}

migrate:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic upgrade head

migration:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic revision --autogenerate -m "${message}"

downgrade:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic downgrade -1

# =================================================================================================
# Docker
# =================================================================================================

docker-config:
	docker-compose config

docker-build:
	docker-compose build

docker-up-db:
	docker-compose up -d redis postgres

docker-up:
	docker-compose up -d

docker-ps:
	docker-compose ps

docker-down:
	docker-compose down

docker-destroy:
	docker-compose down -v --remove-orphans

docker-app-migrate:
	docker-compose exec bot alembic upgrade head

# =================================================================================================
# Application in Docker
# =================================================================================================

app-create: docker-build docker-down docker-up docker-app-migrate

app-logs:
	docker-compose logs -f --tail=${tail} ${args}

app-stop: docker-down

app-start: docker-down docker-up
