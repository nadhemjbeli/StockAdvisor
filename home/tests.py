# from django.test import TestCase
# from datetime import date
import datetime as dt
import pandas_datareader as pdr
# import yfinance as yf
# from fbophet import Prophet
# from fbprophet.plot import plot_plotly
# from plotly import graph_objs as go
# # Create your tests here.
# from sklearn.tree import DecisionTreeRegressor
# import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.optimize as spo
# from .functions import get_data as get_d
#
# START = "2018-01-01"
# TODAY = date.today().strftime("%Y-%m-%d")
# stock = 'GOOG'
#
#
# def load_data(ticker):
#     data = yf.download(ticker, START, TODAY)
#     data.reset_index(inplace=True)
#     return data
#
#
# data = load_data(stock)
#
#
# # Plot raw data
# def plot_raw_data(data):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
#     fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
#     fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
#     fig.show()
#
#
# # Predict forecast with Prophet.
# df_train = data[['Date', 'Close']]
# df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
#
# period=300
#
# m = Prophet()
# m.fit(df_train)
# future = m.make_future_dataframe(periods=period)
# forecast = m.predict(future)
#
# fig1 = plot_plotly(m, forecast)
# fig1.show()
#
# def get_data(symbol, dtime=365):
#     now = dt.datetime.now()
#     start = now - dt.timedelta(dtime)
#     now = now.strftime('%Y-%m-%d')
#     start = start.strftime('%Y-%m-%d')
#     dates = pd.date_range(start, now)
#     data = pdr.DataReader(symbol, 'yahoo', start, now)
#     df = pd.DataFrame(data, index=dates)
#     df_final = pd.DataFrame()
#     df['Date'] = df.index.values
#     df_final['Date'] = df['Date']
#
#     df_final['Open'] = df['Open']
#     df_final['High'] = df['High']
#     df_final['Low'] = df['Low']
#     df_final['Close'] = df['Close']
#     df_final['Volume'] = df['Volume']
#
#     df = df.rename({'Adj Close': 'Adj'}, axis=1)
#     df_final['Adj'] = df.Adj
#     return df_final
#
#
# def get_data_user_symbols(symbols, dtime):
#     # Create an empty dateframe
#     # df = pd.DataFrame(index=dates)
#     now = dt.datetime.now()
#     start = now - dt.timedelta(dtime)
#     now = now.strftime('%Y-%m-%d')
#     start = start.strftime('%Y-%m-%d')
#     dates = pd.date_range(start, now)
#     # if 'TPE-TSEC' not in symbols:
#     #     symbols.insert(0, 'TPE-TSEC')
#     df = pd.DataFrame(index=dates)
#     # df = df['Date'].dt.strftime('%Y-%m-%d')
#
#     for symbol in symbols:
#         df_temp = get_data(symbol)
#         df_temp = df_temp[['Adj']]
#         print(df_temp)
#
#
#         # Rename to prevent clash
#         df_temp = df_temp.rename(columns={'Adj': symbol})
#         # Join two dataframes using DataFrame.join()
#         # if the value of the 'how' argument is assigned, then we don't use dropna()
#         # because it does the same thing
#         # Two ways to get the data frame
#         # [1] data intersection
#         df = df.join(df_temp)
#         # if symbol == 'TPE-TSEC':
#         #     df = df.dropna(subset=["TPE-TSEC"])
#         # [2] data intersection
#         # df = df.join(df_temp, how='inner')  # use default how='left', use how='inner' to join by intersection
#     print(np.shape(df))
#     df = df.dropna(how='all')
#     print(np.shape(df))
#
#     return df
#
# symbols = ['AAPL', 'GOOG']
# def get_user_symbols(request):
#     list_symbols = []
#     list_portfolio = request.user.portfolio_set.all().order_by('name')
#     if len(list_portfolio):
#         for portolio in list_portfolio:
#             list_symbols = list_symbols.append(portolio.symbol)
#     return list_symbols
# # df = get_data_user_symbols(symbols, 365)
# # print(df[:10])
# import plotly.express as px
# df = px.data.stocks()
# print(df)


# import pystan
# model_code = 'parameters {real y;} model {y ~ normal(0,1);}'
# model = pystan.StanModel(model_code=model_code)  # this will take a minute
# y = model.sampling(n_jobs=1).extract()['y']
# y.mean()  # should be close to 0

# from fbprophet import Prophet
# m = Prophet()
# m.fit(df)  # df is a pandas.DataFrame with 'y' and 'ds' columns
# future = m.make_future_dataframe(periods=365)
# m.predict(future)

