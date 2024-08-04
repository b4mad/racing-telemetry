We're dealing with car telemetry data from a racing game.
The pandas data frame has the following columns:

```python
print(df.columns)
Index(['result', 'table', '_start', '_stop', '_time', 'CarModel', 'CurrentLap',
       'GameName', 'SessionId', 'SessionTypeName', 'TrackCode', '_measurement',
       'host', 'topic', 'user', 'Brake', 'Clutch', 'CurrentLapIsValid',
       'CurrentLapTime', 'DistanceRoundTrack', 'Gear', 'Handbrake',
       'LapTimePrevious', 'Pitch', 'PreviousLapWasValid', 'Roll', 'Rpms',
       'SpeedMs', 'SteeringAngle', 'Throttle', 'TyreType', 'WorldPosition_x',
       'WorldPosition_y', 'WorldPosition_z', 'Yaw', 'id'],
      dtype='object')
```