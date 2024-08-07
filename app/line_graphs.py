from dash import Patch

from racing_telemetry.plot.plots import lap_fig


def create_line_graph(df, shared_range, column, title, segment_distances, x_axis="DistanceRoundTrack"):
    fig = lap_fig(df, columns=[column], full_range=True, show_legend=False, title=title, x_axis=x_axis)
    if shared_range:
        fig.update_xaxes(range=shared_range)

    # Add vertical green lines for segment landmarks
    for distance in segment_distances:
        fig.add_shape(
            type="line",
            x0=distance,
            x1=distance,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="green", width=2, dash="dash"),
        )

    slider_value = shared_range[0] if shared_range else df["DistanceRoundTrack"].min()
    fig.add_shape(get_slider_shape(slider_value))

    return fig


def get_slider_shape(slider_value):
    return {"type": "line", "x0": slider_value, "x1": slider_value, "y0": 0, "y1": 1, "xref": "x", "yref": "paper", "line": {"width": 2, "dash": "dash", "color": "red"}}


def add_vertical_line(fig, slider_value):
    patched_figure = Patch()
    slider_shape = get_slider_shape(slider_value)
    patched_figure["layout"]["shapes"][-1] = slider_shape
    return patched_figure
