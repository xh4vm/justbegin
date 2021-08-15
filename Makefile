.PHONY: run
run:
	docker-compose up -d --build

.PHONY: test
test:
	docker exec -it justbegin_web_1 pytest -vv --cov=app/

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
