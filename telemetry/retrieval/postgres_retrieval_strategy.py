import os
import psycopg2
from .retrieval_strategy import RetrievalStrategy

class PostgresRetrievalStrategy(RetrievalStrategy):
    def __init__(self):
        dbname = os.getenv('DB_NAME', 'postgres')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'postgres')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')

        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def retrieve_data(self, filters):
        cursor = self.connection.cursor()
        query = "SELECT * FROM telemetry_game"  # Example query
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
