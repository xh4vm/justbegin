.PHONY: build daemon
build-daemon:
	docker-compose up -d --build

.PHONY: build
build:
	docker-compose up --build

.PHONY: run daemon
run-daemon:
	docker-compose up -d

.PHONY: run
run:
	docker-compose up

.PHONY: test
test:
	docker exec -it backend pytest -vv --cov=app/ 

.PHONY: migrate
migrate:
	docker exec -it backend flask db migrate && flask db upgrade

.PHONY: cli
cli:
	docker exec -it backend bash

.PHONY: log
log:
	docker logs backend

.PHONY: pg
pg:
	docker exec -it db psql -U test

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: clean all docker images
clean-all:
	T=$$(docker ps -q); docker stop $$T; docker rm $$T; docker container prune -f

.PHONY: clean docker images
clean:
	T="backend db elasticsearch"; docker stop $$T; docker rm $$T; docker container prune -f

.PHONY: test
test:
	docker exec -it justbegin_web_1 pytest -vv --cov=app/
