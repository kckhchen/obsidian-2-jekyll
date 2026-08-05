.PHONY: check fmt test

fmt:
	ruff format .
	ruff check --fix .

check:
	ruff format --check .
	ruff check .
	pytest -q

test:
	pytest -q