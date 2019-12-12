import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from sklearn.utils import shuffle
from database import get_data_cache, get_all_food_data
from app_setup import app, colors 

def description2():
    return html.Div(children=[dcc.Markdown('''
        # CaloPlanner
        Now you can have a bit more fun with the different things in our database! Use the filter 
        options on any of the columns to get creative about how to eat and exercise. Just a few ideas --
        try typing in '< 150' into the food calories column to check out some healthier snack options, 
        or type '10' into the duration column and sort by calories to see how to get the most burn 
        without taking too much time out of your day! As usual, you can change the serving quantities
        straight in the table. Finally, just hit the checkbox to see that item appear on the graph. This 
        is a great tool to map out a day's worth of meals and exercise and keep you on track to reach
        your health and fitness goals!''',
        style={'paddingLeft': '5%', 'paddingRight': '5%', 'marginTop': 50, 'marginBottom': 25})])

def food_plan():
    df = shuffle(get_all_food_data(True).drop_duplicates())
    data = df.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='food-explorer',
            columns=[{
                "name": 'Food Name', "id": 'food_name'}, 
                {"name": 'Brand Name', "id": 'brand_name'},
                {"name": 'Serving Unit', "id": 'serving_unit'},
                {"name": 'Serving Quantity', "id": 'serving_qty', 'editable': True},
                {"name": 'Total Calories', "id": 'nf_calories'}],
            data=data,
            fixed_rows={ 'headers': True, 'data': 0 },
            row_deletable=False,
            row_selectable="multi",
            style_data={'fontColor': '#274228'},
            style_cell={'minWidth': '150px', 
                'width': '150px', 
                'maxWidth': '150px', 
                'overflow': 'hidden', 
                'textOverflow': 'ellipsis'},
            style_table={
                'maxHeight': '350px',
                'overflowY': 'scroll',
                "padding": "10px"},
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            style_header={'backgroundColor': '#A9BA9C',
                'fontWeight': 'bold', 
                'fontColor': '#274228', 
                'textAlign': 'left'}, 
            style_data_conditional=[
                {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#D9D9DA'}], 
            css=[{ 'selector': 'td.cell--selected, td.focused', 
            'rule': 'background-color: #D9D9DA !important;'}, 
            { 'selector': 'td.cell--selected *, td.focused *',
            'rule': 'color: #FC6D41 !important;'}],
        )
        ], style={'width': '48%', 'display': 'inline-block', 'padding-right': '10px'})

def exer_plan():
    db = get_data_cache(allow_cached=True)
    df = shuffle(db[2])
    df = df[['name', 'duration_min', 'nf_calories']].drop_duplicates()
    data = df.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='exer-explorer',
            columns=[{
                "name": 'Exercise Name', "id": 'name'}, 
                {"name": 'Duration (Mins)', "id": 'duration_min', 'editable': True},
                {"name": 'Calories Burned', "id": 'cals_burned'}],
            data=data,
            fixed_rows={ 'headers': True, 'data': 0 },
            style_cell={'minWidth': '150px', 
                'width': '150px', 
                'maxWidth': '150px', 
                'overflow': 'hidden', 
                'textOverflow': 'ellipsis'},
            style_table={
                'maxHeight': '350px',
                'overflowY': 'scroll',
                "padding": "10px"},
            style_data_conditional=[
                {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#D9D9DA'}
            ],
            row_deletable=False,
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            row_selectable="multi",
            style_header={'backgroundColor': '#A9BA9C', 
            'fontWeight': 'bold', 
            'textAlign': 'center',
            'fontColor': '#274228'}, 
            css=[{ 'selector': 'td.cell--selected, td.focused', 
            'rule': 'background-color: #D9D9DA !important;'}, 
            { 'selector': 'td.cell--selected *, td.focused *',
            'rule': 'color: #FC6D41 !important;'}]
        )
        ], style={'width': '48%', 'display': 'inline-block', 'padding-left': '10px'})


def dynamic_layout():
    return html.Div([
        description2(),
        dcc.Graph(id='graph-output', style={'width': '90%', 'margin-left': '5%', 'margin-right': '5%'}),
        html.Br(),
        food_plan(),
        exer_plan(), 
        dcc.Link('Return Home', href='/app', 
        style={'color': '#274228'}), 
        html.Br(),
        dcc.Link('Go to CaloTracker', href='/apps/app1', 
        style={'color': '#274228'})],
        id='app2-content')

layout = dynamic_layout()

@app.callback(
    Output('food-explorer', 'data'),
    [Input('food-explorer', 'data_timestamp')],
    [State('food-explorer', 'data')])
def update_food_row(serving, rows):
    df = get_all_food_data()

    for r in rows:
        update = df[df['food_name'] == r['food_name']]
        rowdict = update.to_dict('records')[0]
        temp1 = rowdict['nf_calories']
        temp2 = rowdict['serving_qty']
        try: 
            r['nf_calories'] = float(temp1)/float(temp2) * float(r['serving_qty'])
        except:
            r['nf_calories'] == 'NA'
    return rows


@app.callback(
    Output('exer-explorer', 'data'),
    [Input('exer-explorer', 'data_timestamp')],
    [State('exer-explorer', 'data')])
def update_exer_row(duration, rows):
    
    db = get_data_cache(allow_cached=True)
    df = db[2]

    for r in rows:
        update = df[df['name'] == r['name']]
        rowdict = update.to_dict('records')[0]
        try:
            temp1 = float(rowdict['nf_calories'])
            temp2 = rowdict['duration_min']
            r['cals_burned'] = float(temp1)/float(temp2) * float(r['duration_min'])
            r['name'] = r['name']
        except:
            r['cals_burned'] = 'NA'
    return rows


@app.callback(
    Output('graph-output', 'figure'), 
    [Input('food-explorer', 'derived_virtual_selected_rows'), 
    Input('exer-explorer', 'derived_virtual_selected_rows')], 
    [State('food-explorer', 'derived_viewport_data'), 
    State('exer-explorer', 'derived_viewport_data')])
def update_graph(frows, erows, fdata, edata):
    """"""
    fcals = []
    ecals = []
    ftraces = []
    etraces = []

    if frows is None:
        frows = []
    if erows is None:
        erows = []

    for i in frows: 
        f = fdata[i]
        trace = go.Bar(name = f['food_name'], x = ['Food'], y = [f['nf_calories']], 
                        marker_color = colors[random.randint(1,9)])
        ftraces.append(trace)
        fcals.append(float(f['nf_calories']))
    
    for j in erows:
        e = edata[j]
        trace = go.Bar(name = e['name'], x = ['Exercise'], y = [e['cals_burned']], 
                        marker_color = colors[random.randint(1,9)])
        etraces.append(trace)
        ecals.append(float(e['cals_burned']))

    total = np.sum(fcals) - np.sum(ecals)
    totaltrace = [go.Bar(name = 'Total Caloric Intake', x = ['Total'], y = [total], 
                    marker_color = colors[random.randint(1,9)])]

    traces = ftraces + etraces + totaltrace

    return {
        'data': traces,
        'layout': go.Layout(barmode='stack',
                    title='Personal Calorie Planner',
                    font = dict(color='#274228'),
                    yaxis = dict(title='Number of Calories'),
                    showlegend=False)}



@app.callback(
    Output('food-explorer', 'style_data_conditional'),
    [Input('food-explorer', 'derived_virtual_selected_rows')]
)
def update_styles(selected_rows):
    if selected_rows is None:
        return 
    else:
        return [{
            'if': { 'row_index': i },
            'background_color': '#A9BA9C'
        } for i in selected_rows]

@app.callback(
    Output('exer-explorer', 'style_data_conditional'),
    [Input('exer-explorer', 'derived_virtual_selected_rows')]
)
def update_styles2(selected_rows):
    if selected_rows is None:
        return 
    else:
        return [{
            'if': { 'row_index': i },
            'background_color': '#A9BA9C'
        } for i in selected_rows]

# if __name__ == '__main__':
#     app1.run_server(debug=True, port=1050, host='0.0.0.0')
