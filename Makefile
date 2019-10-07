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

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d
