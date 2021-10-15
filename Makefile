build:
	poetry build

setup:
	pip3 install poetry || pip install poetry
	poetry install
	poetry run pre-commit install

test:
	DJANGO_SETTINGS_MODULE=tests.settings poetry run pytest
