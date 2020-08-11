
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas_datareader import data as web
from datetime import datetime as dt
import yfinance as yf


app = dash.Dash()



app.layout = html.Div([
    html.Div([
        html.H1('Stock Pic'),

        html.Div(['Ticker: ',
            dcc.Input(id='input-on-submit', value='TSLA', type='text')]),
    
        dcc.Graph(id='my-graph'),
        html.P('')
    ],style={'width': '60%', 'display': 'inline-block'}),
    html.Div([
        html.Table(id='my-table'),
        html.P(''),
    ], style={'width': '35%', 'float': 'right', 'display': 'inline-block'}),
    ])

# for the graph
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

# for the quick take table
@app.callback(
    Output('my-table', 'children'),
    [Input('input-on-submit', 'n_submit')],
    [State('input-on-submit','value')])

def generate_table(submits,inputted_value):
    if inputted_value:
        summary_dict = yf.Ticker(inputted_value).info
        industry = summary_dict['industry']
        marketCap = summary_dict['marketCap']
        return [html.Tr(html.Th('Quick Take'))] + [html.Tr(html.Td(industry))] + [html.Tr(html.Td(marketCap))]


    else:
        return [html.Tr(html.Th('Quick Take'))]

if __name__ == '__main__':
    app.run_server(debug=True)