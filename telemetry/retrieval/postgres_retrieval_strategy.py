import os
from typing import Optional
from sqlalchemy import create_engine, func, text
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
        self.Driver = Base.classes.telemetry_driver

    def retrieve_data(self, query):
        with self.db_session() as session:
            result = session.execute(text(query)).fetchall()
        return result

    def games(self):
        with self.db_session() as session:
            return session.query(self.Game).all()

    def drivers(self):
        with self.db_session() as session:
            return session.query(self.Driver).all()

    def sessions(self, limit: Optional[int] = 10, group_by=None):
        with self.db_session() as session:
            if not group_by:
                return session.query(self.Session).limit(limit).all()

            query = session.query(func.count(self.Session.id).label('count'))

            if group_by == 'game':
                query = query.add_columns(self.Game.name)
                query = query.join(self.Game, self.Session.game_id == self.Game.id)
                group_column = self.Game.name
            elif group_by == 'driver':
                query = query.add_columns(self.Driver.name)
                query = query.join(self.Driver, self.Session.driver_id == self.Driver.id)
                group_column = self.Driver.name
            else:
                group_column = getattr(self.Session, group_by)
                query = query.add_columns(group_column)

            return query.group_by(group_column).limit(limit).all()
