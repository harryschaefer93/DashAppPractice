import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('gapminderDataFiveYear.csv')

#options for the dropdown
year_options = []
for year in df.year.unique():
    year_options.append({'label':str(year),'value':year})

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='scatterplot1'),
    dcc.Dropdown(id = 'dropdown', options=year_options, value=df.year.min())
])

@app.callback(Output(component_id='scatterplot1',component_property='figure'),
              [Input(component_id='dropdown',component_property='value')])

def update_graph(selected_year):
    #Data for selected year from dropdown
    filtered_df = df[df.year == selected_year]

    traces = []
    for name in filtered_df.continent.unique():

        df_by_continent = filtered_df[filtered_df.continent == name]

        #adding a scatterplot for each continent
        traces.append(go.Scatter(
            x = df_by_continent.gdpPercap,
            y = df_by_continent.lifeExp,
            mode = 'markers',
            opacity = 0.7,
            marker = {'size':15},
            name = name
        ))

    return {'data': traces, 'layout':go.Layout(title='My Plot',
                                      xaxis={'title': 'GDP per Capita','type':'log'},
                                      yaxis={'title': 'Population Expectancy'})}




if __name__ == '__main__':
    app.run_server()