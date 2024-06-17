.PHONY: test

test:
	PYTHONPATH=. pipenv run pytest -rP

graphql-schema:
	pipenv run gql-cli http://telemetry.b4mad.racing:30050/graphql --print-schema --schema-download  > telemetry/retrieval/schema.graphql

