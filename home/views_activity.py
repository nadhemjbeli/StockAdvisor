from django.shortcuts import render, redirect


def get_list_activity(request, pk):
    error_portfolio_message = None
    error_activity_message = None
    portfolio = None
    list_activity = None
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