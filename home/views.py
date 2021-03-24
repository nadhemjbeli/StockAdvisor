from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from .plots import *
from .dash_apps.finished_apps.simpleexample import *
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


def get_income_statements(request, symbol):
    stocks = Stock.objects.get(symbol=symbol)
    json_data = load_url_financials(symbol)
    print('fmtlong')
    annual_income_statement_longfmt = load_yahoo_annual_income_statement(json_data, 'longFmt')
    print('fmt')
    annual_income_statement_fmt = load_yahoo_annual_income_statement(json_data, 'fmt')
    # print(financials_fmt['annual_income_statements'])
    # financials_raw = load_yahoo_financials(symbol, 'raw')
    context = {
        'stocks': stocks,
        # 'financials_raw': financials_raw,
        'annual_income_statement_fmt': annual_income_statement_fmt,
        'annual_income_statement_longfmt': annual_income_statement_longfmt,
        'symbol': symbol,

    }

    return render(request, 'home/income_statements.html', context)


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
        'symbol': symbol,
        'stock': stock,
        'graph_plotly1': graph_plotly1,
        'graph_plotly2': graph_plotly2,
        'graph_plotly3': graph_plotly3,
        "plot_macd": plot_macd,
        'p_b_s': p_b_s,
    }
    return render(request, 'home/stock_analysis.html', context)


def get_stock_summary(request, symbol):
    get_live_update(symbol)
    area_1_day = area_plot_1_day(symbol)
    context = {
        'area_1_day': area_1_day,
        'symbol': symbol,
    }
    return render(request, 'home/stock/summary.html', context)

