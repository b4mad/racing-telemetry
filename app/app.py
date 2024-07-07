import logging
import json
import dash
from dash import dcc, html
from flask import request, Response
from werkzeug.wsgi import get_current_url
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from telemetry import Telemetry
from telemetry.utility.utilities import get_or_create_df
from telemetry.plot.plots import plot_2d_map, lap_fig

from views import *

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
            dcc.Slider(
                id='distance-slider',
                min=df['DistanceRoundTrack'].min(),
                max=df['DistanceRoundTrack'].max(),
                step=1,
                value=df['DistanceRoundTrack'].min(),
                marks={i: str(i) for i in range(int(df['DistanceRoundTrack'].min()), int(df['DistanceRoundTrack'].max()), 1000)},
                updatemode='drag'
            ),
            dcc.Graph(id='speed-view'),
            dcc.Graph(id='throttle-view'),
            dcc.Graph(id='brake-view'),
            dcc.Graph(id='gear-view'),
            dcc.Graph(id='steer-view'),
            dcc.Graph(id='time-view')
        ], style={'width': '50%', 'height': '100%', 'display': 'inline-block', 'flexDirection': 'column', 'margin-right': '20px'})
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



# Callback to update all views
@app.callback(
    [Output('map-view', 'figure'),
     Output('speed-view', 'figure'),
     Output('throttle-view', 'figure'),
     Output('brake-view', 'figure'),
     Output('gear-view', 'figure'),
     Output('steer-view', 'figure'),
     Output('time-view', 'figure'),
     Output('shared-range', 'data'),
     Output('distance-slider', 'min'),
     Output('distance-slider', 'max'),
     Output('distance-slider', 'value')],
    [Input('map-view', 'relayoutData'),
     Input('speed-view', 'relayoutData'),
     Input('throttle-view', 'relayoutData'),
     Input('brake-view', 'relayoutData'),
     Input('gear-view', 'relayoutData'),
     Input('steer-view', 'relayoutData'),
     Input('time-view', 'relayoutData')],
    [State('shared-range', 'data')],
    prevent_initial_call=True
)
def update_views(map_relayout, speed_relayout, throttle_relayout, brake_relayout, gear_relayout,
                 steer_relayout, time_relayout, shared_range):
    global df
    logger.debug(f"update_views: shared_range: {shared_range}")
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    relayout_data = None
    for view, data in zip(['map-view', 'speed-view', 'throttle-view', 'brake-view', 'gear-view', 'steer-view', 'time-view'],
                          [map_relayout, speed_relayout, throttle_relayout, brake_relayout, gear_relayout, steer_relayout, time_relayout]):
        if trigger_id == view:
            relayout_data = data
            break

    if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
        shared_range = [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']]

    map_fig = update_map_view(df, shared_range)
    lap_figures = update_line_graphs(df, shared_range)

    slider_value = shared_range[0] if shared_range else df['DistanceRoundTrack'].min()
    slider_min, slider_max, new_slider_value = update_slider(df, shared_range, slider_value)

    return map_fig, *lap_figures, shared_range, slider_min, slider_max, new_slider_value

# Callback to update all views
@app.callback(
    [Output('map-view', 'figure', allow_duplicate=True),
     Output('speed-view', 'figure', allow_duplicate=True),
     Output('throttle-view', 'figure', allow_duplicate=True),
     Output('brake-view', 'figure', allow_duplicate=True),
     Output('gear-view', 'figure', allow_duplicate=True),
     Output('steer-view', 'figure', allow_duplicate=True),
     Output('time-view', 'figure', allow_duplicate=True)],
    [Input('distance-slider', 'value')],
    [State('shared-range', 'data')],
    prevent_initial_call=True
)
def update_slider_view(slider_value, shared_range):
    logger.info(f"update_slider: Slider value: {slider_value}, shared_range: {shared_range}")
    global df
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    map_fig = update_map_view(df, shared_range, slider_value)
    lap_figures = update_line_graphs(df, shared_range, slider_value)
    # slider_min, slider_max, new_slider_value = update_slider(df, shared_range, slider_value)

    # return map_fig, *lap_figures, shared_range, slider_min, slider_max, new_slider_value
    return map_fig, *lap_figures

if __name__ == '__main__':
    # set log level
    logging.basicConfig(level=logging.DEBUG)

    @app.server.before_request
    def log_request_info():
        url = get_current_url(request.environ)
        if url.endswith("_reload-hash"):
            return
        # logger.debug('REQ--------------------------------')
        logger.debug(f'URL: {url}')
        # logger.debug(f'Method: {request.method}')
        # logger.debug(f'Headers: {dict(request.headers)}')
        # logger.debug(f'Body: {request.get_data(as_text=True)}')
        # log the size of the request
        logger.debug(f'Request size: {request.content_length} bytes')
        pass

    @app.server.after_request
    def log_response_info(response):
        url = get_current_url(request.environ)
        if url.endswith("_reload-hash"):
            return response
        # logger.debug('RES--------------------------------')
        # logger.debug(f'Status: {response.status}')
        # logger.debug(f'Headers: {dict(response.headers)}')
        # logger.debug(f'Body: {response.get_data(as_text=True)}')
        # log the size of the response
        logger.debug(f'Response size: {len(response.get_data(as_text=True))} bytes')
        return response

    app.run_server(debug=True)



