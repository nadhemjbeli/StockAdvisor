from django.shortcuts import render, redirect
from .models import Activity, Portfolio
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt

@login_required
def add_activity(request, pk_portfolio):
    error_activity_message = None
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
                error_activity_message = 'All numbers must be positive'
                context = {
                    'error_activity_message' : error_activity_message,
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
            Activity.objects.get_or_create(
                portfolio=portfolio,
                number_stocks=number_stocks,
                buying_price=buying_price,
                date_to_buy=date_to_buy,
                selling_price=selling_price,
                date_to_sell=date_to_sell,
            )
            return redirect('home:show_list_activity', pk_portfolio)

    context = {
        'error_activity_message' : error_activity_message,
    }
    return render(request, "home/portfolio_activity/add_activity.html", context)


def get_list_activity(request, pk):
    error_portfolio_message = None
    error_activity_message = None
    portfolio = None
    total_stocks = 0
    total_buys = 0
    total_sales = 0
    gain = 0
    loss = 0
    gain_profit_percentage = 0
    loss_profit_percentage = 0
    try:
        username = request.user
        portfolio = username.portfolio_set.get(id=pk)
    except:
        error_portfolio_message = 'you have no portfolio yet'

    list_activity = portfolio.activity_set.all()
    if len(list_activity) == 0:
        error_activity_message = 'you have no activity in this portfolio'
        print(error_activity_message)
        context = {
            'error_portfolio_message': error_portfolio_message,
            'error_activity_message': error_activity_message,
            'portfolio': portfolio,
            'list_activity': list_activity,
        }
        return render(request, "home/portfolio_activity/list_activity.html", context)
    for activity in list_activity:
        total_buys += activity.buying_price
        total_sales += activity.selling_price
        total_stocks += activity.number_stocks
    print(f'total_stocks = {total_stocks}')
    print(f'bought_prices = {total_buys}')
    print(f'total_sales = {total_sales}')
    average_stock_cost = round(total_buys/total_stocks, 4)
    average_stock_sale = round(total_sales/total_stocks, 4)
    # for activity in list_activity:
    #     profits += activity.selling_price - activity.buying_price
    profits = total_sales - total_buys
    print(f'profits = {profits}')
    if profits >= 0:
        gain = round(100 - (total_buys / total_sales)*100, 4)
        gain_profit_percentage = round((gain / total_sales)*100, 4)
    else:
        loss = round(100 - (total_buys / total_sales)*100, 4)
        loss_profit_percentage = round((loss / total_sales)*100, 4)

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
        'error_activity_message': error_activity_message,
        'portfolio': portfolio,
        'list_activity': list_activity,
    }
    return render(request, "home/portfolio_activity/list_activity.html", context)


@login_required
def edit_activity(request, pk_portfolio, pk_activity):
    portfolio = request.user.portfolio_set.get(id=pk_portfolio)
    activity = portfolio.activity_set.get(id=pk_activity)
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
                error_activity_message = 'Please check the dates you used'
                context = {
                    'error_activity_message' : error_activity_message,
                }
                return render(request, "home/portfolio_activity/add_activity.html", context)
            if buying_price <= 0 or selling_price <= 0 or number_stocks <= 0:
                error_activity_message = 'All numbers must be positive'
                context = {
                    'error_activity_message' : error_activity_message,
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
            activity.number_stocks = number_stocks
            activity.buying_price = buying_price
            activity.date_to_buy = date_to_buy
            activity.selling_price = selling_price
            activity.date_to_sell = date_to_sell
            activity.save()
            return redirect('home:show_list_activity', pk_portfolio)

    context = {
        'activity': activity,
    }
    return render(request, "home/portfolio_activity/edit_activity.html", context)

@login_required
def delete_activity(request, pk_portfolio, pk_activity):
    portfolio = request.user.portfolio_set.get(id=pk_portfolio)
    activity = portfolio.activity_set.get(id=pk_activity)
    activity.delete()

    return redirect('home:show_list_activity', pk_portfolio)
@login_required
def get_all_activity(request):
    error_portfolio_message = None
    error_activity_message = None
    portfolio = None
    profits = 0
    total_stocks = 0
    total_buys = 0
    average_stock_cost = 0
    average_stock_sale = 0
    total_sales = 0
    gain = 0
    loss = 0
    gain_profit_percentage = 0
    loss_profit_percentage = 0
    portfolios_with_activities = 0
    list_symbols = []
    all_portfolio = request.user.portfolio_set.all()
    if len(all_portfolio)>0:
        list_symbols = []
        for portfolio in all_portfolio:
            all_activity = portfolio.activity_set.all()
            if len(all_activity)>0:
                for activity in all_activity:
                    total_buys += activity.buying_price
                    total_sales += activity.selling_price
                    total_stocks += activity.number_stocks
                portfolios_with_activities += 1

        average_stock_cost = round(total_buys/total_stocks, 4)
        average_stock_sale = round(total_sales/total_stocks, 4)
        profits = total_sales - total_buys
        print(f'profits = {profits}')

        if profits >= 0:
            gain = round(100 - (total_buys / total_sales)*100, 4)
            gain_profit_percentage = round((gain / total_sales)*100, 4)
        else:
            loss = round(100 - (total_buys / total_sales)*100, 4)
            loss_profit_percentage = round((loss / total_sales)*100, 4)
    print(list_symbols)
    context = {

        'profits': profits,
        'total_stocks': total_stocks,
        'total_sales': total_sales,
        'total_buys': total_buys,
        'portfolios_with_activities': portfolios_with_activities,
        'portfolios_len': len(all_portfolio),
        'average_stock_cost': average_stock_cost,
        'average_stock_sale': average_stock_sale,
        'gain_profit_percentage': gain_profit_percentage,
        'loss_profit_percentage': loss_profit_percentage,
        'gain': gain,
        'loss': loss,
        'error_portfolio_message': error_portfolio_message,
        'error_activity_message': error_activity_message,
        'portfolio': portfolio,
    }
    return render(request, "home/portfolio_activity/my_all_activity.html", context)