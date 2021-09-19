import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

app = dash.Dash(__name__)

params = [
    'SSTVD','L1', 'R1', 'WPS'
]

app.layout = html.Div([



    html.Hr(),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),

    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'Zone', 'name': 'Zone'}] +
            [{'id': p, 'name': p} for p in params]
        ),
        data= [
            dict(Zone=i, **{param: 0 for param in params})
            for i in range(1, 5)
        ],
        editable=True,
        row_deletable=True
    ),

    html.Hr(),

    dcc.Graph(id='table-editing-simple-output')

])



@app.callback(
    Output('table-editing-simple-output', 'figure'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))

def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

    #construct the wells here
    wells = df

    wells['SSTVD'] = wells['SSTVD'].astype(int)
    wells.WPS = wells['WPS'].astype(int).apply(lambda x: x if x > 0 else x + 1)
    wells['W1'] = 5280 - wells.L1.astype(int) - wells.R1.astype(int)
    wells['goal_well_count'] = 5280/wells.WPS
    wells['Wells'] = (wells.W1/wells.goal_well_count).apply(np.floor)

    well_locations = {'Zone': [], 'Well': [], 'SSTVD': []}

    for row in wells.iterrows():
        # return of a list of each well #
        l1 = [*range(int(row[1]['Wells']))]
        l = [x + 1 for x in l1]

        # for each well calculate it's x coordinate
        coor = []
        for well in l1:
            if well == 0:
                coor.append(row[1]['L1'])
            else:
                coor.append(int(well) * float(row[1]['goal_well_count']) + int(row[1]['L1']))

        zipped = [*zip(l, coor)]
        # append to dictionary
        well_locations['Zone'].append(row[1]['Zone'])
        well_locations['Well'].append(zipped)
        well_locations['SSTVD'].append(row[1]['SSTVD'])

    final = pd.DataFrame(well_locations).explode('Well')

    final[['Well_name','X_loc']] = pd.DataFrame(final['Well'].tolist(),index=final.index)
    final = final.drop(columns=['Well'])


    return {
        'data': [
                       go.Scatter(
                           x=final.X_loc,
                           y=final.SSTVD,
                           mode = 'markers',
                           marker = {
                               'size':12,
                               #'color':'rgb(51,204,153)',
                               'symbol':'circle',
                               'line':{'width':2}
                           },
                           #marker_color=df['Zone']
                       )],
        'layout':go.Layout(title='Gun Barrel Diagram',
                                      xaxis = {'title':'Horizontal View'}, #'range':[0,4]},
                                      yaxis = {'title':'Vertical View', 'range':[-1000,0]})}

@app.callback(
    Output('table-editing-simple', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('table-editing-simple', 'data'),
    State('table-editing-simple', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: 0 for c in columns})
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)
