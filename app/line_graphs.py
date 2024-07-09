from racing_telemetry.plot.plots import lap_fig
from dash import Patch

def create_line_graph(df, shared_range, column, title):
    fig = lap_fig(df, columns=[column], full_range=True, show_legend=False, title=title)
    if shared_range:
        fig.update_xaxes(range=shared_range)
    return fig

def add_vertical_line(fig, slider_value):
    patched_figure = Patch()
    patched_figure["layout"]["shapes"] = [
        {
            "type": "line",
            "x0": slider_value,
            "x1": slider_value,
            "y0": 0,
            "y1": 1,
            "xref": "x",
            "yref": "paper",
            "line": {"width": 2, "dash": "dash", "color": "red"}
        }
    ]
    return patched_figure
