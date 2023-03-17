PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
	poetry run flask --app page_analyzer:app --debug run

lint:
	poetry run flake8 page_analyzer

test:
	env PROJECT_ENV="local_test" poetry run python3 -m pytest -ra -s -vvv tests/

cov:
	poetry run python3 -m pytest --cov=page_analyzer/ tests/

install:
	poetry install

show-dev-deamons:
	ps aux | grep 'make dev'
