.PHONY: check fmt test

fmt:
	ruff format .
	ruff check --fix .

check:
	ruff format .
	ruff check --fix .
	pytest -q

test:
	pytest -q