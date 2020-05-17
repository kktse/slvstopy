init:
	pip install -r requirements.txt

lint:
	flake8 src tests
	mypy src/slvstopy

format:
	black .
	flake8 src tests
	mypy src/slvstopy