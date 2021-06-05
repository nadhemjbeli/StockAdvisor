from django.shortcuts import render, redirect
import requests

from newsapi.newsapi_client import NewsApiClient
from textblob import TextBlob
from newspaper import Article
from plotly.offline import plot
import plotly.graph_objects as go
from .models import Stock, Portfolio
from .plots import candlestick, compute_bollinger_bands, plot_macd_signal, plot_buy_sell, area_plot_1_day, \
    area_plot_1_day_candlestick
from .analysis import get_data, get_macd_signal, buy_sell
from .scraping import load_url_financials, load_yahoo_annual_income_statement, load_yahoo_annual_cash_flow,quote_type_yahoo, \
    stock_price_yahoo, load_yahoo_annual_balance_sheet, load_url_profiles
from .dash_apps.finished_apps.simpleexample import get_live_update
from django.contrib.auth.decorators import login_required
"""polygon.io api"""
API_KEY='XJbvhCkUsEt31XBLRM5wv3EYUAf6SUJb'

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


@login_required
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
        'quote': quote,
        'candlestick': candlestick(ts_df),
        'price_dict': price_dict,
        'message_error': message_error,
        'message_stock_new': message_stock_new,
        'message_stock_exists': message_stock_exists,
    }

    return render(request, 'home/stock/stock.html', context, )


@login_required
def get_stock(request, symbol='AAPL'):
    symbol = symbol.upper()
    stocks = Stock.objects.all()
    print('stocks')
    print('length: ', len(stocks))
    for stock in stocks:
        print(stock.pk, ' ', stock)

    context = {
        'stocks': stocks,
        'symbol': symbol,
    }
    return render(request, "home/table_stock.html", context)


@login_required
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
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock/single_stock.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/single_stock.html', {'message_error': message_error, 'symbol': symbol, })

    json_data_financials = load_url_financials(symbol)
    quote = quote_type_yahoo(json_data_financials)
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
        'price_dict': price_dict,
        'message_error': message_error,
    }

    return render(request, 'home/stock/single_stock.html', context)


def get_income_statements(request, symbol):
    symbol = symbol.upper()
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        print('hi')
        get_data(symbol, dtime=2)
        print('hi2')
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases yet'
            return render(request, 'home/stock_data_vis/income_statements.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock_data_vis/income_statements.html', {'message_error': message_error, 'symbol': symbol, })
    print('hi3')
    json_data = load_url_financials(symbol)
    print('fmtlong')
    annual_income_statement_longfmt = load_yahoo_annual_income_statement(json_data, 'longFmt')
    print('fmt')
    annual_income_statement_fmt = load_yahoo_annual_income_statement(json_data, 'fmt')
    context = {
        'stock': stock,
        'annual_income_statement_fmt': annual_income_statement_fmt,
        'annual_income_statement_longfmt': annual_income_statement_longfmt,
        'symbol': symbol.upper(),
        'message_error': message_error,
    }

    return render(request, 'home/stock_data_vis/income_statements.html', context)


def get_cash_flow(request, symbol):
    symbol = symbol.upper()
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        get_data(symbol, dtime=2)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock_data_vis/cash_flow.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock_data_vis/cash_flow.html', {'message_error': message_error, 'symbol': symbol, })
    json_data = load_url_financials(symbol)
    print('fmtlong')
    annual_cash_flow_longfmt = load_yahoo_annual_cash_flow(json_data, 'longFmt')
    print('fmt')
    annual_cash_flow_fmt = load_yahoo_annual_cash_flow(json_data, 'fmt')
    context = {
        'message_error': message_error,
        'stock': stock,
        'annual_cash_flow_fmt': annual_cash_flow_fmt,
        'annual_cash_flow_longfmt': annual_cash_flow_longfmt,
        'symbol': symbol,
    }

    return render(request, 'home/stock_data_vis/cash_flow.html', context)


def get_balance_sheet(request, symbol):
    symbol = symbol.upper()
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        get_data(symbol, dtime=2)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock_data_vis/balance_sheet.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock_data_vis/balance_sheet.html', {'message_error': message_error, 'symbol': symbol, })
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


def get_profiles(request, symbol):
    symbol = symbol.upper()
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        get_data(symbol, dtime=2)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock_data_vis/balance_sheet.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock_data_vis/balance_sheet.html', {'message_error': message_error, 'symbol': symbol, })
    json_data_profiles = load_url_profiles(symbol)
    print('profiles')
    profiles = json_data_profiles['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers']
    for i, p in enumerate(profiles):
        print(i)
        print(p)
    context = {
        'stock': stock,
        'profiles': profiles,
        'symbol': symbol,
        'message_error': message_error,

    }

    return render(request, 'home/stock_data_vis/profiles.html', context)


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
            message_error = 'is a valid stock but doesn\'t Exist in our databases'
            return render(request, 'home/stock/stock_analysis.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/stock_analysis.html', {'message_error': message_error, 'symbol': symbol, })
    graph_plotly_bollinger, graph_plotly_daily_returns = compute_bollinger_bands(df, symbol, dtime)
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
        'graph_plotly_bollinger': graph_plotly_bollinger,
        'graph_plotly_daily_returns': graph_plotly_daily_returns,
        "plot_macd": plot_macd,
        'p_b_s': p_b_s,
    }
    return render(request, 'home/stock/stock_analysis.html', context)


def get_stock_summary(request, symbol):
    symbol=symbol.upper()
    from pandas_datareader._utils import RemoteDataError
    try:
        get_live_update(symbol)
        area_1_day = area_plot_1_day(symbol)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock/summary.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/summary.html', {'message_error': message_error, 'symbol': symbol, })
    context = {
        'area_1_day': area_1_day,
        'stock': stock,
        'symbol': symbol.upper(),
    }
    return render(request, 'home/stock/summary.html', context)


def get_stock_summary_candlestick(request, symbol):
    symbol=symbol.upper()
    from pandas_datareader._utils import RemoteDataError
    try:
        get_live_update(symbol)
        area_1_day_candlestick = area_plot_1_day_candlestick(symbol)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but Doesn\'t Exist in our databases'
            return render(request, 'home/stock/summary_candlestick.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/summary_candlestick.html', {'message_error': message_error, 'symbol': symbol, })
    context = {
        'area_1_day_candlestick': area_1_day_candlestick,
        'stock': stock,
        'symbol': symbol.upper(),
    }
    return render(request, 'home/stock/summary_candlestick.html', context)


def get_historical_data(request, symbol):
    symbol = symbol.upper()
    message_error = None
    from pandas_datareader._utils import RemoteDataError
    try:
        df = get_data(symbol, dtime=365)
        try:
            stock = Stock.objects.get(symbol=symbol)
        except:
            message_error = 'is a valid stock but doesn\'t Exist in our databases'
            return render(request, 'home/stock/historical_data.html', {'message_error': message_error, 'symbol': symbol, })
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock/historical_data.html', {'message_error': message_error, 'symbol': symbol, })
    data = []
    df = round(df, 3)
    for i in range(df.shape[0]):
        temp = df.iloc[i]
        data.append(dict(temp))
    context = {
        'data': data,
        'symbol': symbol,
        'stock': stock,
        'message_error': message_error,
    }
    return render(request, 'home/stock/historical_data.html', context)


""" prediction"""
import pandas_datareader as pdr

import numpy as np
from sklearn.preprocessing import MinMaxScaler


def get_tesla_pred(request):
    df = pdr.DataReader('TSLA', data_source="yahoo", start="2018-05-01", end="2021-05-20")
    df.to_csv('TSLA.csv')
    df1 = df.reset_index()['Close']
    scaler = MinMaxScaler(feature_range=(0, 1))
    df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))
    ##splitting dataset into train and test split
    training_size = int(len(df1) * 0.75)
    test_size = len(df1) - training_size
    train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]
    return render(request, "home/predictions/tesla_pred.html")


@login_required
def get_news(request, symbol='AAPL'):
    url = f'https://api.polygon.io/v2/reference/news?limit=10&ticker={symbol}&apiKey={API_KEY}'
    if request.method == 'POST':
        symbol = request.GET.get('symbol')

        url = f'https://api.polygon.io/v2/reference/news?limit=10&ticker={symbol}&apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    results = data['results']

    context = {
        'results': results
    }
    return render(request, "home/news/breaking_news.html", context)


@login_required
def get_news_page(request, symbol):
    symbol.upper()
    url = f'https://api.polygon.io/v2/reference/news?limit=10&ticker={symbol}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    results = data['results']
    # print(results[0])

    context = {
        'symbol': symbol,
        'results': results
    }
    return render(request, "home/news/news_page.html", context)



def analysis_news(request):
    # create a newspaper object
    url = input('copy url here: ')

    my_article = Article(url, language="en")
    my_article.download()
    # print(my_article.html)
    my_article.parse()
    # extract the title
    print('Title :', my_article.title)
    # extract the authors
    print('authors :', my_article.authors)

    # NLP
    my_article.nlp()
    # Extract summary
    print('Summary', my_article.summary)
    # Extract keywords
    print('keywords :', my_article.keywords)

    analysis = TextBlob(my_article.text)
    print(analysis.polarity)
    print(f'Sentiment : {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

    return render(request, "home/news/analysis_news.html")


def get_apple_pred(request):
    return render(request, "home/predictions/apple_pred.html")


