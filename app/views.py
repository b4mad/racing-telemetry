
from telemetry.plot.plots import plot_2d_map, lap_fig
import math

def update_slider(df, shared_range, current_value):
    slider_min = df['DistanceRoundTrack'].min()
    slider_max = df['DistanceRoundTrack'].max()
    new_slider_value = current_value

    if shared_range:
        slider_min = max(slider_min, shared_range[0])
        slider_max = min(slider_max, shared_range[1])
        new_slider_value = max(slider_min, min(current_value, slider_max))

    return slider_min, slider_max, new_slider_value

def update_line_graphs(df, shared_range, slider_value):
    figures = []
    for column, title in [
        (["SpeedMs"], "Speed (m/s)"),
        (["Throttle"], "Throttle"),
        (["Brake"], "Brake"),
        (["Gear"], "Gear"),
        (["SteeringAngle"], "Steering Angle"),
        (["CurrentLapTime"], "Lap Time")
    ]:
        fig = lap_fig(df, columns=column, title=title, show_legend=False)
        if shared_range:
            fig.update_xaxes(range=shared_range)
        if slider_value is not None:
            fig.add_vline(x=slider_value, line_width=2, line_dash="dash", line_color="red")
        figures.append(fig)
    return figures

def update_map_view(df, shared_range, slider_value):
    map_fig = plot_2d_map([df])

    if shared_range:
        min_distance, max_distance = shared_range
    elif slider_value is not None:
        min_distance = df['DistanceRoundTrack'].min()
        max_distance = slider_value
    else:
        return map_fig

    filtered_df = df[(df['DistanceRoundTrack'] >= min_distance) & (df['DistanceRoundTrack'] <= max_distance)]
    min_x = filtered_df['WorldPosition_x'].min()
    max_x = filtered_df['WorldPosition_x'].max()
    min_y = filtered_df['WorldPosition_y'].min()
    max_y = filtered_df['WorldPosition_y'].max()
    margin = 50  # Add a margin around the visible area
    map_fig.update_layout(
        xaxis=dict(range=[min_x - margin, max_x + margin]),
        yaxis=dict(range=[min_y - margin, max_y + margin])
    )

    if slider_value is not None:
        # Find the closest point to the slider value
        closest_point = df.iloc[(df['DistanceRoundTrack'] - slider_value).abs().argsort()[:1]]
        x = closest_point['WorldPosition_x'].values[0]
        y = closest_point['WorldPosition_y'].values[0]
        yaw = closest_point['Yaw'].values[0]

        # Draw circle
        circle_size = 20
        map_fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=x - circle_size, y0=y - circle_size,
            x1=x + circle_size, y1=y + circle_size,
            line_color="red"
        )

        # Draw arrow
        arrow_length = 100
        arrow_x = x + math.cos(math.radians(yaw)) * arrow_length
        arrow_y = y + math.sin(math.radians(yaw)) * arrow_length
        map_fig.add_annotation(
            x=x, y=y,
            ax=arrow_x, ay=arrow_y,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor="green"
        )

    return map_fig
