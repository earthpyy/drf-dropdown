build:
	poetry build

setup:
	pip3 install poetry || pip install poetry
	poetry install
	poetry run pre-commit install
