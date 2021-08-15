.PHONY: run
run:
	docker-compose up -d --build

.PHONY: test
test:
	docker exec -it justbegin_web_1 pytest -vv --cov=app/

.PHONY: migrate
migrate:
	docker exec -it justbegin_web_1 flask db migrate && flask db upgrade

.PHONY: cli
cli:
	docker exec -it justbegin_web_1 bash

.PHONY: log
log:
	docker logs justbegin_web_1

.PHONY: pg
pg:
	docker exec -it db psql -U test

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
