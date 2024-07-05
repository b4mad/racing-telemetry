import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
            dcc.Slider(
                id='distance-slider',
                min=df['DistanceRoundTrack'].min(),
                max=df['DistanceRoundTrack'].max(),
                step=1,
                value=df['DistanceRoundTrack'].min(),
                marks={i: str(i) for i in range(int(df['DistanceRoundTrack'].min()), int(df['DistanceRoundTrack'].max()), 1000)},
                updatemode='mouseup'
            ),
            dcc.Graph(id='speed-view', style={'height': '16.67%'}),
            dcc.Graph(id='throttle-view', style={'height': '16.67%'}),
            dcc.Graph(id='brake-view', style={'height': '16.67%'}),
            dcc.Graph(id='gear-view', style={'height': '16.67%'}),
            dcc.Graph(id='steer-view', style={'height': '16.67%'}),
            dcc.Graph(id='time-view', style={'height': '16.67%'})
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
     Input('time-view', 'relayoutData'),
     Input('distance-slider', 'value')],
    [State('shared-range', 'data')]
)
def update_views(map_relayout, speed_relayout, throttle_relayout, brake_relayout, gear_relayout, steer_relayout, time_relayout, slider_value, shared_range):
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

    map_fig = plot_2d_map([df])
    speed_fig = lap_fig(df, columns=["SpeedMs"], title="Speed (m/s)", show_legend=False)
    throttle_fig = lap_fig(df, columns=["Throttle"], title="Throttle", show_legend=False)
    brake_fig = lap_fig(df, columns=["Brake"], title="Brake", show_legend=False)
    gear_fig = lap_fig(df, columns=["Gear"], title="Gear", show_legend=False)
    steer_fig = lap_fig(df, columns=["SteeringAngle"], title="Steering Angle", show_legend=False)
    time_fig = lap_fig(df, columns=["CurrentLapTime"], title="Lap Time", show_legend=False)

    figures = [map_fig, speed_fig, throttle_fig, brake_fig, gear_fig, steer_fig, time_fig]

    if trigger_id == 'distance-slider':
        for fig in figures:
            if fig == map_fig:
                # For the map view, we need to update both x and y axes
                filtered_df = df[df['DistanceRoundTrack'] <= slider_value]
                min_x = filtered_df['WorldPosition_x'].min()
                max_x = filtered_df['WorldPosition_x'].max()
                min_y = filtered_df['WorldPosition_y'].min()
                max_y = filtered_df['WorldPosition_y'].max()
                margin = 50  # Add a margin around the visible area
                fig.update_layout(
                    xaxis=dict(range=[min_x - margin, max_x + margin]),
                    yaxis=dict(range=[min_y - margin, max_y + margin])
                )
            else:
                fig.add_vline(x=slider_value, line_width=2, line_dash="dash", line_color="red")
    elif shared_range:
        for fig in figures:
            if fig == map_fig:
                # For the map view, we need to update both x and y axes
                min_distance, max_distance = shared_range
                filtered_df = df[(df['DistanceRoundTrack'] >= min_distance) & (df['DistanceRoundTrack'] <= max_distance)]
                min_x = filtered_df['WorldPosition_x'].min()
                max_x = filtered_df['WorldPosition_x'].max()
                min_y = filtered_df['WorldPosition_y'].min()
                max_y = filtered_df['WorldPosition_y'].max()
                margin = 50  # Add a margin around the visible area
                fig.update_layout(
                    xaxis=dict(range=[min_x - margin, max_x + margin]),
                    yaxis=dict(range=[min_y - margin, max_y + margin])
                )
            else:
                fig.update_xaxes(range=shared_range)

    slider_min = df['DistanceRoundTrack'].min()
    slider_max = df['DistanceRoundTrack'].max()
    new_slider_value = slider_value

    if shared_range:
        slider_min = max(slider_min, shared_range[0])
        slider_max = min(slider_max, shared_range[1])
        new_slider_value = max(slider_min, min(slider_value, slider_max))

    return *figures, shared_range, slider_min, slider_max, new_slider_value

if __name__ == '__main__':
    app.run_server(debug=True)



