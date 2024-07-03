import plotly.express as px
import pandas as pd
import os

from telemetry.telemetry import Telemetry
from telemetry.plot import *

def plot_sessions(session_ids, landmarks=False, columns=None):
    telemetry = Telemetry()
    telemetry.set_pandas_adapter()
    landmark_df = None
    fig = None
    laps = []

    for session_id in session_ids:
        telemetry.set_filter({'session_id': session_id})
        df = get_or_create_df(lambda: telemetry.get_telemetry_df(), name=str(session_id))
        if not df.empty:
            laps.append(df)

    if laps:
        if columns:
            columns.extend(columns)
        fig = lap_fig(laps[0], columns=columns)  # Initialize the figure with the first lap

        for lap in laps[1:]:
            fig = lap_fig(lap, fig=fig, columns=columns)  # Add subsequent laps to the figure

    if landmarks and laps:
        game = laps[0]['GameName'].iloc[0]
        track = laps[0]['TrackCode'].iloc[0]
        landmark_df = telemetry.landmarks(game=game, track=track)
        if landmark_df is not None:
            for _, landmark in landmark_df.iterrows():
                fig = fig_add_shape(fig, x0=landmark['start'], x1=landmark['start'], color='red')

    return fig


def plot_2d_map_sessions(session_ids, landmarks=False):
    telemetry = Telemetry()
    telemetry.set_pandas_adapter()
    landmark_df = None
    fig = None
    laps = []

    for session_id in session_ids:
        telemetry.set_filter({'session_id': session_id})
        df = get_or_create_df(lambda: telemetry.get_telemetry_df(), name=str(session_id))
        if not df.empty:
            laps.append(df)


    if landmarks and laps:
        game = laps[0]['GameName'].iloc[0]
        track = laps[0]['TrackCode'].iloc[0]
        landmark_df = telemetry.landmarks(game=game, track=track)

    if laps:
        fig = plot_2d_map(laps, landmarks=landmark_df)

    return fig


def get_or_create_df(create_df_func, name=None):
    # Get the directory of the calling function

    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.path.join(current_dir, '../../.cache')
    if name:
        CACHE_FILE = os.path.join(current_dir, f'cached_{name}.pkl')
    else:
        CACHE_FILE = os.path.join(current_dir, 'cached_df.pkl')

    if os.path.exists(CACHE_FILE):
        print("Loading DataFrame from cache...")
        return pd.read_pickle(CACHE_FILE)

    print("DataFrame not found in cache. Creating a new one...")
    df = create_df_func()

    # Cache the DataFrame
    df.to_pickle(CACHE_FILE)
    print("DataFrame cached to disk.")

    return df





