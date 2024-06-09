import unittest
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class TestGraphQLRetrievalStrategy(unittest.TestCase):
    def test_retrieve_data_with_empty_filter(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://example.com/graphql")
        try:
            strategy.retrieve_data(filters={})
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"retrieve_data raised an exception with empty filters: {e}")

    def test_retrieve_data_with_game_filter(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://telemetry.b4mad.racing:30050/graphql")
        filters = ['game']
        result = strategy.retrieve_data(filters=filters)
        self.assertIsInstance(result, list)
        if result:
            self.assertIsInstance(result[0], dict)
    unittest.main()
