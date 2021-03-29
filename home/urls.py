from django.urls import path
from .views import search_stock, get_stock, single_stock, get_cash_flow, get_income_statements, get_stock_summary \
    , stockAnalysis, home, get_historical_data, get_balance_sheet

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('search_stock/', search_stock, name="show_stock_vis"),
    # path('show_data/', views.show_data, name='show_data'),
    path('show_stocks/', get_stock, name='show_stocks'),
    path('stock/<str:symbol>', single_stock, name='show_single_stock'),
    path('stock/<str:symbol>/financials', get_income_statements, name='show_financials'),
    path('stock/<str:symbol>/cash_flow', get_cash_flow, name='show_cash_flow'),
    path('stock/<str:symbol>/balance_sheet', get_balance_sheet, name='show_balance_sheet'),
    path('stock/<str:symbol>/Summary', get_stock_summary, name='show_summary'),
    path('stock/<str:symbol>/Historical', get_historical_data, name='show_historical_data'),
    path('stock_analysis/<str:symbol>/<int:dtime>', stockAnalysis, name='stock_analysis'),
]