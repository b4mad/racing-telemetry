#!/usr/bin/env python
from init import *
from telemetry.analysis import *

t = Telemetry()
t.set_pandas_adapter()
game = "Richard Burns Rally"
landmark_df = t.landmarks(game=game, kind="turn")
print(landmark_df)

# Create a histogram of landmark names
from telemetry.plot.plots import plot_histogram

histogram_fig = plot_histogram(landmark_df, 'name')
histogram_fig.show()

