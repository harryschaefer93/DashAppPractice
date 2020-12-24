import dash
import dash_html_components as html
import dash_core_components as dcc

# commonmark.org/help

app = dash.Dash()

markdown_text = '''
### Dash and Markdown
Dash Apps can be written with Markdown syntax.

Dash uses the [CommonMark] (http://commonmark.org/) style of Markdown.

You can do **bold text** and *italics*

Plus even inline code snippets ect. 
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text)
])

if __name__ == '__main__':
    app.run_server()