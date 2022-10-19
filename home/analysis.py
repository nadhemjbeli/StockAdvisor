import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from yahoo_fin.stock_info import get_data as gd

# import plotly.graph_objects as go
# from plotly.offline import plot
# from alpha_vantage.techindicators import TechIndicators
# from alpha_vantage.timeseries import TimeSeries
import datetime as dt
import requests
from io import BytesIO
import base64

token = 'pk_2287fdfeab07481297cac422c06f9dc6 '


def compute_daily_returns(df, use_pandas=True):
    if not use_pandas:
        # Note: Returned DataFrame must have the same number of rows
        daily_returns = df.copy()  # copy given DataFrame to match size and column names
        # Compute daily returns for row 1 onwards
        # df[1:] picks all the rows from 1 till the end
        # df[:-1] picks all the row from 0 till 1 less than the end
        daily_returns[1:] = (df[1:] / df[:-1].values) - 1
        daily_returns.ix[0, :] = 0  # set daily returns for row 0 to 0
    else:
        df = df.drop(columns='Date')

        daily_returns = (df / df.shift(1)) - 1
    return daily_returns


def get_image():
    # create a bytes buffer for the image to save
    buffer = BytesIO()
    # create the plot with th use of BytesIO object as its 'file'
    plt.savefig(buffer, format='png')
    # set the cursor the begining of the stream
    buffer.seek(0)
    # retreive the entire content of the 'file'
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    # free the memory of the buffer
    buffer.close()

    return graph


def get_rolling_mean(values, window):
    return pd.Series.rolling(values, window=window).mean()


def get_rolling_std(values, window):
    return pd.Series.rolling(values, window=window).std()


def get_bollinger_bands(rm, rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def get_data(symbol, dtime=365):
    start = dt.datetime.now() - dt.timedelta(dtime)
    now = dt.datetime.now()
    # data = pdr.DataReader(symbol, 'yahoo', start, now)
    # data = yf.download(symbol, start, now)
    data = gd(symbol, start, now)
    df = pd.DataFrame(data)
    df_final = pd.DataFrame()
    df['Date'] = df.index.values
    df_final['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    # TODO: yf
    # df_final['Open'] = df['Open']
    # df_final['High'] = df['High']
    # df_final['Low'] = df['Low']
    # df_final['Close'] = df['Close']
    # df_final['Volume'] = df['Volume']
    # df = df.rename({'Adj Close': 'Adj'}, axis=1)
    # df_final['Adj'] = df.Adj
    # TODO: yahoo_fin.stock_info.get_data
    df_final['Open'] = df['open']
    df_final['High'] = df['high']
    df_final['Low'] = df['low']
    df_final['Close'] = df['close']
    df_final['Volume'] = df['volume']
    df_final['Adj'] = df.adjclose

    return df_final


def normalize_data(df):
    return df / df.iloc[0, :]


def get_data_user_symbols(symbols, dtime=365, normalize=False):
    # Create an empty dateframe
    # df = pd.DataFrame(index=dates)
    now = dt.datetime.now()
    start = now - dt.timedelta(dtime)
    now = now.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    dates = pd.date_range(start, now)
    # if 'TPE-TSEC' not in symbols:
    #     symbols.insert(0, 'TPE-TSEC')
    df = pd.DataFrame(index=dates)
    # df = df['Date'].dt.strftime('%Y-%m-%d')

    for symbol in symbols:
        df_temp = get_data(symbol)
        df_temp = df_temp[['Adj']]
        print(symbol, len(df_temp))

        # Rename to prevent clash
        df_temp = df_temp.rename(columns={'Adj': symbol})
        df = df.join(df_temp)
    df = df.dropna(how='all')
    if normalize:
        df = normalize_data(df)
    return df


def get_macd_signal(data, dtime):
    # Calculate the MACD and signal indicators
    # Calculate the sort term exponential moving average (EMA)
    ShortEMA = data.Close.ewm(span=12, adjust=False).mean()
    # Calculate the long term exponential moving average (EMA)
    LongEMA = data.Close.ewm(span=26, adjust=False).mean()
    # Calculate the MACD line
    MACD = ShortEMA - LongEMA
    # Calculate the signal line
    signal = MACD.ewm(span=2, adjust=False).mean()
    return MACD, signal


# Create a function to signal when to buy and sell an asset
def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] < signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] > signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    return (Buy, Sell)





