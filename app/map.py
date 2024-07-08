from telemetry.plot.plots import plot_2d_map
from dash import Patch
import math

def create_map_view(df, shared_range, slider_value = None):
    map_fig = plot_2d_map([df])

    if shared_range:
        min_distance, max_distance = shared_range
    else:
        min_distance = df['DistanceRoundTrack'].min()
        max_distance = df['DistanceRoundTrack'].max()

    filtered_df = df[(df['DistanceRoundTrack'] >= min_distance) & (df['DistanceRoundTrack'] <= max_distance)]
    min_x = filtered_df['WorldPosition_x'].min()
    max_x = filtered_df['WorldPosition_x'].max()
    min_y = filtered_df['WorldPosition_y'].min()
    max_y = filtered_df['WorldPosition_y'].max()
    margin = 50  # Add a margin around the visible area
    map_fig.update_layout(
        xaxis=dict(range=[min_x - margin, max_x + margin]),
        yaxis=dict(range=[min_y - margin, max_y + margin]),
        title=None,
        showlegend=False,
        xaxis_visible=False,
        yaxis_visible=False,
    )
    return map_fig

def patch_circle_and_arrow(df, slider_value):
    patched_figure = Patch()

    # Find the closest point to the slider value
    closest_point = df.iloc[(df['DistanceRoundTrack'] - slider_value).abs().argsort()[:1]]
    x = closest_point['WorldPosition_x'].values[0]
    y = closest_point['WorldPosition_y'].values[0]
    yaw = closest_point['Yaw'].values[0]

    # Draw circle
    circle_size = 20
    patched_figure["layout"]["shapes"] = [
        {
            "type": "circle",
            "xref": "x", "yref": "y",
            "x0": x - circle_size, "y0": y - circle_size,
            "x1": x + circle_size, "y1": y + circle_size,
            "line": {"color": "red"}
        }
    ]

    # Draw arrow
    arrow_length = 100
    arrow_x = x + math.cos(math.radians(yaw + 90)) * arrow_length
    arrow_y = y + math.sin(math.radians(yaw + 90)) * arrow_length
    patched_figure["layout"]["shapes"].append({
        "type": "line",
        "x0": x, "y0": y,
        "x1": arrow_x, "y1": arrow_y,
        "line": {"color": "green"}
    })

    return patched_figure
