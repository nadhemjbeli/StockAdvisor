#######
# This page updates automatically!
######
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from bs4 import BeautifulSoup
from django_plotly_dash import DjangoDash
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app1 = DjangoDash('price', external_stylesheets=external_stylesheets)

app1.layout = html.Div([
    html.H2(id='live-update-text', children='Price:'),
    # dcc.Interval(
    #     id='interval-component',
    #     interval=3000, # 3000 milliseconds = 3 seconds
    #     n_intervals=0
    # ),

    html.H2(id='live-update-change', children='Change:'),
    dcc.Interval(
        id='interval-component',
        interval=3000, # 3000 milliseconds = 3 seconds
        n_intervals=0
    ),
])

@app1.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_price(n):
    stock='AAPL'
    url_quote = 'https://finance.yahoo.com/quote/{}?p={}'
    url = url_quote.format(stock, stock)
    # print(url)
    r = requests.get(url)
    # soup = bs4.BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.text, 'lxml')
    price = soup.find('div', {'class':'D(ib) Mend(20px)'}).findChildren()[0].text
    print('Price: {}'.format(price))
    # change = soup.find('div', {'class':'D(ib) Mend(20px)'}).findChildren()[0].text
    # return price, change
    return 'Price: {} '.format(price)

@app1.callback(Output('live-update-change', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_change(n):
    stock='AAPL'
    url_quote = 'https://finance.yahoo.com/quote/{}?p={}'
    url = url_quote.format(stock, stock)
    # print(url)
    r = requests.get(url)
    # soup = bs4.BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.text, 'lxml')
    change = soup.find('div', {'class':'D(ib) Mend(20px)'}).findChildren()[1].text
    print('Change: {}'.format(change))
    # change = soup.find('p', {'class':'Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)'}).findChildren()[1].text
    # return price, change
    return 'Change: {}'.format(change)