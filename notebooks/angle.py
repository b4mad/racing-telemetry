#!/usr/bin/env python
from init import *
from racing_telemetry.analysis import *

t = Telemetry()
t.set_pandas_adapter()
session_id = 1719854504
session_id = 1719855408
session_id = 1719991508
driver = "durandom"
t.set_filter({'session_id': session_id, 'driver': 'durandom'})

lap = get_or_create_df(lambda: t.get_telemetry_df(), name=session_id)

streaming = Streaming(raceline_yaw=True)
for index, row in lap.iterrows():
    streaming.notify(row.to_dict())
    features = streaming.get_features()
    for feature, value in features.items():
        yaw = value
        lap.at[index, feature] = value

# print("\nFinal dataframe with added features:")
# print(lap[['SpeedMs', 'average_speed', 'coasting_time']].tail())

# print("\nFinal computed features:")
# print(streaming.get_features())

# Create the lap figure
fig = lap_fig(lap, columns=["Yaw", "raceline_yaw"])

# print every 100th row Yaw and raceline_yaw
# print(lap[['Yaw', 'raceline_yaw']].iloc[::100])

# Show the figure
fig.show()

# plot_2d_map(lap).show()