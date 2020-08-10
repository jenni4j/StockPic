
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas_datareader import data as web
from datetime import datetime as dt


app = dash.Dash()



app.layout = html.Div(children=[
    html.H1('Stock Pic'),

    html.Div(['Ticker: ',
            dcc.Input(id='input-on-submit', value='TSLA', type='text')]),
    
    html.H2('Historical Stock Price'),
    dcc.Graph(id='my-graph'),
    html.P('')
])

@app.callback(
    Output('my-graph', 'figure'),
    [Input('input-on-submit', 'n_submit')],
    [State('input-on-submit','value')])

def update_graph(submits,inputted_value):
    if inputted_value:
        stockpricedf = web.DataReader(
            inputted_value, data_source='yahoo',
            start=dt(2013,1,1), end=dt.now())
        return {
            'data': [{
                'x': stockpricedf.index,
                'y': stockpricedf.Close
            }]
        }
    else:
        return {
            'data': []
        }


if __name__ == '__main__':
    app.run_server(debug=True)