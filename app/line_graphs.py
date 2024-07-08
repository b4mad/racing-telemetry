from telemetry.plot.plots import lap_fig
from dash import Patch

def update_line_graphs_old(df, shared_range, slider_value = None):
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

def create_line_graphs(df, shared_range):
     lap_figures = []
     for column in ["SpeedMs", "Throttle", "Brake", "Gear", "SteeringAngle", "CurrentLapTime"]:
         fig = lap_fig(df, columns=[column], full_range=True, show_legend=False, title=column)
         if shared_range:
             fig.update_xaxes(range=shared_range)
         lap_figures.append(fig)
     return lap_figures

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
            "line": {"width": 3, "dash": "dash", "color": "red"}
        }
    ]
    return patched_figure
