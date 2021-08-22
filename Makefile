include .env

tail := 200
PYTHONPATH := $(shell pwd):${PYTHONPATH}

PROJECT := aiogram_bot
LOCALES_DOMAIN := bot
LOCALES_DIR := locales
VERSION := 0.1
PIPENV_VERBOSITY := -1

# =================================================================================================
# Base
# =================================================================================================

default:help

help:
	@echo "aiogram bot"

# =================================================================================================
# Development
# =================================================================================================

isort:
	poetry run isort aiogram_bot

black:
	poetry run black aiogram_bot

flake8:
	poetry run flake8 aiogram_bot

lint: isort black flake8

entrypoint:
	pipenv run bash ../docker-entrypoint.sh ${args}

texts-update:
	poetry run pybabel extract . \
    	-o ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot \
    	--project=${PROJECT} \
    	--version=${VERSION} \
    	--copyright-holder=Illemius \
    	-k __:1,2 \
    	--sort-by-file -w 99
	poetry run pybabel update \
		-d ${LOCALES_DIR} \
		-D ${LOCALES_DOMAIN} \
		--update-header-comment \
		-i ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot

texts-compile:
	poetry run pybabel compile -d locales -D bot

texts-create-language:
	poetry run pybabel init -i locales/bot.pot -d locales -D bot -l ${language}

alembic:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} poetry run alembic ${args}

migrate:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} poetry run alembic upgrade head

migration:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} poetry run alembic revision --autogenerate -m "${message}"

downgrade:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} poetry run alembic downgrade -1

beforeStart: docker-up-db migrate texts-compile

app:
	pipenv run python -m aiogram_bot ${args}

start:
	$(MAKE) beforeStart
	$(MAKE) aiogram_bot args="run-polling"

# =================================================================================================
# Docker
# =================================================================================================

docker-config:
	docker-compose config

docker-ps:
	docker-compose ps

docker-build:
	docker-compose build

docker-up-db:
	docker-compose up -d redis postgres

docker-up:
	docker-compose up -d --remove-orphans

docker-stop:
	docker-compose stop

docker-down:
	docker-compose down

docker-destroy:
	docker-compose down -v --remove-orphans

docker-logs:
	docker-compose logs -f --tail=${tail} ${args}

# =================================================================================================
# Application in Docker
# =================================================================================================

app-create: docker-build docker-stop docker-up

app-logs:
	$(MAKE) docker-logs args="bot"

app-stop: docker-stop

app-down: docker-down

app-start: docker-stop docker-up

app-destroy: docker-destroy
