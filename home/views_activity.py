from django.shortcuts import render, redirect
from .models import Transaction, Portfolio
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
import pandas as pd

from .plots import plot_stats, plot_stock_unindexed, plot_stats_transaction


@login_required
def add_transaction(request, pk_portfolio):
    error_transaction_message = None
    if request.method == 'POST':
        if request.POST:
            number_stocks = int(request.POST.get('number_stocks'))
            buying_price = float(request.POST.get('buying_price'))
            date_to_buy = request.POST.get('date_to_buy')
            date_to_buy = dt.strptime(date_to_buy, '%Y-%m-%d')
            print(date_to_buy)
            selling_price = float(request.POST.get('selling_price'))
            date_to_sell = request.POST.get('date_to_sell')
            date_to_sell = dt.strptime(date_to_sell, '%Y-%m-%d')
            print(date_to_sell)
            portfolio = request.user.portfolio_set.get(id=pk_portfolio)
            if buying_price <= 0 or selling_price <= 0 or number_stocks <= 0:
                error_transaction_message = 'All numbers must be positive'
                context = {
                    'error_activity_message': error_transaction_message,
                }
                return render(request, "home/portfolio_activity/add_activity.html", context)
            # if buying_price < 0:
            #     error_activity_message = 'buying price must be positive'
            #     context = {
            #         'error_activity_message' : error_activity_message,
            #     }
            #     return render(request, "home/portfolio_activity/add_activity.html", context)
            # if selling_price < 0:
            #     error_activity_message = 'selling price must be positive'
            #     context = {
            #         'error_activity_message' : error_activity_message,
            #     }
            #     return render(request, "home/portfolio_activity/add_activity.html", context)
            # try:
            #     print('checking date')
            #     year = date_activity.year
            #     month = date_activity.month
            #     day = date_activity.day
            #
            #     portfolio.activity_set.filter(date_activity)
            #     print('exists')
            #     error_message = 'the date was already chosen!!!'
            #     context = {
            #         'error_message': error_message,
            #     }
            #     return render(request, "home/portfolio_activity/add_activity.html", context)
            # except:
            #     pass
            Transaction.objects.get_or_create(
                portfolio=portfolio,
                number_stocks=number_stocks,
                buying_price=buying_price,
                date_to_buy=date_to_buy,
                selling_price=selling_price,
                date_to_sell=date_to_sell,
            )
            return redirect('home:show_list_activity', pk_portfolio)

    context = {
        'error_activity_message': error_transaction_message,
    }
    return render(request, "home/portfolio_activity/add_activity.html", context)


def get_list_transaction(request, pk):
    error_portfolio_message = None
    error_transaction_message = None
    portfolio = None
    total_stocks = 0
    total_buys = 0
    total_sales = 0
    gain = 0
    loss = 0
    gain_profit_percentage = 0
    loss_profit_percentage = 0
    data = []
    try:
        username = request.user
        portfolio = username.portfolio_set.get(id=pk)
    except:
        error_portfolio_message = 'you have no portfolio yet'

    list_transaction = portfolio.transaction_set.all()
    if len(list_transaction) == 0:
        error_transaction_message = 'you have no activity in this portfolio'
        context = {
            'error_portfolio_message': error_portfolio_message,
            'error_activity_message': error_transaction_message,
            'portfolio': portfolio,
            'list_activity': list_transaction,
        }
        return render(request, "home/portfolio_activity/list_activity.html", context)
    df_stats = pd.DataFrame(columns=['pk', 'id', 'number_stocks', 'buying_price', 'date_to_buy', 'selling_price', 'date_to_sell', 'profit', 'profit_percentage'])
    i = 0
    j = 0
    for transaction in list_transaction:
        j += 1
        total_buys += transaction.buying_price
        total_sales += transaction.selling_price
        total_stocks += transaction.number_stocks
        profits_transaction = transaction.selling_price - transaction.buying_price
        profit_percentage = round((profits_transaction / transaction.selling_price) * 100, 4)
        df_stats.loc[i] = [j, transaction.pk, transaction.number_stocks, transaction.buying_price, transaction.date_to_buy,
                           transaction.selling_price, transaction.date_to_sell, profits_transaction, profit_percentage]
        i += 1

    fig_div = plot_stats_transaction(df_stats)
    print(f'total_stocks = {total_stocks}')
    print(f'bought_prices = {total_buys}')
    print(f'total_sales = {total_sales}')
    for i in range(df_stats.shape[0]):
        temp = df_stats.iloc[i]
        data.append(dict(temp))
    average_stock_cost = round(total_buys / total_stocks, 4)
    average_stock_sale = round(total_sales / total_stocks, 4)
    # for activity in list_activity:
    #     profits += activity.selling_price - activity.buying_price
    profits = total_sales - total_buys
    print(f'profits = {profits}')
    if profits >= 0:
        gain = round(100 - (total_buys / total_sales) * 100, 4)
        gain_profit_percentage = round((gain / total_sales) * 100, 4)
    else:
        loss = round(100 - (total_buys / total_sales) * 100, 4)
        loss_profit_percentage = round((loss / total_sales) * 100, 4)

    context = {

        'total_stocks': total_stocks,
        'total_sales': total_sales,
        'total_buys': total_buys,
        'average_stock_cost': average_stock_cost,
        'average_stock_sale': average_stock_sale,
        'gain_profit_percentage': gain_profit_percentage,
        'loss_profit_percentage': loss_profit_percentage,
        'profits': profits,
        'gain': gain,
        'loss': loss,
        'error_portfolio_message': error_portfolio_message,
        'error_activity_message': error_transaction_message,
        'portfolio': portfolio,
        'list_activity': list_transaction,
        'data': data,
        'fig_div': fig_div,
    }
    return render(request, "home/portfolio_activity/list_activity.html", context)


@login_required
def edit_transaction(request, pk_portfolio, pk_transaction, id_transaction):
    portfolio = request.user.portfolio_set.get(id=pk_portfolio)
    transaction = portfolio.transaction_set.get(id=pk_transaction)
    if request.method == 'POST':
        if request.POST:
            number_stocks = request.POST.get('number_stocks')
            buying_price = request.POST.get('buying_price')
            date_to_buy = request.POST.get('date_to_buy')
            date_to_buy = dt.strptime(date_to_buy, '%Y-%m-%d')
            print(date_to_buy)
            selling_price = float(request.POST.get('selling_price'))
            date_to_sell = request.POST.get('date_to_sell')
            date_to_sell = dt.strptime(date_to_sell, '%Y-%m-%d')
            print(date_to_sell)
            if date_to_buy > date_to_sell or date_to_buy > dt.now() or date_to_sell > dt.now():
                error_transaction_message = 'Please check the dates you used'
                context = {
                    'error_activity_message': error_transaction_message,
                }
                return render(request, "home/portfolio_activity/add_activity.html", context)
            if float(buying_price) <= 0 or float(selling_price) <= 0 or float(number_stocks) <= 0:
                error_transaction_message = 'All numbers must be positive'
                context = {
                    'error_activity_message': error_transaction_message,
                }
                return render(request, "home/portfolio_activity/add_activity.html", context)
            # try:
            #     print('checking date')
            #     portfolio.activity_set.get(date_activity)
            #     print('exists')
            #     error_message = 'the date was already chosen!!!'
            #     context = {
            #         'error_message': error_message,
            #     }
            #     return render(request, "home/portfolio_activity/add_activity.html", context)
            # except:
            #     pass
            transaction.number_stocks = number_stocks
            transaction.buying_price = buying_price
            transaction.date_to_buy = date_to_buy
            transaction.selling_price = selling_price
            transaction.date_to_sell = date_to_sell
            transaction.save()
            return redirect('home:show_list_activity', pk_portfolio)

    context = {
        'activity': transaction,
        'id_transaction': id_transaction,
    }
    return render(request, "home/portfolio_activity/edit_activity.html", context)


@login_required
def delete_transaction(request, pk_portfolio, pk_transaction):
    portfolio = request.user.portfolio_set.get(id=pk_portfolio)
    transaction = portfolio.transaction_set.get(id=pk_transaction)
    transaction.delete()

    return redirect('home:show_list_activity', pk_portfolio)


@login_required
def get_all_transaction(request):
    error_portfolio_message = None
    error_transaction_message = None
    portfolio = None
    profits = 0
    profits_portfolio = 0
    profit_percentage = 0
    total_stocks = 0
    total_buys = 0
    total_sales = 0
    portfolio_stocks = 0
    portfolio_buys = 0
    portfolio_sales = 0
    average_stock_cost = 0
    average_stock_sale = 0
    gain = 0
    loss = 0
    gain_profit_percentage = 0
    loss_profit_percentage = 0
    portfolios_with_activities = 0
    data = []
    error_transaction_message = ''
    all_portfolio = request.user.portfolio_set.all()
    if len(all_portfolio) > 0:
        df_stats = pd.DataFrame(columns=['portfolio', 'portfolio_stock', 'total_stocks', 'total_buys', 'total_sales', 'profit', 'profit_percentage'])
        for portfolio in all_portfolio:

            all_transaction = portfolio.transaction_set.all()
            if len(all_transaction) > 0:
                # portfolio_sales = sum(all_transaction)
                for transaction in all_transaction:
                    # total_buys += activity.buying_price
                    # total_sales += activity.selling_price
                    # total_stocks += activity.number_stocks
                    portfolio_buys += transaction.buying_price
                    portfolio_sales += transaction.selling_price
                    portfolio_stocks += transaction.number_stocks
                    profits_portfolio = portfolio_sales - portfolio_buys
                    profit_percentage = round((profits_portfolio / portfolio_sales) * 100, 4)
                # portfolio_elements = []
                df_stats.loc[portfolios_with_activities] = [portfolio.name, portfolio.stock.symbol, portfolio_stocks, portfolio_buys,
                                                                             portfolio_sales, profits_portfolio, profit_percentage]
                portfolio_stocks = 0
                portfolio_buys = 0
                portfolio_sales = 0
                portfolios_with_activities += 1
        if portfolios_with_activities>0:
            for i in range(df_stats.shape[0]):
                temp = df_stats.iloc[i]
                data.append(dict(temp))
            # print('data\n', data)
            # print(df_stats)
            # print(sum(df_stats['total_buys']))

            total_buys += sum(df_stats['total_buys'])
            total_sales += sum(df_stats['total_sales'])
            total_stocks += sum(df_stats['total_stocks'])
            average_stock_cost = round(total_buys / total_stocks, 4)
            average_stock_sale = round(total_sales / total_stocks, 4)
            profits = total_sales - total_buys
            # print(f'profits = {profits}')
            fig1_div = plot_stats(df_stats)

            if profits >= 0:
                gain = round(100 - (total_buys / total_sales) * 100, 4)
                gain_profit_percentage = round((gain / total_sales) * 100, 4)
            else:
                loss = round(100 - (total_buys / total_sales) * 100, 4)
                loss_profit_percentage = round((loss / total_sales) * 100, 4)

            context = {

                'profits': profits,
                'total_stocks': total_stocks,
                'total_sales': total_sales,
                'total_buys': total_buys,
                'portfolios_with_activities': portfolios_with_activities,
                'fig1_div': fig1_div,
                'portfolios_len': len(all_portfolio),
                'average_stock_cost': average_stock_cost,
                'average_stock_sale': average_stock_sale,
                'gain_profit_percentage': gain_profit_percentage,
                'loss_profit_percentage': loss_profit_percentage,
                'gain': gain,
                'loss': loss,
                'error_portfolio_message': error_portfolio_message,
                'error_activity_message': error_transaction_message,
                'portfolio': portfolio,
                'data': data,
            }
            return render(request, "home/portfolio_activity/my_all_activity.html", context)
        else:
            error_transaction_message = 'you have no transaction in any portfolio of yours'
    else:
        error_transaction_message = 'you have no portfolio yet'
    context = {
        'error_activity_message': error_transaction_message,
    }
    return render(request, "home/portfolio_activity/my_all_activity.html", context)
