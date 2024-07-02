import sys
import os
import plotly.express as px
import ipywidgets as widgets
import pandas as pd
from IPython.display import display
from plots import *

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(script_dir)
# Add the project root to the Python path
sys.path.append(project_root)

from telemetry import Telemetry


def plot_sessions(session_ids, landmarks=False):
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
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.path.join(current_dir, 'cache')
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

