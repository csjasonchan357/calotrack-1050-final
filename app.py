# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from app_setup import app
from apps import app1, app2
import index
import aboutpage

from database import get_data_cache, get_all_food_data

app.layout = html.Div([
    dcc.Location(id='url', pathname = '/app', refresh=False), 
    html.Div(id='page-content')])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app':
        return index.layout
    elif pathname == '/about':
        return aboutpage.layout
    elif pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        '404'

if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
