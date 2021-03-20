from django.shortcuts import render
from . import models
# from home.dash_apps import models
from .functions import *
from .models import Stock

api_key = '701005b908bc42b8800ca2fac03f2736'


# PlotlyGraph
def candlestick(ts_df):
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


def plotly(ts_df):
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


def plotly_slider(ts_df):
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

def compute_bollinger_bands(df, symbol, dtime, *args, **kwargs):
    plt.switch_backend("AGG")
    df_temp = df['High']
    ax = df_temp.plot(title=f'{symbol.upper()} rolling mean', label=f'{symbol.upper()}')

    if dtime == 30:
        # 1. Compute rolling mean
        rm_TSEC = get_rolling_mean(df_temp, window=3)

        # 2. Compute rolling standard deviation
        rstd_TSEC = get_rolling_std(df_temp, window=3)

    else:
        # 1. Compute rolling mean
        rm_TSEC = get_rolling_mean(df_temp, window=dtime // 36)

        # 2. Compute rolling standard deviation
        rstd_TSEC = get_rolling_std(df_temp, window=dtime // 36)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_TSEC, rstd_TSEC)

    rm_TSEC.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Adj')
    ax.legend(loc='upper left')
    graph = get_image()
    # df_temp['upper band'] = df_temp['High']
    figure1 = go.Figure(
        [
            go.Scatter(
                name='High',
                x=df.index,
                y=df['High'],
            ),
            go.Scatter(
                name='Rolling Mean',
                x=df.index,
                y=rm_TSEC,
            ),
            go.Scatter(
                name='upper band',
                x=df.index,
                y=upper_band,
            ),
            go.Scatter(
                name='lower band',
                x=df.index,
                y=lower_band,
            ),
        ]
    )

    compare_div1 = plot(figure1, output_type='div')

    daily_returns = compute_daily_returns(df)
    figure2 = go.Figure(
        [
            go.Scatter(
                x=daily_returns.index,
                y=daily_returns['High'],
                text='Daily Returns',
            )
        ]
    )

    figure2.update_layout(
        title=f"Daily return of {symbol}",
        xaxis_title="Days",
        yaxis_title="daily return",
    )
    figure2.update_xaxes(rangeslider_visible=True)
    compare_div2 = plot(figure2, output_type='div')
    df2 = pd.DataFrame()
    df2['Date'] = daily_returns.index.values
    df2['High'] = daily_returns['High'].values
    df2 = df2[1:]
    figure3 = px.area(df2, x='Date', y='High', title='Daily Returns', )
    figure3.update_xaxes(rangeslider_visible=True)
    compare_div3 = plot(figure3, output_type='div')
    return graph, compare_div1, compare_div2, compare_div3


def plot_buy_sell(data, symbol):
    fig = go.Figure(
        [
            go.Scatter(
                name='Buy',
                x=data.index,
                y=data['Buy_Signal_Price'],
                mode='markers',
                opacity=1,
                marker=dict(
                    color='LightGreen',
                    size=15,
                ),
                text='Buy',
            ),
            go.Scatter(
                name='Sell',
                x=data.index,
                y=data['Sell_Signal_Price'],
                mode='markers',
                marker=dict(
                    color='tomato',
                    size=15,
                ),
                text='Sell',
            ),
            go.Scatter(
                name=f'{symbol} Price',
                x=data.index,
                y=data['Close'],
                opacity=0.5,
                text=f'{symbol} Price',
                line=dict(
                    color='blue',
                    width=3
                )
            ),
        ]
    )
    fig.update_layout(
        title=f"{symbol} Buys & Sells",
        xaxis_title="Days",
    )
    fig.update_xaxes(rangeslider_visible=True)
    plotly_div = plot(fig, output_type='div')
    return plotly_div


def plot_macd_signal(data, symbol, MACD, signal):
    fig = go.Figure(
        [
            go.Scatter(
                name=f'{symbol} MACD',
                x=data.index,
                y=MACD,
                line=dict(
                    color='blue',
                    width=3,
                ),
            ),
            go.Scatter(
                name=f'{symbol} signal',
                x=data.index,
                y=signal,
                line=dict(
                    color='tomato',
                    width=3,
                ),
            ),
        ]
    )
    fig.update_xaxes(rangeslider_visible=True)
    plotly_div = plot(fig, output_type='div')
    return plotly_div


# def get_stock(request, symbol='AAPL'):
#     stocks = Stock.objects.all()
#     print(request.path)
#     # print(request.get_full_path)
#     # allData = []
#     # print(stock_data)
#     # for i in range(stock_data.shape[0]):
#     #     temp = stock_data.iloc[i]
#     #     allData.append(dict(temp))
#     context = {
#         'stocks': stocks,
#         'symbol': symbol,
#         # 'stock_data': stock_data,
#     }
#     # print(stock_data)
#     return render(request, "home/table_stock.html", context)
