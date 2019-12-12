import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.utils import shuffle
from database import get_data_cache, get_all_food_data
import ETL
import random
from app_setup import app, colors


def description():
    return html.Div(children=[dcc.Markdown('''
        # CaloTracker
        This is an interactive tool for you to search and log different foods from our existing
        database of foods. Your caloric total will be divided between food and exercise, with labels
        for each individual entry to really help you break your intake down! Just search for a food
        or exercise using the dropdown bars, and the full info will appear in the table. Change 
        your serving quantity and time spend working out straight in the table, as well; the total
        calories will automatically update in the table and in the graph. And, if you can't find the
        food or exercise that you're looking for, query it yourself from our API, and the dropdown 
        bars will contain any new results. Happy logging!''',
        style={'paddingLeft': '5%', 'paddingRight': '5%', 'marginTop': 50, 'marginBottom': 25 
        })])

def food_log():
    df = shuffle(get_all_food_data(False))
    opts = df['food_name'].unique()
    #data = df.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='foods-table',
            columns=[{
                "name": 'Food Name', "id": 'food_name'}, 
                {"name": 'Brand Name', "id": 'brand_name'},
                {"name": 'Serving Unit', "id": 'serving_unit'},
                {"name": 'Serving Quantity', "id": 'serving_qty', 'editable': True},
                {"name": 'Total Calories', "id": 'nf_calories'}], 
            data=[],
            row_deletable=True,
            fixed_rows={ 'headers': True, 'data': 0 },
            style_cell={'minWidth': '65px', 
                'width': '65px', 
                'maxWidth': '65px', 
                'overflow': 'hidden', 
                'textOverflow': 'ellipsis'},
            style_table={
                'maxHeight': '300px',
                'overflowY': 'scroll',
                'margin-left': '7px', 
                'padding-right': '7%'
                },    
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            css=[{ 'selector': 'td.cell--selected, td.focused', 
                'rule': 'background-color: #D9D9DA !important;'}, 
                { 'selector': 'td.cell--selected *, td.focused *',
                'rule': 'color: #FC6D41 !important;'}],
            style_header={'backgroundColor': '#A9BA9C',
                'fontWeight': 'bold', 
                'textAlign': 'center'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': '#D9D9DA'}
                ]), 
        html.Br(),
        html.Div([dcc.Dropdown(
            id='food-log',
            options=[{'label': i, 'value': i} for i in opts],
            placeholder="Select a food")], 
            style={'margin-left': '11%', 'color': '#274228', 'width': '80%'}),
        html.Div([html.Button('Add Food',
            id='adding-food-button',
            n_clicks=0)], 
            style={'margin-left': '11%', 'display': 'inline-block', 'color': '#274228'})],
        style={'width': '48%', 'display': 'inline-block'})

def exer_log():
    db = get_data_cache(allow_cached=True)
    df = shuffle(db[2])
    #data = df.to_dict('records')
    opts = df['name'].unique()
    return html.Div([
        dash_table.DataTable(
            id='exer-table',
            columns=[{
                "name": 'Exercise Name', "id": 'exer_name'}, 
                {"name": 'Duration (Mins)', "id": 'duration_min', 'editable': True},
                {"name": 'Calories Burned', "id": 'cals_burned'}],
            data=[],
            fixed_rows={ 'headers': True, 'data': 0 },
            style_cell={'minWidth': '65px', 
                'width': '65px', 
                'maxWidth': '65px', 
                'overflow': 'hidden', 
                'textOverflow': 'ellipsis', 
                'fontColor': '#274228'},
            style_table={
                'maxHeight': '300px',
                'overflowY': 'scroll',
                'margin-right': '5%', 
                'padding-left': '9%'
                },
            row_deletable=True,
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': '#D9D9DA'}
                ],
            style_header={'backgroundColor': '#A9BA9C',
                'fontWeight': 'bold', 
                'textAlign': 'center'}, 
            css=[{ 'selector': 'td.cell--selected, td.focused', 
            'rule': 'background-color: #D9D9DA !important;'}, 
            { 'selector': 'td.cell--selected *, td.focused *',
            'rule': 'color: #FC6D41 !important;'}]
        ),
        html.Br(),
        html.Div([dcc.Dropdown(
            id='exer-log',
            options=[{'label': i, 'value': i} for i in opts],
            placeholder="Select an exercise")],
            style={'margin-left': '17%', 'color': '#274228'}),
        html.Div([html.Button('Add Exercise',
            id='adding-exercise-button',
            n_clicks=0)], 
            style={'margin-left': '17%', 
            'display': 'inline-block', 'color': '#274228', 'fontColor': '#A9BA9C'})], 
        style={'width': '48%', 'display': 'inline-block'})

def food_search():
    """"""
    return html.Div([
        dcc.Input(id='food-search', type='text', value=''),
        html.Button('Find my food!', id='food-submit', n_clicks=0, 
        style={'margin-left': '5px'}),
        html.P(id='food-output')], 
        style={'display': 'inline-block', 
        'align-items': 'center',
        'margin-left': '14%',
        'margin-right': '5%'}
    )

def exer_search():
    """"""
    return html.Div([
        dcc.Input(id='exer-name-search', type='text', value=''),
        html.Button('Find my exercise!', id='exer-submit', n_clicks=0, 
        style={'margin-left': '5px'}),
        html.P(id='exer-output')], 
        style={'display': 'inline-block', 
        'align-items': 'center', 
        'margin-right': '14%', 
        'margin-left': '5%'}
    )

def dynamic_layout():
    return html.Div([
        description(),
        dcc.Graph(id='log-graph', style={'width': '90%', 'margin-left': '5%', 'margin-right': '5%'}),
        food_log(),
        exer_log(),
        html.Br(),
        html.Br(),
        dcc.Markdown('''Couldn't find what you were looking for? Try searching the API with the name of a food,
        exercise,or a list of either separated by a common and space (and please be patient)! Foods go in the
        left search bar, and exercises on the right.''', style={'paddingLeft': '5%', 'paddingRight': '5%'}),
        food_search(),
        exer_search(),
        html.Br(),
        dcc.Link('Return Home', href='/app', 
        style={'color': '#274228'}), 
        html.Br(),
        dcc.Link('Go to CaloPlanner', href='/apps/app2', 
        style={'color': '#274228'})],
        id='app1-content')

layout = dynamic_layout()

@app.callback(
    Output('foods-table', 'data'),
    [Input('adding-food-button', 'n_clicks'), 
    Input('foods-table', 'data_timestamp')],
    [State('food-log', 'value'),
    State('foods-table', 'data'),
    State('foods-table', 'columns')])
def update_food_row(n_clicks, serving, food, rows, columns):
    
    df = get_all_food_data(True)
    info = df[df['food_name']==food]

    def add_row(r): 
        if len(info) == 0:
            pass
        else: 
            rowdict = info.to_dict('records')[0]
            vals = rowdict.values()
            r.append({c['id']: v for (c,v) in zip(columns, vals)})
        return r 
    
    if len(rows) == 0:
        add_row(rows)
    
    else:
        test = [list(r.values()) for r in rows]
        flat_list = [item for sublist in test for item in sublist]
        if food in flat_list:
            pass
        else:
            add_row(rows) 

    for r in rows:
        update = df[df['food_name'] == r['food_name']]
        rowdict = update.to_dict('records')[0]
        temp1 = rowdict['nf_calories']
        temp2 = rowdict['serving_qty']
        r['nf_calories'] = float(temp1)/float(temp2) * float(r['serving_qty'])
    return rows

@app.callback(
    Output('exer-table', 'data'),
    [Input('adding-exercise-button', 'n_clicks'), 
    Input('exer-table', 'data_timestamp')],
    [State('exer-log', 'value'),
    State('exer-table', 'data'),
    State('exer-table', 'columns')])
def update_exer_row(n_clicks, duration, exercise, rows, columns):
    
    db = get_data_cache(allow_cached=True)
    df = db[2]
    info = df[df['name']==exercise]

    def add_erow(r): 
        if len(info) == 0:
            pass
        else: 
            rowdict = info.to_dict('records')[0]
            vals = rowdict.values()
            r.append({c['id']: v for (c,v) in zip(columns, vals)})
        return r 
    
    if len(rows) == 0:
        add_erow(rows)
    
    else:
        test = [list(r.values()) for r in rows]
        flat_list = [item for sublist in test for item in sublist]
        if exercise in flat_list:
            pass
        else:
            add_erow(rows) 

    for r in rows:
        update = df[df['name'] == r['exer_name']]
        rowdict = update.to_dict('records')[0]
        temp1 = rowdict['nf_calories']
        temp2 = rowdict['duration_min']
        r['cals_burned'] = float(temp1)/float(temp2) * float(r['duration_min'])
    return rows

@app.callback(
    Output('log-graph', 'figure'),
    [Input('foods-table', 'derived_viewport_data'),
     Input('exer-table', 'derived_viewport_data')],
     [State('foods-table', 'columns'),
     State('exer-table', 'columns')])
def display_output(frows, erows, fcols, ecols):

    fcals = []
    ecals = []
    ftraces = []
    etraces = []

    if frows is None:
        pass
    else:
        for f in frows:
            trace = go.Bar(name = f['food_name'],
                x = ['Food'],
                y = [f['nf_calories']], 
                marker_color = colors[random.randint(1,9)])
            ftraces.append(trace)
            fcals.append(f['nf_calories'])
    
    if erows is None:
        pass
    else:
        for e in erows:
            trace = go.Bar(name = e['exer_name'],
                x = ['Exercise'],
                y = [e['cals_burned']],
                marker_color = colors[random.randint(1,9)])
            etraces.append(trace)
            ecals.append(e['cals_burned'])

    total = np.sum(fcals) - np.sum(ecals)
    totaltrace = [go.Bar(name = 'Total Caloric Intake',
                    x = ['Total'],
                    y = [total], 
                    marker_color = colors[random.randint(1,9)])]

    traces = ftraces + etraces + totaltrace

    return {
        'data': traces,
        'layout': go.Layout(barmode='stack',
                    title='Personal Calorie Log',
                    font = dict(color = '#274228'),
                    yaxis = dict(title='Number of Calories'),
                    showlegend=False)}

@app.callback(
    Output('food-output', 'children'), 
    [Input('food-submit', 'n_clicks')], 
    [State('food-search', 'value')]
)
def foodapi(click, term):
    if click == 0: 
        return 
    else: 
        hits = ETL.user_food_query(term)
        return u'Your query returned {} results!'.format(hits)

@app.callback(
    Output('exer-output', 'children'), 
    [Input('exer-submit', 'n_clicks')], 
    [State('exer-name-search', 'value')]
)
def exerapi(click, term):
    if click == 0: 
        return 
    else: 
        hits = ETL.user_exercise_query(term)
        return u'Your query returned {} results!'.format(hits)

@app.callback(
    Output('exer-log', 'options'), 
    [Input('exer-output', 'children')]
)
def update_exer_drop(refresh):
    df = shuffle(get_data_cache()[2])
    opts = df['name'].unique()
    return [{'label': i, 'value': i} for i in opts]

@app.callback(
    Output('food-log', 'options'), 
    [Input('food-output', 'children')]
)
def update_food_drop(refresh):
    df = shuffle(get_all_food_data(False))
    opts = df['food_name'].unique()
    return [{'label': i, 'value': i} for i in opts]

# if __name__ == '__main__':
#     app.run_server(debug=True, port=1050, host='0.0.0.0')
