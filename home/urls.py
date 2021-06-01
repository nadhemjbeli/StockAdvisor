from django.urls import path
from .views import search_stock, get_stock, single_stock, get_cash_flow, get_income_statements, get_stock_summary \
    , stockAnalysis, home, get_historical_data, get_balance_sheet, get_profiles, get_news, \
    analysis_news, get_tesla_pred, get_apple_pred, get_stock_summary_candlestick, get_news_page
from .views_portfolio import get_list_portfolio, set_portfolio, delete_portfolio, edit_portfolio
from .views_activity import get_list_activity, add_activity, delete_activity, edit_activity, get_all_activity

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
    path('my_all_activities/', get_all_activity, name="show_all_activity"),
    path('activities/portfolio_<int:pk>', get_list_activity, name="show_list_activity"),
    path('add_activity/portfolio_<int:pk_portfolio>', add_activity, name="add_activity"),
    path('edit_activity_<int:pk_activity>/portfolio_<int:pk_portfolio>', edit_activity, name="edit_activity"),
    path('delete_activity_<int:pk_activity>/portfolio_<int:pk_portfolio>', delete_activity, name="delete_activity"),

    #stock financials
    path('stock/<str:symbol>/financials', get_income_statements, name='show_financials'),
    path('stock/<str:symbol>/cash_flow', get_cash_flow, name='show_cash_flow'),
    path('stock/<str:symbol>/balance_sheet', get_balance_sheet, name='show_balance_sheet'),
    path('stock/<str:symbol>/profile', get_profiles, name='show_profile'),
    path('stock/<str:symbol>/Summary_line', get_stock_summary, name='show_summary'),
    path('stock/<str:symbol>/Summary_candlestick', get_stock_summary_candlestick, name='show_summary_candlestick'),
    path('stock/<str:symbol>/Historical', get_historical_data, name='show_historical_data'),

    #stock analysis
    path('stock_analysis/<str:symbol>/<int:dtime>', stockAnalysis, name='stock_analysis'),


    #stock news
    path('show_news/', get_news, name='show_news'),
    path('news/<str:symbol>', get_news_page, name='show_news_page'),
    path('analysis_news/', analysis_news, name='analysis_news'),

    #stock predictions
    path('tesla_pred/', get_tesla_pred, name='tesla_pred'),
    path('apple_pred/', get_apple_pred, name='apple_pred'),
]