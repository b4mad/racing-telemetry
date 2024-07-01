#!/usr/bin/env python
from init import *
import ipywidgets as widgets
from IPython.display import display

t = Telemetry()
t.set_pandas_adapter()

df = t.drivers()

print(df.head())

#     result  table                           _start                            _stop                            _time               CarModel CurrentLap  ...  Throttle    TyreType WorldPosition_x WorldPosition_y WorldPosition_z       Yaw            id
# 0  _result      0 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:30.457458+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 1  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.640037+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 2  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.744887+00:00  Citroen Xsara Kit Car          0  ...  0.000000  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 3  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.857103+00:00  Citroen Xsara Kit Car          0  ...  0.007843  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0
# 4  _result      1 2023-07-02 16:19:40.153722+00:00 2024-07-01 16:19:40.153722+00:00 2024-07-01 15:30:35.966476+00:00  Citroen Xsara Kit Car          0  ...  0.168627  Dry Gravel     -231.150589        83.04983      -27.045351 -64.44776  1719840630-0

