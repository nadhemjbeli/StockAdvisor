from django.shortcuts import render
from . import models
# from home.dash_apps import models
from .analysis import get_rolling_mean, get_rolling_std, get_bollinger_bands, compute_daily_returns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot
import datetime as dt
import plotly.express as px

api_key = '701005b908bc42b8800ca2fac03f2736'


# PlotlyGraph
def candlestick(ts_df):
    dt_all = pd.date_range(start=ts_df.index[0], end=ts_df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in ts_df.index]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
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

    figure.update_xaxes(
        rangebreaks=[dict(values=dt_breaks)]  # hide dates with no values
    )

    figure.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                # dict(count=1, label="day", step="day", stepmode="todate"),
                dict(count=1, label="this month", step="month", stepmode="todate"),
                dict(count=31, label="1 month", step="day", stepmode="todate"),
                dict(count=1, label="this year", step="year", stepmode="todate"),
                dict(step="all")
            ])
        ))
    candlestick_div = plot(figure, output_type='div')
    return candlestick_div


def choose_color_area_1_day(df):
    start = df['close'][0]
    print('start ', start)
    end = df['close'][-1]
    print('end ', end)
    if end > start:
        figure = go.Figure(
            data=[
                go.Scatter(
                    x=df.index,
                    y=df['close'],
                    line=dict(
                        color='green',
                        width=5
                    )
                )
            ]
        )
    else:
        # figure = px.line(df, x=df.index, y='close')
        # figure.update_layout(plot_bgcolor='white')
        figure = go.Figure(
                data=[
                    go.Scatter(
                        x=df.index,
                        y=df['close'],
                        line=dict(
                            color='tomato',
                            width=8
                        )
                    )
                ]
            )
    return figure


def area_plot_1_day(symbol):
    # from twelvedata import TDClient
    link = 'https://cloud.iexapis.com/stable/stock/{]/chart/date/20210528?token={}'
    from iexfinance.stocks import get_historical_intraday
    token = 'pk_b4d054d6cd7640a38df80d61172890b3'
    # if dt.datetime.now().hour == 9:
    #     if dt.datetime.now().minute >30:
    #         start = dt.datetime.now()
    #     else:
    #         start = dt.datetime.now() - dt.timedelta(1)
    # elif dt.datetime.now().hour > 9:
    #     start = dt.datetime.now() - dt.timedelta(4)
    # else:
    #     start = dt.datetime.now() - dt.timedelta(1)
    start = dt.datetime.now()
    start_date = start.replace(hour=9, minute=30, second=0, microsecond=0)
    print(start_date)
    end_date = start.replace(hour=16, minute=0, second=0, microsecond=0)
    # Initialize client - apikey parameter is requiered
    # api_key = '701005b908bc42b8800ca2fac03f2736'
    df = get_historical_intraday(symbol, ouput_format='pandas', token=token, start=start_date, end=end_date)
    print("df: ", df)
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in df.index]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    # figure = px.area(x=df.index, y=df['close'])
    figure = choose_color_area_1_day(df)
    print(dt_breaks)
    figure.update_xaxes(
        rangebreaks=[dict(values=dt_breaks)]  # hide dates with no values
    )
    area_div = plot(figure, output_type='div')
    return area_div


def area_plot_1_day_candlestick(symbol):
    # from twelvedata import TDClient
    from iexfinance.stocks import get_historical_intraday
    token = 'pk_b4d054d6cd7640a38df80d61172890b3'
    if dt.datetime.now().hour == 9:
        if dt.datetime.now().minute >30:
            start = dt.datetime.now()
        else:
            start = dt.datetime.now() - dt.timedelta(1)
    elif dt.datetime.now().hour > 9:
        start = dt.datetime.now()
    else:
        start = dt.datetime.now() - dt.timedelta(1)
    # start=dt.datetime(2020, 12, 12)
    start_date = start.replace(hour=9, minute=30, second=0, microsecond=0)
    print(start_date)
    end_date = start.replace(hour=16, minute=0, second=0, microsecond=0)
    # Initialize client - apikey parameter is requiered
    # api_key = '701005b908bc42b8800ca2fac03f2736'
    df = get_historical_intraday(symbol, ouput_format='pandas', token=token, start=start_date, end=end_date)
    print(df)
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    # print(dt_all)
    dt_obs = [d.strftime("%Y-%m-%d") for d in df.index]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    figure = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                high=df['high'],
                low=df['low'],
                open=df['open'],
                close=df['close'],
            )
        ]
    )
    figure.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                # dict(count=1, label="day", step="day", stepmode="todate"),
                dict(count=30, label="last half hour", step="minute", stepmode="todate"),
                dict(count=1, label="last hour", step="hour", stepmode="todate"),
                dict(count=4, label="last 4 hours", step="hour", stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangebreaks=[dict(values=dt_breaks)],  # hide dates with no values
    )
    area_div = plot(figure, output_type='div')
    return area_div
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


def compare_stock(df):
    fig = px.line(df, x=df.index, y=df.columns,
                  title='Compare your chosen stocks')
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
        rm_TSEC = get_rolling_mean(df_temp, window=int(dtime // (dtime*0.1)))

        # 2. Compute rolling standard deviation
        rstd_TSEC = get_rolling_std(df_temp, window=int(dtime // (dtime*0.1)))

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_TSEC, rstd_TSEC)

    rm_TSEC.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Adj')
    ax.legend(loc='upper left')
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

    figure1.update_layout(
        title=f"{symbol} bollinger Bands",
        xaxis_title="Days",
        yaxis_title="bollinger Bands",
    )
    div_bollinger = plot(figure1, output_type='div')

    daily_returns = compute_daily_returns(df)
    # figure2 = go.Figure(
    #     [
    #         go.Scatter(
    #             x=daily_returns.index,
    #             y=daily_returns['High'],
    #             text='Daily Returns',
    #         )
    #     ]
    # )

    # figure2.update_layout(
    #     title=f"Daily return of {symbol}",
    #     xaxis_title="Days",
    #     yaxis_title="daily return",
    # )
    # figure2.update_xaxes(rangeslider_visible=True)
    # compare_div2 = plot(figure2, output_type='div')
    df2 = pd.DataFrame()
    df2['Date'] = daily_returns.index.values
    df2['High'] = daily_returns['High'].values
    df2 = df2[1:]
    figure3 = px.area(df2, x='Date', y='High', title=f'Daily Returns of {symbol}', )
    figure3.update_xaxes(rangeslider_visible=True)
    div_daily_returns = plot(figure3, output_type='div')
    # return compare_div1, compare_div2, compare_div3
    return div_bollinger, div_daily_returns


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

def plot_prediction(forecast, df_train , period):
    forecast = forecast.set_index('ds')
    df = df_train.set_index('ds')
    df_pred = forecast[-period:]
    dt_all = pd.date_range(start=forecast.index[0], end=forecast.index[-1])
    dt_obs = [d for d in forecast.index.strftime("%Y-%m-%d")]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    # Create traces
    fig = go.Figure([go.Scatter(x=forecast.index, y=forecast['yhat_upper'],
                                mode='lines',
                                line=dict(width=0.01, color='gray'),
                                showlegend=False,
                                name='prediction'),
                     go.Scatter(x=forecast.index, y=forecast['yhat_lower'],
                                mode='lines',
                                line=dict(width=0.01, color='gray'),
                                fill='tonexty',
                                showlegend=False,
                                name='prediction')])
    fig.add_trace(go.Scatter(x=df_pred.index, y=df_pred['yhat'],
                             mode='lines',
                             line=dict(width=2, color='tomato'),
                             name='future predicted'))
    fig.add_trace(go.Scatter(x=df.index, y=df['y'],
                             mode='lines',
                             line=dict(width=3, color='blue'),
                             name='actual'))
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                # dict(count=1, label="day", step="day", stepmode="todate"),
                dict(count=6, label="6m", step="month", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="todate"),
                dict(count=2, label="2y", step="year", stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangebreaks=[dict(values=dt_breaks)],  # hide dates with no values
    )
    pred_div = plot(fig, output_type='div')
    return pred_div

def plot_stats(df):
    fig1 = go.Figure(data=[
        go.Bar(name='total buys', x=df['portfolio'], y=df['total_buys']),
        go.Bar(name='total sales', x=df['portfolio'], y=df['total_sales'])
    ])
    # Change the bar mode
    fig1.update_layout(barmode='group')
    fig1_div = plot(fig1, output_type='div')
    return fig1_div