import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from database import get_data_cache, get_all_food_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
colors = ['#000000', '#FC6D41', '#274228', '#274228', '#7FB800', '#955E42', '#000000', '#F0A202', '#706C61', '#65743A']
