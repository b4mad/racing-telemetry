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

print("\nStreaming average speed calculation:")
streaming = Streaming()
for _, row in lap.iterrows():
    streaming.notify(row.to_dict())

features = streaming.get_features()
print(features)
# streaming_avg = features['average_speed'][-1] if features['average_speed'] else None

# if streaming_avg is not None:
#     print(f"Average speed for session {session_id}: {streaming_avg:.2f} m/s")
# else:
#     print("No data available for average speed calculation.")
