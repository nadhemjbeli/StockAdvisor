import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from bs4 import BeautifulSoup
from home.plots import *

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
            interval=1*4000,  # 3000 milliseconds = 3 seconds
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
        price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('div').findChildren()[0].text
        change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).findChildren()[1].text
        print('Price: {} {}'.format(price, change))
        style1 = {'padding': '5px', 'fontSize': '30px'}
        style2 = {'padding': '5px', 'fontSize': '26px', 'font-weight': '26px'}
        if change[0] == '+':
            style2['color'] = 'green'
        else:
            style2['color'] = 'red'
        # return [
        #     html.Span('Price: {},'.format(price), style=style1),
        #     html.Span('change: {}'.format(change), style=style2),
        # ]
        return 'price: {}'.format(price)

def get_stock(request, symbol='AAPL'):
    stocks = Stock.objects.all()

    context = {
        'stocks': stocks,
        'symbol': symbol,
    }
    return render(request, "home/table_stock.html", context)


def single_stock(request, symbol='AAPL'):
    get_live_update(symbol)
    message_error = None
    stock = Stock.objects.get(symbol=symbol)
    # print(stock)
    from pandas_datareader._utils import RemoteDataError
    try:
        ts_df = get_data(symbol)
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock.html', {'message_error': message_error, 'symbol': symbol, })

    # PlotlyGraph
    json_data_financials = load_url_financials(symbol)

    quote = quote_type_yahoo(json_data_financials)
    print(quote)
    price_dict = stock_price_yahoo(json_data_financials)
    # price_dict_long_fmt = stock_price_yahoo(json_data_financials, 'longFmt')
    # token = 'Tpk_b1ce81ac4db5431c97ffe71615ee3689'
    # api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={token}'
    # data = requests.get(api_url).json()
    # print(f'data:\n{data}')
    # data['changePercent'] = round(data['changePercent'], 3)
    # stock_data = get_stock_quote(symbol, api_key)
    # print(f'stock_data:\n{stock_data}')
    # models.Stock.objects.get_or_create(symbol=quote['symbol'], name=quote['shortName'], currency=quote['currency'])
    context = {
        'stock': stock,
        'symbol': symbol,
        # 'stock_data': stock_data,
        # 'data': data,
        'quote': quote,
        'candlestick': candlestick(ts_df),
        # 'plotly': plotly(ts_df),
        # 'plotly_slider': plotly_slider(ts_df),
        # 'compare_stock': compare_stock(),
        'price_dict': price_dict,
        'message_error': message_error,
    }

    return render(request, 'home/stock.html', context)


def search_stock(request):
    message_error = None
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        symbol = symbol.upper()

    else:
        symbol = 'AAPL'
    from pandas_datareader._utils import RemoteDataError
    try:
        ts_df = get_data(symbol)
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock.html', {'message_error': message_error, 'symbol': symbol, })
    get_live_update(symbol)

    def compare_stock():
        df = px.data.stocks()
        fig = px.line(df, x="date", y=df.columns,
                      hover_data={"date": "|%B %d, %Y"},
                      title='custom tick labels')
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y")
        compare_div = plot(fig, output_type='div')
        return compare_div

    json_data_financials = load_url_financials(symbol)

    quote = quote_type_yahoo(json_data_financials)
    print(quote)
    price_dict = stock_price_yahoo(json_data_financials)

    models.Stock.objects.get_or_create(symbol=quote['symbol'], name=quote['shortName'], currency=price_dict['currency'])
    context = {
        'symbol': symbol,
        # 'stock_data': stock_data,
        # 'data': data,
        'quote': quote,
        'candlestick': candlestick(ts_df),
        'plotly': plotly(ts_df),
        'plotly_slider': plotly_slider(ts_df),
        'compare_stock': compare_stock(),
        'price_dict': price_dict,
        'message_error': message_error,
    }

    return render(request, 'home/stock.html', context, )
