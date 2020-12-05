PATHS = src tests

init:
	pip install -r requirements/requirements.txt
	pip install -r requirements/requirements-dev.txt
	pip install -e .

lint:
	flake8 ${PATHS}
	mypy ${PATHS}

format:
	black ${PATHS}
	flake8 ${PATHS}
	mypy ${PATHS}

test:
	pytest -vv

test-coverage:
	pytest --cov-report term --cov=src
