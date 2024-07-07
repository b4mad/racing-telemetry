from telemetry.plot.plots import plot_2d_map, lap_fig
from dash import Patch

def update_slider(df, shared_range, current_value):
    slider_min = df['DistanceRoundTrack'].min()
    slider_max = df['DistanceRoundTrack'].max()
    new_slider_value = current_value

    if shared_range:
        slider_min = max(slider_min, shared_range[0])
        slider_max = min(slider_max, shared_range[1])
        new_slider_value = max(slider_min, min(current_value, slider_max))

    return slider_min, slider_max, new_slider_value


