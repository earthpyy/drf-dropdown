build:
	poetry build

setup:
	pip3 install poetry poetry-dynamic-versioning || pip install poetry poetry-dynamic-versioning
	poetry install
	poetry run pre-commit install
