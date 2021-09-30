####################################################################################################################
# Yahoo scraping
####################################################################################################################
import re
from bs4 import BeautifulSoup
import json
import datetime as dt
import requests

import yfinance as yf

token = 'pk_2287fdfeab07481297cac422c06f9dc6'

def scrape_yahoo_numbered_data(some_list, dtype):
    list_smts = []
    for s in some_list:
        statement = {}
        for key, val in s.items():
            try:
                statement[key] = val[dtype]
            except TypeError:
                continue
            except KeyError:
                continue
        list_smts.append(statement)
    return list_smts


def scrape_yahoo_dict_data(some_dict, dtype):
    statement = {}
    for key, val in some_dict.items():
        try:
            statement[key] = val[dtype]
        except TypeError:
            continue
        except KeyError:
            continue
    print(statement)
    return statement


def load_url_financials(stock):
    url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'
    response = requests.get(url_financials.format(stock, stock))
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    # print(pattern)
    script_data = soup.find('script', text=pattern).contents[0]
    start = script_data.find('context') - 2
    json_data = json.loads(script_data[start: -12])
    return json_data


def load_url_profiles(stock):
    url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
    response = requests.get(url_profile.format(stock, stock))
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    print(soup.find('script', text=pattern))

    script_data = soup.find('script', text=pattern).contents[0]
    start = script_data.find('context') - 2
    json_data = json.loads(script_data[start: -12])
    return json_data


def get_stock_quote(ticker_symbol, api):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    for i in response:
        try:
            response[i] = float(response[i])

        except Exception:
            pass
        if isinstance(response[i], float):
            response[i] = round(response[i], 3)
    return response



# def load_yahoo_financials(json_data_financials, dtype='raw'):
#     annual_is = json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory'][
#         'incomeStatementHistory']
#     quarterly_is = \
#     json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly'][
#         'incomeStatementHistory']
#
#     annual_cf = \
#     json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory'][
#         'cashflowStatements']
#     quarterly_cf = \
#     json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly'][
#         'cashflowStatements']
#
#     annual_bs = json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory'][
#         'balanceSheetStatements']
#     quarterly_bs = \
#     json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly'][
#         'balanceSheetStatements']
#
#     statements = {
#         'annual_income_statements': annual_is,
#         'quarterly_income_statements': quarterly_is,
#         'annual_cash_flow': annual_cf,
#         'quarterly_cash_flow': quarterly_cf,
#         'annual_balance_sheet': annual_bs,
#         'quarterly_balance_sheet': quarterly_bs,
#     }
#
#     for key, val in statements.items():
#         statements[key] = scrape_yahoo_numbered_data(val, dtype)
#
#     return statements


def load_yahoo_annual_income_statement(json_data_financials, dtype='raw'):
    annual_is = json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory'][
        'incomeStatementHistory']
    annual_income_statement = scrape_yahoo_numbered_data(annual_is, dtype)
    print(annual_income_statement)
    return annual_income_statement


def load_yahoo_annual_cash_flow(json_data_financials, dtype='raw'):
    annual_cf = \
        json_data_financials['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory'][
            'cashflowStatements']
    annual_cash_flow = scrape_yahoo_numbered_data(annual_cf, dtype)
    print(annual_cash_flow)
    return annual_cash_flow


def load_yahoo_annual_balance_sheet(json_data_balance_sheet, dtype='raw'):
    annual_bs = \
        json_data_balance_sheet['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory'][
            'balanceSheetStatements']
    annual_balance_sheet = scrape_yahoo_numbered_data(annual_bs, dtype)
    print(annual_balance_sheet[0])
    return annual_balance_sheet


def quote_type_yahoo(json_data_quote):
    json_quote = json_data_quote['context']['dispatcher']['stores']['QuoteSummaryStore']['quoteType']
    print(json_quote)
    return json_quote


def stock_price_yahoo(json_data_price):
    json_price = json_data_price['context']['dispatcher']['stores']['QuoteSummaryStore']['price']
    print(json_price)
    return json_price


def load_data_yfinance(ticker):
    today = dt.datetime.now()
    start = today - dt.timedelta(800)
    data = yf.download(ticker, start, today)
    data.reset_index(inplace=True)
    return data