import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .retrieval_strategy import RetrievalStrategy

class PostgresRetrievalStrategy(RetrievalStrategy):
    def __init__(self):
        dbname = os.getenv('DB_NAME', 'postgres')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'postgres')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')

        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        self.Session = sessionmaker(bind=self.engine)

    def retrieve_data(self, query):
        with self.Session() as session:
            result = session.execute(text(query)).fetchall()
        return result

    def games(self):
        query = "SELECT * FROM telemetry_game"
        return self.retrieve_data(query)

    def sessions(self, limit=10):
        query = f"SELECT * FROM telemetry_session LIMIT {limit}"
        return self.retrieve_data(query)
