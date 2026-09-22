.PHONY: test lint clean install

install:
	pip install -e .[dev]

test:
	pytest -v

lint:
	flake8 etl_wore tests

clean:
	rm -rf build dist *.egg-info .pytest_cache outputs temp
