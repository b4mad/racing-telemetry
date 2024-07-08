import plotly.graph_objects as go
import hashlib


def telemetry_for_fig(segment, track_length=None):
    if segment.start > segment.end:
        # add track_length to all distances that are less than start
        df = segment.telemetry.copy()
        if track_length is None:
            track_length = df["DistanceRoundTrack"].max()
            print(f"track_length: {track_length}")
        df["DistanceRoundTrack"] = df["DistanceRoundTrack"].apply(
            lambda x: x + track_length if x < segment.start else x
        )
        return df
    return segment.telemetry


def features_for_fig(segment, track_length, features):
    if segment.start > segment.end:
        features = features.copy()
        for key in ["start", "end", "max_start", "max_end"]:
            value = features[key]
            if value < segment.start:
                # print(f"adding track_length to {key} {value} -> {value + track_length}")
                features[key] = value + track_length
    return features


def get_color_from_string(s):
    """Generate a color based on the hash of the input string, with defaults for Brake and Throttle."""
    if s == "Brake":
        return "red"
    elif s == "Throttle":
        return "green"
    else:
        hash_object = hashlib.md5(s.encode())
        hash_hex = hash_object.hexdigest()
        r, g, b = int(hash_hex[:2], 16), int(hash_hex[2:4], 16), int(hash_hex[4:6], 16)
        return f'rgb({r},{g},{b})'

def lap_fig(df, mode=None, columns=["Throttle", "Brake"], fig=None,
            full_range=True, title=None, show_x_axis=False,
            show_legend=True):
    # Add title with TrackCode and CarModel if not provided
    if title is None:
        title = ""
        track_code = df["TrackCode"].iloc[0]
        car_model = df["CarModel"].iloc[0]
        if track_code:
            title += f"Track: {track_code}"
        if car_model:
            title += f" - Car: {car_model}" if title else f"Car: {car_model}"

    layout_base = {
        # 'height': 100,  # Increased height to accommodate title
        'xaxis': {
            'showgrid': True,
            'zeroline': False,
            'gridcolor': '#E2E2E2',
            'side': 'top',
            'fixedrange': False,
            'visible': show_x_axis,  # Make x-axis visibility optional
            # 'showticklabels': True,  # Show tick labels only when x-axis is visible
        },
        'yaxis': {
            'showline': False,
            'gridcolor': '#E2E2E2',
            'fixedrange': True,
            'title': title
        },
        'margin': {
            'l': 50,
            'r': 0,
            'b': 10,
            't': 5,  # Increased top margin for title
            'pad': 4
        },
        'paper_bgcolor': '#ffffff',
        'plot_bgcolor': '#ffffff'
    }

    fig = fig or go.Figure(layout=layout_base)
    if fig:
        fig.update_layout(layout_base)

    for column in columns:
        color = get_color_from_string(column)
        fig.add_scatter(
            x=df["DistanceRoundTrack"],
            y=df[column],
            marker=dict(size=1),
            mode=mode,
            name=column,
            line=dict(color=color),
            showlegend=show_legend,
        )

    # Set the range of the x-axis and the distance between tick marks
    # set start to the nearest 100 meters
    if not full_range:
        start = df["DistanceRoundTrack"].min()
        start = start - (start % 100)
        # end = df["DistanceRoundTrack"].max()
        # if end - start < 400:
        #     end = start + 400
        end = start + 1000
        x_range = [start, end]
        fig.update_xaxes(range=x_range, dtick=100)

    return fig

def plot_histogram(df, column_name):
    """
    Create a histogram using Plotly.

    :param df: DataFrame containing the data
    :param column_name: Name of the column to plot
    :return: Plotly Figure object
    """
    value_counts = df[column_name].value_counts().sort_values(ascending=False)

    fig = go.Figure(data=[go.Bar(
        x=value_counts.index,
        y=value_counts.values,
        text=value_counts.values,
        textposition='auto',
    )])

    fig.update_layout(
        title=f'Histogram of {column_name}',
        xaxis_title=column_name,
        yaxis_title='Count',
        bargap=0.2,
    )

    return fig


def fig_add_shape(fig, color="black", **kwargs):
    default = dict(
        type="rect",
        xref="x",
        yref="y",
        x0=0,
        y0=0,
        x1=0,
        y1=1,
        line=dict(color=color, width=2, dash="dot"),
    )
    args = {**default, **kwargs}
    fig.add_shape(**args)
    return fig


def fig_add_features(fig, features, color="red"):
    fig_add_shape(fig, x0=features["start"], x1=features["end"], color=color)
    fig_add_shape(
        fig,
        x0=features["max_start"],
        y0=features["max_low"],
        x1=features["max_end"],
        y1=features["max_high"],
        color=color,
    )
    fig_add_shape(
        fig,
        type="line",
        x0=features["max_start"],
        y0=features["force"],
        x1=features["max_end"],
        y1=features["force"],
        line=dict(color="yellow", width=2),
    )

def plot_3d_map(df):
    """
    Create a 3D map using Plotly with WorldPosition coordinates.

    :param df: DataFrame containing WorldPosition_x, WorldPosition_y, and WorldPosition_z columns
    :return: Plotly Figure object
    """
    fig = go.Figure(data=[go.Scatter3d(
        x=df['WorldPosition_x'],
        y=df['WorldPosition_y'],
        z=df['WorldPosition_z'],
        mode='lines',
        line=dict(
            color='blue',
            width=2
        )
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='X Position',
            yaxis_title='Y Position',
            zaxis_title='Z Position',
            aspectmode='data'
        ),
        title='3D Map of World Positions'
    )

    return fig

def plot_2d_map(data, landmarks=None):
    """
    Create a 2D map using Plotly with WorldPosition coordinates and optional landmarks.

    :param data: DataFrame or list of DataFrames containing WorldPosition_x, WorldPosition_y, and DistanceRoundTrack columns
    :param landmarks: DataFrame containing landmark information (optional)
    :return: Plotly Figure object
    """
    fig = go.Figure()

    if isinstance(data, list):
        colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow']
        for i, df in enumerate(data[1:]):
            fig.add_trace(go.Scatter(
                x=df['WorldPosition_x'],
                y=df['WorldPosition_y'],
                mode='lines',
                line=dict(
                    color=colors[i % len(colors)],
                    width=2
                ),
                name=f'Track {i+1}'
            ))
        df = data[0]
    else:
        df = data

    # if landmarks is None or landmarks does not contain any kind == 'segment' rows
    if landmarks is None or landmarks[landmarks['kind'] == 'segment'].empty:
        fig.add_trace(go.Scatter(
            x=df['WorldPosition_x'],
            y=df['WorldPosition_y'],
            mode='lines',
            line=dict(
                color='blue',
                width=2
            ),
            name='Track'
        ))

    if landmarks is not None:
        segment_colors = ['red', 'blue']  # Alternating colors for segments
        color_index = 0

        for _, landmark in landmarks.iterrows():
            if landmark['kind'] == 'turn':
                # Find the closest point to the landmark's start
                closest_point = df.iloc[(df['DistanceRoundTrack'] - landmark['start']).abs().argsort()[:1]]

                fig.add_trace(go.Scatter(
                    x=[closest_point['WorldPosition_x'].values[0]],
                    y=[closest_point['WorldPosition_y'].values[0]],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='red',
                        symbol='star'
                    ),
                    name=f"{landmark['name']}"
                ))
            elif landmark['kind'] == 'segment':
                # Color points between start and end of the segment
                segment_df = df[(df['DistanceRoundTrack'] > landmark['start']) &
                                (df['DistanceRoundTrack'] <= landmark['end'])]

                fig.add_trace(go.Scatter(
                    x=segment_df['WorldPosition_x'],
                    y=segment_df['WorldPosition_y'],
                    mode='lines',
                    marker=dict(
                        size=2,
                        color=segment_colors[color_index % 2],
                    ),
                    name=f"{landmark['name']}"
                ))

                color_index += 1


    # Calculate the range for x and y axes
    x_min, x_max = df['WorldPosition_x'].min(), df['WorldPosition_x'].max()
    y_min, y_max = df['WorldPosition_y'].min(), df['WorldPosition_y'].max()

    # Add a small margin (e.g., 5%) to the range
    margin = 0.05
    x_range = [x_min - margin * (x_max - x_min), x_max + margin * (x_max - x_min)]
    y_range = [y_min - margin * (y_max - y_min), y_max + margin * (y_max - y_min)]

    fig.update_layout(
        xaxis_title='X Position',
        yaxis_title='Y Position',
        title='2D Map of World Positions with Landmarks',
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
            range=x_range,
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            range=y_range,
        )
    )

    return fig
