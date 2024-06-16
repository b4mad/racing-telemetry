.PHONY: test

test:
	PYTHONPATH=. pipenv run pytest -rP

graphql-schema:
	pipenv run gql-cli https://rickandmortyapi.com/graphql --print-schema --schema-download  > telemetry/retrieval/schema.graphql

