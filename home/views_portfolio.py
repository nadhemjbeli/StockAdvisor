from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from django.contrib.auth.decorators import login_required


@login_required
def get_list_portfolio(request):
    error_message = None
    list_portfolio = None
    try:
        username = request.user
        list_portfolio = username.portfolio_set.all().order_by('id')
    except:
        error_message = 'you have no portfolio yet'
    context = {
        'error_message': error_message,
        'list_portfolio': list_portfolio,
    }
    return render(request, "home/portfolio/list_portfolio.html", context)


@login_required
def delete_portfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    portfolio.delete()
    return redirect('home:show_list_portfolio')


@login_required
def edit_portfolio(request, pk):
    list_portfolio = request.user.portfolio_set.all().order_by('name')
    stocks = Stock.objects.all()
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