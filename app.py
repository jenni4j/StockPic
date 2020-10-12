
import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from pandas_datareader import data as web
from datetime import datetime as dt
import yfinance as yf
import locale
l = locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
import numpy as np

external_stylesheets=["assets/stylesheets.css"]


app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div([
        html.H4('StockPic')
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
        html.Table(id='obs-table'),
        dcc.Textarea(
            id='inv-thesis-textarea',
            value='Investment Thesis:',
            style={'width': '100%', 'height': 80},),
        dcc.Textarea(
            id='comp-adv-textarea',
            value='Competitive Advantages:',
            style={'width': '100%', 'height': 80},),
        dcc.Textarea(
            id='risk-textarea',
            value='Risks & Bear Case:',
            style={'width': '100%', 'height': 80},)
    ], style={'width': '60%', 'float': 'right', 'display': 'inline-block'}),

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
    if type(number) == int or type(number) == float or isinstance(number,np.floating):
        return "{:.2%}".format(number)
    else:
        return number

def multiplize(number):
    if type(number) == int or type(number) == float or isinstance(number,np.floating):
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
        name = summary_dict.get('longName','')
        sector = summary_dict.get('sector','')
        industry = summary_dict.get('industry','')
        marketCap = summary_dict.get('marketCap','')
        marketCap = locale.currency(marketCap, grouping=True)
        trailPE = multiplize(summary_dict.get('trailingPE',''))
        fwdPE = multiplize(summary_dict.get('forwardPE',''))
        evToEbitda = multiplize(summary_dict.get('enterpriseToEbitda',''))
        priceToSales = multiplize(summary_dict.get('priceToSalesTrailing12Months',''))
        profitMargin = percentize(summary_dict.get('profitMargins',''))
        revGrowth = percentize(summary_dict.get('revenueQuarterlyGrowth',''))
        earnGrowth = percentize(summary_dict.get('earningsQuarterlyGrowth',''))
        divYield = percentize(summary_dict.get('dividendYield',''))
        payout = percentize(summary_dict.get('payoutRatio',''))
        return [html.Tr([html.Td('Company'),html.Td(name)])] + \
        [html.Tr([html.Td('Sector'),html.Td(sector)])] + \
        [html.Tr([html.Td('Industry'),html.Td(industry)])] + \
        [html.Tr([html.Td('Market Cap'),html.Td(marketCap)])] + \
        [html.Tr([html.Td('Trailing P/E'),html.Td(trailPE)])] + \
        [html.Tr([html.Td('Forward P/E'),html.Td(fwdPE)])] + \
        [html.Tr([html.Td('Enterprise Value/EBITDA'),html.Td(evToEbitda)])] + \
        [html.Tr([html.Td('Price/Sales'),html.Td(priceToSales)])] + \
        [html.Tr([html.Td('Profit Margin'),html.Td(profitMargin)])] + \
        [html.Tr([html.Td('Quarterly Revenue Growth'),html.Td(revGrowth)])] + \
        [html.Tr([html.Td('Quarterly Earnings Growth'),html.Td(earnGrowth)])] + \
        [html.Tr([html.Td('Dividend Yield'),html.Td(divYield)])] + \
        [html.Tr([html.Td('Payout Ratio'),html.Td(payout)])]
    else:
        return [html.Tr(html.Th(''))]


# for observations table
@app.callback(
    Output('obs-table', 'children'),
    [Input('input-on-submit', 'n_submit')],
    [State('input-on-submit','value')])

def generate_table(submits,inputted_value):
    if inputted_value:
        bs_df = yf.Ticker(inputted_value).balance_sheet
        cf_df = yf.Ticker(inputted_value).cashflow
        is_df = yf.Ticker(inputted_value).financials
        earningsQual = (cf_df.loc['Total Cash From Operating Activities'][0] - cf_df.loc['Capital Expenditures'][0])/cf_df.loc['Net Income'][0]
        if earningsQual < 0.8:
            eqWarning = 'Warning: Free Cashflow appears to be less than 0.8x of net income'
        else:
            eqWarning = ''
        revQualCurr = bs_df.loc['Net Receivables'][0]/is_df.loc['Total Revenue'][0]
        revQualPrev = bs_df.loc['Net Receivables'][1]/is_df.loc['Total Revenue'][1]
        revenueQual = revQualCurr/revQualPrev - 1
        if revenueQual > 0:
            rqWarning = 'Warning: Receivables seem to be becoming a larger component of Revenue'
        else:
            rqWarning = ''
        currentRatio = bs_df.loc['Total Current Assets'][0]/bs_df.loc['Total Current Liabilities'][0]
        if currentRatio < 1.5:
            crWarning = 'Warning: Current Liabilities are less than 1.5x of Current Assets'
        else:
            crWarning = ''
        debtToEquity = bs_df.loc['Total Liab'][0]/(bs_df.loc['Total Assets'][0] - bs_df.loc['Total Liab'][0])
        if debtToEquity > 1.1:
            deWarning = 'Warning: Debt is greater than 1.1x of Equity'
        else:
            deWarning = ''
        icr = is_df.loc['Ebit'][0]/is_df.loc['Interest Expense'][0]
        if icr < 6:
            icrWarning = 'Warning: Earnings only cover less than 6x Interest Expenses'
        else:
            icrWarning = ''
        roe = is_df.loc['Net Income'][0]/bs_df.loc['Total Stockholder Equity'][0]
        if roe < 5:
            roeWarning = 'Warning: Return on Equity is less than 5%'
        else:
            roeWarning = ''
        return [html.Tr([html.Td('Earnings Quality'),html.Td(multiplize(earningsQual)),html.Td(eqWarning)])] + \
        [html.Tr([html.Td('Revenue Quality'),html.Td(percentize(revenueQual)),html.Td(rqWarning)])] + \
        [html.Tr([html.Td('Current Ratio'),html.Td(multiplize(currentRatio)),html.Td(crWarning)])] + \
        [html.Tr([html.Td('Debt to Equity'),html.Td(multiplize(debtToEquity)),html.Td(deWarning)])] + \
        [html.Tr([html.Td('Interest Coverage Ratio'),html.Td(multiplize(icr)),html.Td(icrWarning)])] + \
        [html.Tr([html.Td('Return on Equity'),html.Td(percentize(roe)),html.Td(roeWarning)])]
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