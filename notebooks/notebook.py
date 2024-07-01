#!/usr/bin/env python
from init import *
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(current_dir, 'cached_df.pkl')


t = Telemetry()
t.set_pandas_adapter()
t.set_filter({'session_id': 1719840630})

lap = get_or_create_df(lambda: t.get_telemetry_df())

# print(lap.columns)
# Index(['result', 'table', '_start', '_stop', '_time', 'CarModel', 'CurrentLap',
#        'GameName', 'SessionId', 'SessionTypeName', 'TrackCode', '_measurement',
#        'host', 'topic', 'user', 'Brake', 'Clutch', 'CurrentLapIsValid',
#        'CurrentLapTime', 'DistanceRoundTrack', 'Gear', 'Handbrake',
#        'LapTimePrevious', 'Pitch', 'PreviousLapWasValid', 'Roll', 'Rpms',
#        'SpeedMs', 'SteeringAngle', 'Throttle', 'TyreType', 'WorldPosition_x',
#        'WorldPosition_y', 'WorldPosition_z', 'Yaw', 'id'],
#       dtype='object')

#     result  table                           _start                            _stop                            _time               CarModel CurrentLap  ...  Throttle    TyreType WorldPosition_x WorldPosition_y WorldPosition_z       Yaw            id
# 0  _result      0 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:30.457458+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 1  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.640037+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 2  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.744887+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 3  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.857103+00:00  Citroen Xsara Kit Car          0  ...  0.007843  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 4  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.966476+00:00  Citroen Xsara Kit Car          0  ...  0.168627  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0

track = lap["TrackCode"].iloc[0]

# get all sessions with the same track
sessions = t.sessions(track=track)
# print(sessions)
#        id  session_id                            start                              end  ...  game_id  session_type_id                          created                         modified
# 0  217034  1699005080 2023-11-03 10:51:20.663487+00:00 2023-11-03 10:51:21.098663+00:00  ...        4                5 2023-11-03 10:51:21.150090+00:00 2023-11-03 10:51:21.150090+00:00
# 1  217094  1699008948 2023-11-03 11:55:49.837733+00:00 2023-11-03 13:01:19.491911+00:00  ...        4                1 2023-11-03 11:55:49.923447+00:00 2023-11-03 13:01:19.495411+00:00
# 2  217058  1699006987 2023-11-03 11:22:18.131304+00:00 2023-11-03 11:32:51.623627+00:00  ...        1                3 2023-11-03 11:22:20.214744+00:00 2023-11-03 11:32:51.635752+00:00
# 3  217035  1699005236 2023-11-03 10:53:56.204342+00:00 2023-11-03 10:53:56.423060+00:00  ...        4                5 2023-11-03 10:53:56.493476+00:00 2023-11-03 10:53:56.493476+00:00

laps = [lap]
for session_id in sessions["session_id"]:
    t.set_filter({'session_id': session_id})
    lap = get_or_create_df(lambda: t.get_telemetry_df(), name=session_id)
    laps.append(lap)

# fig = lap_fig(df)
# fig.show()

# fig = plot_3d_map(df)

# fig = plot_2d_map(df)
# fig.show()

# Fetch all tracks for Richard Burns Rally
# rbr_tracks_df = t.tracks(game="Richard Burns Rally")

# # Display the head of the DataFrame
# print(rbr_tracks_df.head())

landmarks_df = t.landmarks(game="Richard Burns Rally", track=track, kind="turn")
# print(landmarks_df)
#        id                          created                         modified         name  start   end is_overtaking_spot  kind  track_id  from_cc
# 0   28155 2024-06-07 16:42:04.441178+00:00 2024-06-07 16:42:04.441178+00:00     FLATLEFT    280  None               None  turn      3133     True
# 1   28156 2024-06-07 16:42:04.449884+00:00 2024-06-07 16:42:04.449884+00:00    FASTRIGHT    450  None               None  turn      3133     True
# 2   28157 2024-06-07 16:42:04.457963+00:00 2024-06-07 16:42:04.457963+00:00    FLATRIGHT    575  None               None  turn      3133     True
# 3   28158 2024-06-07 16:42:04.466408+00:00 2024-06-07 16:42:04.466408+00:00  HAIRPINLEFT    640  None               None  turn      3133     True
# 4   28159 2024-06-07 16:42:04.475159+00:00 2024-06-07 16:42:04.475159+00:00       KRIGHT    710  None               None  turn      3133     True

# fig = plot_2d_map(lap, landmarks_df)
# fig.show()
