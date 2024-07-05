import os
import sys
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
        self.Track = Base.classes.telemetry_track
        self.Landmark = Base.classes.telemetry_landmark
        self.Lap = Base.classes.telemetry_lap
        self.Car = Base.classes.telemetry_car

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

    def sessions(self, limit: Optional[int] = 10, group_by=None, game_name=None, track_name=None, driver_name=None):
        with self.db_session() as session:
            query = session.query(self.Session)

            if game_name:
                query = query.join(self.Game).filter(self.Game.name == game_name)
            if track_name:
                query = query.join(self.Lap).join(self.Track).filter(self.Track.name == track_name)
            if driver_name:
                query = query.join(self.Driver).filter(self.Driver.name == driver_name)

            if not group_by:
                # s = query.statement
                # print(s.compile(compile_kwargs={"literal_binds": True}))
                return query.limit(limit).all()

            query = query.with_entities(func.count(self.Session.id).label('count'))

            if group_by == 'game':
                query = query.add_columns(self.Game.name)
                query = query.join(self.Game, self.Session.game_id == self.Game.id)
                group_column = self.Game.name
            elif group_by == 'driver':
                query = query.add_columns(self.Driver.name)
                query = query.join(self.Driver, self.Session.driver_id == self.Driver.id)
                group_column = self.Driver.name
            elif group_by == 'track':
                query = query.add_columns(self.Track.name)
                query = query.join(self.Lap).join(self.Track)
                group_column = self.Track.name
            else:
                group_column = getattr(self.Session, group_by)
                query = query.add_columns(group_column)

            return query.group_by(group_column).limit(limit).all()

    def tracks(self, game_name=None, track_name=None):
        with self.db_session() as session:
            query = session.query(self.Track)

            if game_name:
                query = query.join(self.Game).filter(self.Game.name == game_name)

            if track_name:
                query = query.filter(self.Track.name == track_name)

            return query.all()

    def laps(self, limit: Optional[int] = 10, session_id=None, track_name=None, driver_name=None):
        with self.db_session() as session:
            query = session.query(self.Lap)

            if session_id:
                query = query.filter(self.Lap.session_id == session_id)
            if track_name:
                query = query.join(self.Track).filter(self.Track.name == track_name)
            if driver_name:
                query = query.join(self.Session).join(self.Driver).filter(self.Driver.name == driver_name)

            query = query.order_by(self.Lap.start.desc())

            return query.limit(limit).all()

    def landmarks(self, game_name=None, track_name=None, kind=None):
        with self.db_session() as session:
            query = session.query(self.Landmark)

            if game_name or track_name:
                query = query.join(self.Track)

                if game_name:
                    query = query.join(self.Game).filter(self.Game.name == game_name)

                if track_name:
                    query = query.filter(self.Track.name == track_name)

            if kind:
                query = query.filter(self.Landmark.kind == kind)

            return query.all()

    def cars(self, game=None):
        with self.db_session() as session:
            query = session.query(self.Car)

            if game:
                query = query.join(self.Game).filter(self.Game.name == game)

            return query.all()
