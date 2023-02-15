PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
	poetry run flask --app page_analyzer:app --debug run

lint:
	poetry run flake8 page_analyzer

test:
	poetry run python3 -m pytest -ra -s -vvv tests/

cov:
	poetry run python3 -m pytest --cov

install:
	poetry install

show-dev-deamons:
	ps aux | grep 'make dev'