.PHONY: test build upload clean

test:
	PYTHONPATH=. pipenv run pytest -vrP

graphql-schema:
	pipenv run gql-cli http://telemetry.b4mad.racing:30050/graphql --print-schema --schema-download  > telemetry/retrieval/schema.graphql

build:
	pipenv run python setup.py sdist bdist_wheel

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

