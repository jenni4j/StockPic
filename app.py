
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()



app.layout = html.Div(children=[
    html.H1('Stock Pic'),

    html.Div(['Ticker: ',
            dcc.Input(id='my-input',value='initial value', type='text')]),
            html.Br(),
            html.Div(id='my-output'),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)

def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)