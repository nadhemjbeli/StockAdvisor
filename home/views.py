from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from .models import Stock
from .plots import candlestick, compute_bollinger_bands, plot_macd_signal, plot_buy_sell, area_plot_1_day
from .functions import load_url_financials, load_yahoo_annual_income_statement, load_yahoo_annual_cash_flow, get_data, \
    get_macd_signal, buy_sell, quote_type_yahoo, stock_price_yahoo, load_yahoo_annual_balance_sheet
from .dash_apps.finished_apps.simpleexample import get_live_update
# Create your views here.
symbol = 'AAPL'


def home(request):
    def scatter():
        x1 = [1, 2, 3, 4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot1': scatter()
    }

    return render(request, 'home/welcome.html', context)


def search_stock(request):
    message_error = None
    message_stock_exists = None
    message_stock_new = None
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        symbol = symbol.upper()

    else:
        symbol = 'AAPL'
    from pandas_datareader._utils import RemoteDataError
    try:
        ts_df = get_data(symbol, dtime=365)
        try:
            Stock.objects.get(symbol=symbol)
            message_stock_exists = 'Exists in the databases'
        except:
            message_stock_new = 'Entered to the databases'
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/stock.html', {'message_error': message_error, 'symbol': symbol, })
    # get_live_update(symbol)

    json_data_financials = load_url_financials(symbol)

    quote = quote_type_yahoo(json_data_financials)
    print(f'quote: {quote}')
    price_dict = stock_price_yahoo(json_data_financials)

    Stock.objects.get_or_create(
        symbol=quote['symbol'],
        name=quote['shortName'],
        currency=price_dict['currency'],
        exchangeTimezoneName=quote['exchangeTimezoneName'],
        market=quote['market']
    )
    context = {
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
        'message_stock_new': message_stock_new,
        'message_stock_exists': message_stock_exists,
    }

    return render(request, 'home/stock/stock.html', context, )


def get_stock(request, symbol='AAPL'):
    symbol = symbol.upper()
    stocks = Stock.objects.all()
    print('stocks')
    for stock in stocks:
        print(stock)
    context = {
        'stocks': stocks,
        'symbol': symbol,
    }
    return render(request, "home/table_stock.html", context)


def single_stock(request, symbol='AAPL'):
    symbol = symbol.upper()
    get_live_update(symbol)
    message_error = None

    # print(stock)
    from pandas_datareader._utils import RemoteDataError
    try:
        ts_df = get_data(symbol, 365)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'Doesn\'t Exist'
            return render(request, 'home/stock/single_stock.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/single_stock.html', {'message_error': message_error, 'symbol': symbol, })

    # PlotlyGraph
    json_data_financials = load_url_financials(symbol)

    quote = quote_type_yahoo(json_data_financials)
    # print(quote)
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

    return render(request, 'home/stock/single_stock.html', context)


def get_income_statements(request, symbol):
    symbol = symbol.upper()
    message_error = None
    try:
        stock = Stock.objects.get(symbol=symbol)
    except:
        message_error = 'Doesn\'t Exist'
        return render(request, 'home/stock_data_vis/income_statements.html', {'message_error': message_error, 'symbol': symbol, })
    json_data = load_url_financials(symbol)
    print('fmtlong')
    annual_income_statement_longfmt = load_yahoo_annual_income_statement(json_data, 'longFmt')
    print('fmt')
    annual_income_statement_fmt = load_yahoo_annual_income_statement(json_data, 'fmt')
    # print(financials_fmt['annual_income_statements'])
    # financials_raw = load_yahoo_financials(symbol, 'raw')
    context = {
        'stock': stock,
        # 'financials_raw': financials_raw,
        'annual_income_statement_fmt': annual_income_statement_fmt,
        'annual_income_statement_longfmt': annual_income_statement_longfmt,
        'symbol': symbol.upper(),
        'message_error': message_error,
    }

    return render(request, 'home/stock_data_vis/income_statements.html', context)


def get_cash_flow(request, symbol):
    symbol = symbol.upper()
    message_error = None
    try:
        stock = Stock.objects.get(symbol=symbol)
    except:
        message_error = 'Doesn\'t Exist'
        return render(request, 'home/stock_data_vis/cash_flow.html', {'message_error': message_error, 'symbol': symbol, })
    json_data = load_url_financials(symbol)
    print('fmtlong')
    annual_cash_flow_longfmt = load_yahoo_annual_cash_flow(json_data, 'longFmt')
    print('fmt')
    annual_cash_flow_fmt = load_yahoo_annual_cash_flow(json_data, 'fmt')
    # print(financials_fmt['annual_income_statements'])
    # financials_raw = load_yahoo_financials(symbol, 'raw')
    context = {
        'message_error': message_error,
        'stock': stock,
        # 'financials_raw': financials_raw,
        'annual_cash_flow_fmt': annual_cash_flow_fmt,
        'annual_cash_flow_longfmt': annual_cash_flow_longfmt,
        'symbol': symbol,
    }

    return render(request, 'home/stock_data_vis/cash_flow.html', context)


def get_balance_sheet(request, symbol):
    symbol = symbol.upper()
    message_error = None
    try:
        stock = Stock.objects.get(symbol=symbol)
    except:
        message_error = 'Doesn\'t Exist'
        return render(request, 'home/stock_data_vis/income_statements.html', {'message_error': message_error, 'symbol': symbol, })
    json_data_balance_sheet = load_url_financials(symbol)
    print('fmtlong')
    annual_balance_sheet_longfmt = load_yahoo_annual_balance_sheet(json_data_balance_sheet, 'longFmt')
    print('fmt')
    annual_balance_sheet_fmt = load_yahoo_annual_balance_sheet(json_data_balance_sheet, 'fmt')
    context = {
        'stock': stock,
        'annual_balance_sheet_longfmt': annual_balance_sheet_longfmt,
        'annual_balance_sheet_fmt': annual_balance_sheet_fmt,
        'symbol': symbol,
        'message_error': message_error,

    }

    return render(request, 'home/stock_data_vis/balance_sheet.html', context)


# def show_data(request):
#     df = get_data(symbol)
#     # graph = get_simple_plot(x=df['dates'], y=df['Adj'], data=df)
#     graph, plotly = compute_bollinger_bands(df, symbol)
#     context = {
#         'plotly': plotly,
#         'symbol': symbol,
#         'df': df,
#         'graph': graph,
#     }
#     return render(request, "home/visualize.html", context)


def stockAnalysis(request, symbol, dtime=365):
    symbol = symbol.upper()
    get_live_update(symbol)
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        df = get_data(symbol, dtime)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'Doesn\'t Exist'
            return render(request, 'home/stock/stock_analysis.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/stock_analysis.html', {'message_error': message_error, 'symbol': symbol, })
    graph_plotly1, graph_plotly2, graph_plotly3 = compute_bollinger_bands(df, symbol, dtime)
    MACD, signal = get_macd_signal(df, dtime)
    plot_macd = plot_macd_signal(df, symbol, MACD, signal)
    # Create new columns for the data
    df['MACD'] = MACD
    df['Signal Line'] = signal
    # Create buy and sell column
    a = buy_sell(df)
    df['Buy_Signal_Price'] = a[0]
    df['Sell_Signal_Price'] = a[1]

    p_b_s = plot_buy_sell(df, symbol)
    context = {
        'symbol': symbol.upper(),
        'stock': stock,
        'message_error': message_error,
        'graph_plotly1': graph_plotly1,
        'graph_plotly2': graph_plotly2,
        'graph_plotly3': graph_plotly3,
        "plot_macd": plot_macd,
        'p_b_s': p_b_s,
    }
    return render(request, 'home/stock/stock_analysis.html', context)


def get_stock_summary(request, symbol):

    get_live_update(symbol)
    area_1_day = area_plot_1_day(symbol)
    context = {
        'area_1_day': area_1_day,
        'symbol': symbol.upper(),
    }
    return render(request, 'home/stock/summary.html', context)


def get_historical_data(request, symbol):
    symbol = symbol.upper()
    df = get_data(symbol, dtime=365)
    # print(df)
    # data = dict(zip(df['Date'], df['Open']))
    data = []
    df = round(df, 3)
    for i in range(df.shape[0]):
        temp = df.iloc[i]
        data.append(dict(temp))
    # print(data)
    context = {
        'data': data,
        'symbol': symbol,
    }
    return render(request, 'home/stock/historical_data.html', context)


