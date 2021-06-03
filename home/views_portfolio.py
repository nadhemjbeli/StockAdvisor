from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from.functions import get_data_user_symbols
from django.contrib.auth.decorators import login_required

from .plots import compare_stock


@login_required
def set_portfolio(request):
    stocks = Stock.objects.all().order_by('name')
    name = None
    list_portfolio = request.user.portfolio_set.all()
    username = request.user
    print(username)
    portfolio_num = len(list_portfolio)+1
    portfolio_len = len(list_portfolio)
    if portfolio_len >= 5:
        full_length_message = f'sorry, you can\'t create more than {portfolio_len} portfolios '
        context = {
            'full_length_message': full_length_message,
            'name': name,
        }
        return render(request, "home/portfolio/create_portfolio.html", context)
    if request.method == 'POST':
        if request.POST:
            name = request.POST.get('name')
            pk = request.POST.get('symbol')
            stock_rel = Stock.objects.get(id=pk)
            print(stock_rel)
            try:
                print('getting portfolio name')
                request.user.portfolio_set.get(name=name)
                error_message = 'Exists already!!!'
                print(error_message)
                context = {
                    'error_message': error_message,
                    'portfolio_num': portfolio_num,
                    'name': name,
                    'list_portfolio': list_portfolio,
                    'stocks': stocks,
                }
                return render(request, "home/portfolio/create_portfolio.html", context)
            except:
                pass
            Portfolio.objects.get_or_create(
                name=name,
                stock=stock_rel,
                user=username
            )
            return redirect('home:show_list_portfolio')

    context = {
        'portfolio_num': portfolio_num,
        'list_portfolio': list_portfolio,
        'name': name,
        'stocks': stocks,
    }
    return render(request, "home/portfolio/create_portfolio.html", context)


@login_required
def get_list_portfolio(request):
    error_message = None
    list_portfolio = None
    list_symbols = []
    try:
        username = request.user
        list_portfolio = username.portfolio_set.all().order_by('name')
        if len(list_portfolio):
            for portfolio in list_portfolio:
                list_symbols.append(portfolio.stock.symbol)
            df_compare = get_data_user_symbols(list_symbols, normalize=True)
            # print(df_compare)
            print(df_compare)
    except:
        error_message = 'you have no portfolio yet'
    print(list_symbols)
    context = {
        'compare_stock': compare_stock(df_compare),
        'error_message': error_message,
        'list_portfolio': list_portfolio,
    }
    return render(request, "home/portfolio/list_portfolio.html", context)


@login_required
def delete_portfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    list_activities = portfolio.activity_set.all()
    for activity in list_activities:
        activity.delete()
    portfolio.delete()
    return redirect('home:show_list_portfolio')


@login_required
def edit_portfolio(request, pk):
    list_portfolio = request.user.portfolio_set.all().order_by('name')
    stocks = Stock.objects.all().order_by('name')
    username = request.user
    portfolio = username.portfolio_set.get(id=pk)
    if request.method == 'POST':
        if request.POST:
            name = request.POST.get('name')
            pk_stock = request.POST.get('symbol')
            stock_rel = Stock.objects.get(id=pk_stock)
            print(stock_rel)

            portfolio.name = name
            portfolio.stock = stock_rel
            portfolio.save()
            return redirect('home:show_list_portfolio')

    context = {
        'portfolio': portfolio,
        'list_portfolio': list_portfolio,
        'stocks': stocks,
    }
    return render(request, "home/portfolio/edit_portfolio.html", context)