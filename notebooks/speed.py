#!/usr/bin/env python
from init import *
from telemetry.analysis import *

t = Telemetry()
t.set_pandas_adapter()
session_id = 1719933663
driver = "durandom"
t.set_filter({'session_id': session_id, 'driver': 'durandom'})

# fig = plot_sessions([session_id], landmarks=True, columns=["SpeedMs"])
# fig.show()

lap = get_or_create_df(lambda: t.get_telemetry_df(), name=session_id)

avg_speed = average_speed(lap)
print(f"Average speed for session {session_id}: {avg_speed:.2f} m/s")
# Average speed for session 1719933663: 32.75 m/s

print("\nStreaming average speed calculation and adding features to dataframe:")
streaming = Streaming()
for index, row in lap.iterrows():
    streaming.notify(row.to_dict())
    features = streaming.get_features()
    for feature, value in features.items():
        lap.at[index, feature] = value[-1] if isinstance(value, list) else value

print("\nFinal dataframe with added features:")
print(lap[['SpeedMs', 'average_speed', 'coasting_time']].tail())

print("\nFinal computed features:")
print(streaming.get_features())

# Create the lap figure
# fig = lap_fig(lap, columns=["SpeedMs", "Throttle", "Brake", "average_speed", "coasting_time"])
fig = lap_fig(lap, columns=["Throttle", "Brake", "coasting_time", "CurrentLapTime"])

# Show the figure
fig.show()
