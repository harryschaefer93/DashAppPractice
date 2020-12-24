import dash
import dash_html_components as html
import dash_core_components as dcc


app = dash.Dash()


app.layout = html.Div([

    html.Label('Dropdown Component:'),
    dcc.Dropdown(
        options=[
            {'label': 'Houston', 'value': 'HTX'},
            {'label': 'Austin', 'value': 'ATX'},
            {'label': 'Dallas', 'value': 'DTX'}],
        value='HTX'),

    html.P(html.Label('Slider Component:')),
    #html.P inserts linebreak so labels aren't on top of eachother
    dcc.Slider(
        min=0,
        max=9,
        marks={i: '{}'.format(i) for i in range(10)},
        value=5),

    html.P(html.Label('Radio Items Component')),
    dcc.RadioItems(
        options=[
            {'label': 'Houston', 'value': 'HTX'},
            {'label': 'Austin', 'value': 'ATX'},
            {'label': 'Dallas', 'value': 'DTX'}],
        value='HTX')

])


if __name__ == '__main__':
    app.run_server()