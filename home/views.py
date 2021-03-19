
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from .plots import *
# Create your views here.
symbol = 'AAPL'
def home(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context ={
        'plot1': scatter()
    }

    return render(request, 'home/welcome.html', context)


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

    token = 'Tpk_b1ce81ac4db5431c97ffe71615ee3689'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={token}'
    # api_url = f'https://sandbox.iexapis.com/stable/stock/aapl/quote?token={token}'
    data = requests.get(api_url).json()
    data['changePercent'] = round(data['changePercent'], 3)
    print(f'data:\n{data}')
    stock_data = get_stock_quote(symbol, api_key)
    print(f'stock_data:\n{stock_data}')
    models.Stock.objects.get_or_create(symbol=symbol, name=stock_data['name'], currency=stock_data['currency'])
    context = {
        'symbol': symbol,
        # 'moredata': moredata,
        # 'eth': eth,
        # 'btc': btc,
        # 'ltc': ltc,
        # 'percentchange': percentchange,
        # 'buyers': buyers,
        # 'sellers': sellers,
        'stock_data': stock_data,
        'data': data,
        'candlestick': candlestick(ts_df),
        'plotly': plotly(ts_df),
        'plotly_slider': plotly_slider(ts_df),
        'compare_stock': compare_stock(),
        'message_error': message_error,
    }
    return render(request, 'home/stock.html', context)


def single_stock(request, symbol):
    message_error = None
    stock = Stock.objects.get(symbol=symbol)
    print(stock)
    from pandas_datareader._utils import RemoteDataError
    try:
        ts_df = get_data(symbol)
    except (RemoteDataError, KeyError):
        message_error = 'isn\'t a stock symbol'
        return render(request, 'home/stock.html', {'message_error': message_error, 'symbol': symbol, })

    # PlotlyGraph
    def candlestick():
        figure = go.Figure(
            data=[
                go.Candlestick(
                    x=ts_df.index,
                    high=ts_df['High'],
                    low=ts_df['Low'],
                    open=ts_df['Open'],
                    close=ts_df['Close'],
                )
            ]
        )

        candlestick_div = plot(figure, output_type='div')
        return candlestick_div

    def plotly():
        figure = go.Figure(
            [
                go.Scatter(
                    x=ts_df.index,
                    y=ts_df['High'],
                )
            ]
        )

        plotly_div = plot(figure, output_type='div')
        return plotly_div

    def plotly_slider():
        fig = px.line(ts_df, x='Date', y='High', title='Time Series with Rangeslider')
        fig.update_xaxes(rangeslider_visible=True)
        plotly_div = plot(fig, output_type='div')
        return plotly_div

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

    token = 'Tpk_b1ce81ac4db5431c97ffe71615ee3689'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={token}'
    data = requests.get(api_url).json()
    print(f'data:\n{data}')
    data['changePercent'] = round(data['changePercent'], 3)
    stock_data = get_stock_quote(symbol, api_key)
    print(f'stock_data:\n{stock_data}')
    models.Stock.objects.get_or_create(symbol=symbol, name=stock_data['name'], currency=stock_data['currency'])
    context = {
        'symbol': symbol,
        'stock_data': stock_data,
        'data': data,
        'candlestick': candlestick(),
        'plotly': plotly(),
        'plotly_slider': plotly_slider(),
        'compare_stock': compare_stock(),
        'message_error': message_error,
    }
    return render(request, 'home/stock.html', context)


def stockAnalysis(request, symbol, dtime):
    stock = Stock.objects.get(symbol=symbol)
    df = get_data(symbol, dtime)
    graph, graph_plotly1, graph_plotly2, graph_plotly3 = compute_bollinger_bands(df, symbol, dtime)
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
        'stock': stock,
        'graph_plotly1': graph_plotly1,
        'graph_plotly2': graph_plotly2,
        'graph_plotly3': graph_plotly3,
        "plot_macd": plot_macd,
        'p_b_s': p_b_s,
    }
    return render(request, 'home/stock_analysis.html', context)
