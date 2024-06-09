.PHONY: test

test:
	PYTHONPATH=. pipenv run pytest -rP