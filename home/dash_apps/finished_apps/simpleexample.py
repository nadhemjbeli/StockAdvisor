import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import requests
# from home.models import Stock
from bs4 import BeautifulSoup


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')])
def display_value(value):
    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i ** 3)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}


###########################################################################################################

# app1 = DjangoDash('price', external_stylesheets=external_stylesheets)
#
# app1.layout = html.B([
#     # html.H4(id='live-update-text', children='', style={'height': '30px', 'overflow': 'hidden'}),
#     html.B(id='live-update-text', children='',),
#     dcc.Interval(
#         id='interval-component',
#         interval=3000, # 3000 milliseconds = 3 seconds
#         n_intervals=0
#     ),
# ])
#
# @app1.callback(Output('live-update-text', 'children'),
#                [Input('interval-component', 'n_intervals')])
# def update_price(n):
#     stock='AAPL'
#     url_quote = 'https://finance.yahoo.com/quote/{}?p={}'
#     url = url_quote.format(stock, stock)
#     # print(url)
#     r = requests.get(url)
#     # soup = bs4.BeautifulSoup(r.text, 'html.parser')
#     soup = BeautifulSoup(r.text, 'lxml')
#     price = soup.find('div', {'class':'D(ib) Mend(20px)'}).findChildren()[0].text
#     print('Price: {}'.format(price))
#     # change = soup.find('p', {'class':'Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)'}).findChildren()[1].text
#     # return price, change
#     return price


# @app1.callback(Output('live-update-change', 'children'),
#                [Input('interval-component', 'n_intervals')])
# def update_change(n):
#     stock='AAPL'
#     url_quote = 'https://finance.yahoo.com/quote/{}?p={}'
#     url = url_quote.format(stock, stock)
#     # print(url)
#     r = requests.get(url)
#     # soup = bs4.BeautifulSoup(r.text, 'html.parser')
#     soup = BeautifulSoup(r.text, 'lxml')
#     change = soup.find('div', {'class':'D(ib) Mend(20px)'}).findChildren()[1].text
#     print('Change: {}'.format(change))
#     print(type(change))
#     # change = soup.find('p', {'class':'Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)'}).findChildren()[1].text
#     # return price, change
#     return 'Change: {}'.format(change)


def get_live_update(stock):
    app1 = DjangoDash('price', external_stylesheets=external_stylesheets)

    app1.layout = html.Div([
        html.H2(id='live-update-text', children=''),
        # dcc.Interval(
        #     id='interval-component',
        #     interval=3000, # 3000 milliseconds = 3 seconds
        #     n_intervals=0
        # ),

        # html.H2(id='live-update-change', children='Change:'),
        dcc.Interval(
            id='interval-component',
            interval=1*3000,  # 3000 milliseconds = 3 seconds
            n_intervals=1
        ),
    ])

    @app1.callback(Output('live-update-text', 'children'),
                   [Input('interval-component', 'n_intervals')])
    def update_price(n):
        # print(dir(HttpResponse()))
        # print(HttpResponse())
        url_quote = 'https://finance.yahoo.com/quote/{}?p={}'

        url = url_quote.format(stock, stock)
        # print(url)
        r = requests.get(url)
        # soup = bs4.BeautifulSoup(r.text, 'html.parser')
        soup = BeautifulSoup(r.text, 'lxml')
        # price = soup.find('div', {'class': 'D(ib) Va(m) Maw(65%) Ov(h)'}).find('p').findChildren()[0].text
        price = soup.find('div', {'class': 'D(ib) Mend(20px)'}).findChildren()[0].text
        change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).findChildren()[1].text
        time = soup.find('div', {'class': 'D(ib) Mend(20px)'}).findChildren()[3].text
        print('Price: {} {} {}'.format(price, change, time))
        style1 = {'padding': '5px', 'fontSize': '30px', 'font-weight': '700'}
        style2 = {'padding': '5px', 'fontSize': '26px', 'font-weight': '26px'}
        if change[0] == '+':
            style2['color'] = 'green'
        else:
            style2['color'] = 'red'
        return [
            html.Span('Price: {},'.format(price), style=style1),
            html.Span('change: {}'.format(change), style=style2),
        ]






def get_stock_summary(request, symbol):
    get_live_update(symbol)
    area_1_day = area_plot_1_day(symbol)
    context = {
        'area_1_day': area_1_day,
        'symbol': symbol,
    }
    return render(request, 'home/stock/summary.html', context)
