include .env

.ONESHELL:

shell:
	pipenv shell

setup:
	pipenv sync

lint:
	pipenv run lint

entrypoint:
	cd src
	pipenv run bash ../docker-entrypoint.sh ${ARGS}

texts-update:
	pipenv run texts_update

alembic:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic ${args}

migrate:
	cd src
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pipenv run alembic upgrade head

texts-compile:
	pipenv run texts_compile

docker-config:
	docker-compose config

docker-ps:
	docker-compose ps

docker-destroy:
	docker-compose down -v --remove-orphans

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-up-db:
	docker-compose up -d redis postgres
