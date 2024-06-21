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

    def sessions(self, limit: Optional[int] =10, group_by=None):
        with self.db_session() as session:
            if group_by:
                if group_by == 'game':
                    return session.query(
                        self.Game.name,
                        func.count(self.Session.id).label('count')
                    ).join(self.Game, self.Session.game_id == self.Game.id).group_by(self.Game.name).limit(limit).all()
                elif group_by == 'driver':
                    return session.query(
                        self.Driver.name,
                        func.count(self.Session.id).label('count')
                    ).join(self.Session, self.Driver.id == self.Session.driver_id).group_by(self.Driver.name).limit(limit).all()
                else:
                    return session.query(
                        getattr(self.Session, group_by),
                        func.count(self.Session.id).label('count')
                    ).group_by(getattr(self.Session, group_by)).limit(limit).all()
            else:
                return session.query(self.Session).limit(limit).all()
