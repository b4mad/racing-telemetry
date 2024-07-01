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


def get_or_create_df(create_df_func, name=None):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
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

