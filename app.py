
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas_datareader import data as web
from datetime import datetime as dt
import yfinance as yf
import locale
l = locale.setlocale(locale.LC_ALL, 'en_US.utf-8')


app = dash.Dash()



app.layout = html.Div([
    html.Div([
        html.H4('Stock Pic')
    ]),
    html.Div(['Ticker: ',
        dcc.Input(
            id='input-on-submit', 
            value='TSLA', 
            type='text'
        )
    ], style={'font-size': 'large'}),
    
    html.Div([
        html.H6('Key Metrics'),
        html.Table(id='metrics-table')
    ], style={'width': '40%', 'display': 'inline-block'}),
    
    html.Div([
        html.H6('Observations'),
        html.Table(id='obs-table')
    ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),

    html.Div([
        html.H6('Company Description'),
        html.Table(id='desc-table')
    ], style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        html.H6('Price History'),
        dcc.Graph(id='price-graph')
    ], style={'width': '100%', 'display': 'inline-block'})
])

# helper functions
def percentize(number):
    if type(number) == int or type(number) == float:
        return "{:.2%}".format(number)
    else:
        return number

def multiplize(number):
    if type(number) == int or type(number) == float:
        return str(round(number,2)) + 'x'
    else:
        return number    


# for the graph
@app.callback(
    Output('price-graph', 'figure'),
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

# for the key metrics table
@app.callback(
    Output('metrics-table', 'children'),
    [Input('input-on-submit', 'n_submit')],
    [State('input-on-submit','value')])

def generate_table(submits,inputted_value):
    if inputted_value:
        summary_dict = yf.Ticker(inputted_value).info
        name = summary_dict['longName']
        industry = summary_dict['industry']
        marketCap = summary_dict['marketCap']
        marketCap = locale.currency(marketCap, grouping=True)
        trailPE = multiplize(summary_dict['trailingPE'])
        fwdPE = multiplize(summary_dict['forwardPE'])
        evToEbitda = multiplize(summary_dict['enterpriseToEbitda'])
        priceToSales = multiplize(summary_dict['priceToSalesTrailing12Months'])
        priceToBook = multiplize(summary_dict['priceToBook'])
        profitMargin = percentize(summary_dict['profitMargins'])
        revGrowth = percentize(summary_dict['revenueQuarterlyGrowth'])
        earnGrowth = percentize(summary_dict['earningsQuarterlyGrowth'])
        divYield = percentize(summary_dict['dividendYield'])
        payout = percentize(summary_dict['payoutRatio'])
        return [html.Tr([html.Td('Company'),html.Td(name)])] + \
        [html.Tr([html.Td('Industry'),html.Td(industry)])] + \
        [html.Tr([html.Td('Market Cap'),html.Td(marketCap)])] + \
        [html.Tr([html.Td('Trailing P/E'),html.Td(trailPE)])] + \
        [html.Tr([html.Td('Forward P/E'),html.Td(fwdPE)])] + \
        [html.Tr([html.Td('Price/Sales'),html.Td(priceToSales)])] + \
        [html.Tr([html.Td('Price/Book'),html.Td(priceToBook)])] + \
        [html.Tr([html.Td('Profit Margin'),html.Td(profitMargin)])] + \
        [html.Tr([html.Td('Quarterly Revenue Growth'),html.Td(revGrowth)])] + \
        [html.Tr([html.Td('Quarterly Earnings Growth'),html.Td(earnGrowth)])] + \
        [html.Tr([html.Td('Dividend Yield'),html.Td(divYield)])] + \
        [html.Tr([html.Td('Payout Ratio'),html.Td(payout)])]
    else:
        return [html.Tr(html.Th(''))]


# for the company description table
@app.callback(
    Output('desc-table', 'children'),
    [Input('input-on-submit', 'n_submit')],
    [State('input-on-submit','value')])

def generate_table(submits,inputted_value):
    if inputted_value:
        summary_dict = yf.Ticker(inputted_value).info
        desc = summary_dict['longBusinessSummary']
        return [html.Tr(html.Td(desc))]   
    else:
        return [html.Tr(html.Th(''))]



if __name__ == '__main__':
    app.run_server(debug=True)