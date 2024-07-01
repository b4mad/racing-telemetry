import sys
import os
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
from plots import *

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(script_dir)
# Add the project root to the Python path
sys.path.append(project_root)

from telemetry import Telemetry
