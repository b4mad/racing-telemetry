import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
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
        html.Div([
            dcc.Graph(id='map-view', style={'height': '100%'})
        ], style={'width': '50%', 'height': '100%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='speed-view', style={'height': '50%'}),
            dcc.Graph(id='throttle-view', style={'height': '50%'})
        ], style={'width': '50%', 'height': '100%', 'display': 'inline-block', 'flexDirection': 'column'})
    ], style={'display': 'flex', 'height': '100vh'}),
    dcc.Store(id='shared-range')
], style={'height': '100vh', 'width': '100vw'})

# Add CSS to ensure full height and width
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to update the map view
@app.callback(
    Output('map-view', 'figure'),
    [Input('map-view', 'id')]
)
def update_map_view(_):
    fig = plot_2d_map([df])
    return fig

# Callback to update the speed and throttle views
@app.callback(
    [Output('speed-view', 'figure'),
     Output('throttle-view', 'figure'),
     Output('shared-range', 'data')],
    [Input('speed-view', 'relayoutData'),
     Input('throttle-view', 'relayoutData')],
    [State('shared-range', 'data')]
)
def update_views(speed_relayout, throttle_relayout, shared_range):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'speed-view':
        relayout_data = speed_relayout
    elif trigger_id == 'throttle-view':
        relayout_data = throttle_relayout
    else:
        relayout_data = None

    if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
        shared_range = [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']]
    
    speed_fig = lap_fig(df, columns=["SpeedMs"], title="SpeedMs")
    throttle_fig = lap_fig(df, columns=["Throttle"], title="Throttle")

    if shared_range:
        speed_fig.update_xaxes(range=shared_range)
        throttle_fig.update_xaxes(range=shared_range)

    return speed_fig, throttle_fig, shared_range

if __name__ == '__main__':
    app.run_server(debug=True)



