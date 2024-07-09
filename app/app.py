import logging
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import request
from werkzeug.wsgi import get_current_url
from dash.dependencies import Input, Output, State
from racing_telemetry import Telemetry
from racing_telemetry.utility.utilities import get_or_create_df

from map import *
from line_graphs import *
from slider import *

# Define the configuration for data views
DATA_VIEWS = [
    {'column': 'SpeedMs', 'title': 'Speed (m/s)'},
    {'column': 'Throttle', 'title': 'Throttle'},
    {'column': 'Yaw', 'title': 'Yaw'},
    # {'column': 'Brake', 'title': 'Brake'},
    # {'column': 'Gear', 'title': 'Gear'},
    {'column': 'SteeringAngle', 'title': 'Steer Angle'},
    # {'column': 'CurrentLapTime', 'title': 'Lap Time'}
]

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Dash app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize Telemetry
telemetry = Telemetry()
telemetry.set_pandas_adapter()
session_id = 1719933663
driver = "durandom"
telemetry.set_filter({'session_id': session_id, 'driver': 'durandom'})

# Use get_or_create_df to retrieve the DataFrame
df = get_or_create_df(lambda: telemetry.get_telemetry_df(), name=session_id)
game = df["GameName"].iloc[0]
track = df["TrackCode"].iloc[0]
landmarks = telemetry.landmarks(game=game, track=track)

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map-view', style={'height': '100vh'})
        ], width=6, className='p-0'),
        dbc.Col([
            dcc.Slider(
                id='distance-slider',
                step=1,
                value=1,
                min=0,
                max=1,
                updatemode='drag'
            ),
            html.Div([
                dcc.Graph(id=f'data-{i+1}-view', className='graph') for i in range(len(DATA_VIEWS))
            ], style={'height': 'calc(100vh - 50px)', 'overflowY': 'auto', 'width': '90%'})
        ], width=6, className='p-0')
    ], className='g-0'),
    dcc.Store(id='shared-range')
], fluid=True, style={'height': '100vh', 'width': '100vw'}, className='p-0')

# Add CSS to ensure full height and width
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
            }}
            .graph {{
                height: calc((100% / {len(DATA_VIEWS)}) - 8px);
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''



# Callback to update all views
@app.callback(
    [Output('map-view', 'figure')] +
    [Output(f'data-{i+1}-view', 'figure') for i in range(len(DATA_VIEWS))] +
    [Output('shared-range', 'data'),
     Output('distance-slider', 'min'),
     Output('distance-slider', 'max'),
     Output('distance-slider', 'marks'),
     Output('distance-slider', 'value')],
    [Input('map-view', 'relayoutData')] +
    [Input(f'data-{i+1}-view', 'relayoutData') for i in range(len(DATA_VIEWS))],
    [State('shared-range', 'data')],
    prevent_initial_call=True
)
def update_views(*args):
    global df, landmarks
    shared_range = args[-1]
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    relayout_data = None
    for i, data in enumerate(args[:-1]):
        view = f'data-{i}-view' if i > 0 else 'map-view'
        if trigger_id == view:
            relayout_data = data
            break

    logger.debug(f"update_views: trigger_id: {trigger_id}")
    logger.debug(f"update_views: shared_range: {shared_range}")
    logger.debug(f"update_views: relayout_data: {relayout_data}")

    map_zoom = None
    if relayout_data:
        if 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data and 'yaxis.range[0]' in relayout_data and 'yaxis.range[1]' in relayout_data:
            map_zoom = {
                'x': [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']],
                'y': [relayout_data['yaxis.range[0]'], relayout_data['yaxis.range[1]']]
            }
            min_distance = df[(df['WorldPosition_x'] >= map_zoom['x'][0]) & (df['WorldPosition_x'] <= map_zoom['x'][1]) & (df['WorldPosition_y'] >= map_zoom['y'][0]) & (df['WorldPosition_y'] <= map_zoom['y'][1])]['DistanceRoundTrack'].min()
            max_distance = df[(df['WorldPosition_x'] >= map_zoom['x'][0]) & (df['WorldPosition_x'] <= map_zoom['x'][1]) & (df['WorldPosition_y'] >= map_zoom['y'][0]) & (df['WorldPosition_y'] <= map_zoom['y'][1])]['DistanceRoundTrack'].max()
            shared_range = [min_distance, max_distance]
        elif 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
            shared_range = [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']]

    map_fig = create_map_view(df,
                              shared_range = shared_range,
                              map_zoom = map_zoom,
                              landmarks=landmarks)
    lap_figures = [create_line_graph(df, shared_range, view['column'], view['title']) for view in DATA_VIEWS]

    slider_value = shared_range[0] if shared_range else df['DistanceRoundTrack'].min()
    slider_min, slider_max, new_slider_value = update_slider(df, shared_range, slider_value)
    # calculate the step size for the slider
    slider_range = slider_max - slider_min
    step = int(slider_range / 10) + 1
    slider_marks = {i: {'label': str(i)} for i in range(int(slider_min), int(slider_max) + 1, step)}

    return [map_fig] + lap_figures + [shared_range, slider_min, slider_max, slider_marks, new_slider_value]

@app.callback(
    [Output('map-view', 'figure', allow_duplicate=True)] +
    [Output(f'data-{i+1}-view', 'figure', allow_duplicate=True) for i in range(len(DATA_VIEWS))],
    [Input('distance-slider', 'value')],
    [State('shared-range', 'data')],
    prevent_initial_call=True
)
def update_slider_view(slider_value, shared_range):
    logger.info(f"update_slider: Slider value: {slider_value}, shared_range: {shared_range}")
    global df

    patched_map = patch_circle_and_arrow(df, slider_value)
    patched_figures = [patched_map]
    for _ in range(len(DATA_VIEWS)):  # For each of the data views
        patched_figure = add_vertical_line(None, slider_value)
        patched_figures.append(patched_figure)

    return patched_figures

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
        # if response.status_code == 500 or response.status_code == 304:
        #     return response
        # logger.debug('RES--------------------------------')
        # logger.debug(f'Status: {response.status}')
        # logger.debug(f'Headers: {dict(response.headers)}')
        # logger.debug(f'Body: {response.get_data(as_text=True)}')
        try:
            logger.debug(f'Response size: {len(response.get_data(as_text=True))} bytes')
        except:
            pass
        return response

    app.run_server(debug=True)
