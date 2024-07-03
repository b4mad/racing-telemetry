import sys
import os
import plotly.express as px
import ipywidgets as widgets
import pandas as pd
from IPython.display import display

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(script_dir)
# Add the project root to the Python path
sys.path.append(project_root)

from telemetry import Telemetry
from telemetry.utility import *
from telemetry.analysis import *



