.PHONY: clean init

init: clean
	pipenv install --dev
	pipenv run pre-commit install

service_up:
	docker-compose run -d database && docker-compose run -d redis

service_down:
	docker-compose down && docker volume rm database_data

reformat: black isort

black:
	pipenv run black api/endpoints/
	pipenv run black api/tests/

isort:
	pipenv run isort api/*.py
	pipenv run isort api/endpoints/**/*.py

analysis: bandit

bandit:
	pipenv run bandit api/

lint: pylint flake8

flake8:
	pipenv run flake8 api/ --max-line-length=120 --exclude=test,database

pylint:
	pipenv run pylint --rcfile=setup.cfg api/

test:
	pipenv run pytest -vv --cov-report=term-missing --cov=api/endpoints api/tests

ci-bundle: reformat analysis lint test

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f report.xml
	rm -f coverage.xml
