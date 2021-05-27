from django.urls import path
from .views import search_stock, get_stock, single_stock, get_cash_flow, get_income_statements, get_stock_summary \
    , stockAnalysis, home, get_historical_data, get_balance_sheet, get_profiles, set_portfolio, get_news,\
    analysis_news, get_tesla_pred, get_apple_pred
from .views_portfolio import get_list_portfolio, delete_portfolio, edit_portfolio
from .views_activity import get_list_activity

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),

    # search and show stock
    path('search_stock/', search_stock, name="show_stock_vis"),
    # path('show_data/', views.show_data, name='show_data'),
    path('show_stocks/', get_stock, name='show_stocks'),
    path('stock/<str:symbol>', single_stock, name='show_single_stock'),

    #portfolio
    path('create_portfolio/', set_portfolio, name="create_portfolio"),
    path('list_portfolio/', get_list_portfolio, name="show_list_portfolio"),
    path('edit_portfolio/<int:pk>', edit_portfolio, name="edit_portfolio"),
    path('delete_portfolio/<int:pk>', delete_portfolio, name="delete_portfolio"),

    #portfolio_activity
    path('activities/portfolio/<int:pk>', get_list_activity, name="show_list_activity"),

    #stock financials
    path('stock/<str:symbol>/financials', get_income_statements, name='show_financials'),
    path('stock/<str:symbol>/cash_flow', get_cash_flow, name='show_cash_flow'),
    path('stock/<str:symbol>/balance_sheet', get_balance_sheet, name='show_balance_sheet'),
    path('stock/<str:symbol>/profile', get_profiles, name='show_profile'),
    path('stock/<str:symbol>/Summary', get_stock_summary, name='show_summary'),
    path('stock/<str:symbol>/Historical', get_historical_data, name='show_historical_data'),

    #stock analysis
    path('stock_analysis/<str:symbol>/<int:dtime>', stockAnalysis, name='stock_analysis'),


    #stock news
    path('show_news/', get_news, name='show_news'),
    path('analysis_news/', analysis_news, name='analysis_news'),

    #stock predictions
    path('tesla_pred/', get_tesla_pred, name='tesla_pred'),
    path('apple_pred/', get_apple_pred, name='apple_pred'),
]