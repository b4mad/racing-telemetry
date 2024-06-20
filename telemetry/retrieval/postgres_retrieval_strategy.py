import psycopg2
from .retrieval_strategy import RetrievalStrategy

class PostgresRetrievalStrategy(RetrievalStrategy):
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def retrieve_data(self, filters):
        cursor = self.connection.cursor()
        query = "SELECT * FROM telemetry_data"  # Example query
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
