import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from .retrieval_strategy import RetrievalStrategy

class PostgresRetrievalStrategy(RetrievalStrategy):
    def __init__(self):
        dbname = os.getenv('DB_NAME', 'postgres')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'postgres')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')

        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        self.db_session = sessionmaker(bind=self.engine)

        Base = automap_base()
        Base.prepare(self.engine, reflect=True)

        self.Game = Base.classes.telemetry_game
        self.Session = Base.classes.telemetry_session

    def retrieve_data(self, query):
        with self.db_session() as session:
            result = session.execute(text(query)).fetchall()
        return result

    def games(self):
        with self.db_session() as session:
            return session.query(self.Game).all()

    def sessions(self, limit=10):
        with self.db_session() as session:
            return session.query(self.Session).limit(limit).all()
