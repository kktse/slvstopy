init:
	pip install -r requirements/requirements.txt
	pip install -r requirements/requirements-dev.txt
	pip install -e .

lint:
	flake8 src tests
	mypy src/slvstopy

format:
	black .
	flake8 src tests
	mypy src/slvstopy