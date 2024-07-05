import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from telemetry import Telemetry
from telemetry.utility.utilities import get_or_create_df
from telemetry.plot.plots import plot_2d_map, lap_fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize Telemetry
telemetry = Telemetry()
telemetry.set_pandas_adapter()
session_id = 1719933663
driver = "durandom"
telemetry.set_filter({'session_id': session_id, 'driver': 'durandom'})

# Use get_or_create_df to retrieve the DataFrame
df = get_or_create_df(lambda: telemetry.get_telemetry_df(), name=session_id)

# Layout of the app
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='map-view')
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='telemetry-view')
    ], style={'width': '50%', 'display': 'inline-block'})
])

# Callback to update the map view
@app.callback(
    Output('map-view', 'figure'),
    [Input('map-view', 'id')]
)
def update_map_view(_):
    fig = plot_2d_map([df])
    return fig

# Callback to update the telemetry data view
@app.callback(
    Output('telemetry-view', 'figure'),
    [Input('telemetry-view', 'id')]
)
def update_telemetry_view(_):
    fig = lap_fig(df, columns=["SpeedMs"])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



